"""
P3-001: Chat API — 실제 LLM(OpenAI / Gemini) 연결 구현

우선순위:
  1. OPENAI_API_KEY 환경변수 → OpenAI GPT-4o-mini 사용
  2. GEMINI_API_KEY 환경변수 → Google Gemini Flash 사용
  3. 둘 다 없으면 → 실제 DB 검색 결과 기반 템플릿 응답

NLP 파싱 전략:
  - LLM에게 JSON 구조화된 intent를 추출하게 함 (function calling / structured output)
  - intent: search_gpu | compare_price | explain | general
  - 추출된 intent로 실제 DB 조회 후 결과를 LLM에 컨텍스트로 제공 (RAG-lite)
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
import json
import logging

from apps.api.core.database import get_db
from apps.api.core.config import settings
from apps.services.gpu.models_history import PriceHistory

router = APIRouter()
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    query: str

class IntentResult(BaseModel):
    intent: str          # search_gpu | compare_price | explain | general
    gpu_model: Optional[str] = None
    provider: Optional[str] = None
    budget_usd: Optional[float] = None

class ChatResponse(BaseModel):
    answer: str
    action_type: str
    payload: dict = {}
    source: str = "llm"  # llm | template | error


# ── LLM 클라이언트 초기화 ─────────────────────────────────
def _get_openai_client():
    api_key = getattr(settings, "OPENAI_API_KEY", None)
    if not api_key:
        return None
    try:
        from openai import AsyncOpenAI
        return AsyncOpenAI(api_key=api_key)
    except ImportError:
        logger.warning("[Chat] openai 패키지 미설치")
        return None

def _get_gemini_client():
    api_key = getattr(settings, "GEMINI_API_KEY", None)
    if not api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except ImportError:
        logger.warning("[Chat] google-generativeai 패키지 미설치")
        return None


# ── Intent 추출 ────────────────────────────────────────────
INTENT_SYSTEM_PROMPT = """You are an AI assistant for InfraIndex, a GPU cloud price comparison platform.

Extract the user's intent from their query and return ONLY a valid JSON object with:
- "intent": one of ["search_gpu", "compare_price", "explain", "general"]
- "gpu_model": GPU model name if mentioned (e.g. "H100", "RTX 4090", null if not mentioned)
- "provider": cloud provider if mentioned (e.g. "vast-ai", "runpod", "aws", null if not mentioned)
- "budget_usd": hourly budget in USD if mentioned (e.g. 2.0, null if not mentioned)

Examples:
Query: "H100 가격 알려줘" → {"intent":"search_gpu","gpu_model":"H100","provider":null,"budget_usd":null}
Query: "runpod vs vast 비교" → {"intent":"compare_price","gpu_model":null,"provider":null,"budget_usd":null}
Query: "시간당 2달러 이하 A100" → {"intent":"search_gpu","gpu_model":"A100","provider":null,"budget_usd":2.0}

Return ONLY the JSON, no other text."""

async def _extract_intent_openai(client, query: str) -> IntentResult:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": INTENT_SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        response_format={"type": "json_object"},
        max_tokens=150,
        temperature=0.1,
    )
    data = json.loads(response.choices[0].message.content)
    return IntentResult(**data)

async def _extract_intent_gemini(client, query: str) -> IntentResult:
    prompt = f"{INTENT_SYSTEM_PROMPT}\n\nQuery: {query}"
    response = await client.generate_content_async(prompt)
    text = response.text.strip()
    # JSON 블록 추출
    if "```" in text:
        text = text.split("```")[1].replace("json", "").strip()
    data = json.loads(text)
    return IntentResult(**data)


# ── DB 컨텍스트 조회 ──────────────────────────────────────
async def _fetch_price_context(db: AsyncSession, intent: IntentResult) -> Dict:
    """Intent에 맞는 실제 DB 데이터 조회 (RAG-lite context)"""
    if not intent.gpu_model:
        return {}

    since_days = 7
    from datetime import datetime, timedelta, timezone
    since = datetime.now(timezone.utc) - timedelta(days=since_days)

    query = (
        select(
            PriceHistory.provider_id,
            PriceHistory.gpu_model,
            func.min(PriceHistory.price_per_hour).label("min_price"),
            func.max(PriceHistory.price_per_hour).label("max_price"),
            func.avg(PriceHistory.price_per_hour).label("avg_price"),
            func.count(PriceHistory.id).label("cnt"),
        )
        .where(PriceHistory.gpu_model.ilike(f"%{intent.gpu_model}%"))
        .where(PriceHistory.timestamp >= since)
        .group_by(PriceHistory.provider_id, PriceHistory.gpu_model)
        .order_by(func.min(PriceHistory.price_per_hour).asc())
    )
    if intent.provider:
        query = query.where(PriceHistory.provider_id == intent.provider)
    if intent.budget_usd:
        query = query.having(func.min(PriceHistory.price_per_hour) <= intent.budget_usd)

    result = await db.execute(query)
    rows = result.all()

    return {
        "gpu_model": intent.gpu_model,
        "providers": [
            {
                "provider": r.provider_id,
                "min_price": round(float(r.min_price), 4),
                "max_price": round(float(r.max_price), 4),
                "avg_price": round(float(r.avg_price), 4),
                "data_points": r.cnt,
            }
            for r in rows
        ],
    }


# ── 답변 생성 ─────────────────────────────────────────────
ANSWER_SYSTEM_PROMPT = """You are InfraIndex AI assistant. Answer in the same language as the user's query (Korean if Korean, English if English).
Be concise, data-driven, and helpful. Format prices as $/hr."""

async def _generate_answer_openai(client, query: str, context: Dict) -> str:
    ctx_str = json.dumps(context, ensure_ascii=False) if context else "No price data available yet."
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
            {"role": "user", "content": f"Question: {query}\n\nPrice Data Context:\n{ctx_str}"},
        ],
        max_tokens=400,
        temperature=0.3,
    )
    return response.choices[0].message.content

async def _generate_answer_gemini(client, query: str, context: Dict) -> str:
    ctx_str = json.dumps(context, ensure_ascii=False) if context else "No price data available yet."
    prompt = f"{ANSWER_SYSTEM_PROMPT}\n\nQuestion: {query}\n\nPrice Data Context:\n{ctx_str}"
    response = await client.generate_content_async(prompt)
    return response.text

def _template_answer(query: str, context: Dict) -> str:
    """LLM 없을 때 DB 데이터 기반 템플릿 응답"""
    if not context or not context.get("providers"):
        return (
            f"'{query}'에 대한 검색 결과를 찾지 못했습니다. "
            "현재 수집된 데이터가 없거나 해당 GPU 모델이 지원되지 않습니다. "
            "검색창에서 직접 GPU 모델명을 검색해보세요."
        )
    gpu = context["gpu_model"]
    providers = context["providers"]
    cheapest = providers[0]
    lines = [f"**{gpu}** 최저가 기준 (최근 7일):"]
    for p in providers[:5]:
        lines.append(f"• {p['provider']}: ${p['min_price']:.4f}~${p['max_price']:.4f}/hr (평균 ${p['avg_price']:.4f})")
    lines.append(f"\n최저가: **{cheapest['provider']}** $**{cheapest['min_price']:.4f}**/hr")
    return "\n".join(lines)


# ── 메인 엔드포인트 ───────────────────────────────────────
@router.post("/", response_model=ChatResponse)
async def chat_query(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    P3-001: NLP Query Engine — 실제 LLM 연결 (OpenAI / Gemini)
    자연어 질문을 파싱 → DB 조회 → LLM 답변 생성 (RAG-lite)

    우선순위: OpenAI → Gemini → 템플릿 응답
    """
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    openai_client = _get_openai_client()
    gemini_client = _get_gemini_client() if not openai_client else None

    intent = IntentResult(intent="general")
    context: Dict = {}
    source = "template"

    try:
        # 1단계: Intent 추출
        if openai_client:
            intent = await _extract_intent_openai(openai_client, query)
            source = "openai"
        elif gemini_client:
            intent = await _extract_intent_gemini(gemini_client, query)
            source = "gemini"

        # 2단계: DB에서 컨텍스트 조회
        if intent.intent in ("search_gpu", "compare_price") and intent.gpu_model:
            context = await _fetch_price_context(db, intent)

        # 3단계: 답변 생성
        if openai_client:
            answer = await _generate_answer_openai(openai_client, query, context)
        elif gemini_client:
            answer = await _generate_answer_gemini(gemini_client, query, context)
        else:
            answer = _template_answer(query, context)
            source = "template"

    except json.JSONDecodeError as e:
        logger.warning(f"[Chat] Intent JSON parse failed: {e} — falling back to template")
        context = await _fetch_price_context(db, IntentResult(intent="search_gpu", gpu_model=query[:50]))
        answer = _template_answer(query, context)
        source = "template"
    except Exception as e:
        logger.error(f"[Chat] LLM error: {e}", exc_info=True)
        answer = f"일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요. ({type(e).__name__})"
        source = "error"

    return ChatResponse(
        answer=answer,
        action_type=intent.intent,
        payload=context,
        source=source,
    )

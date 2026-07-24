import os
import requests
import logging
from datetime import date
from typing import Dict, Any, List

from shared.db.session import _build_engine, _build_session_factory
from shared.models.ai_pricing import AIModelMaster, AIModelPriceHistory
from sqlalchemy.future import select

logger = logging.getLogger(__name__)

# OpenRouter API URL
OPENROUTER_MODELS_API = "https://openrouter.ai/api/v1/models"

# Define the models we want to track and their tiers
# model_id must match OpenRouter's "id" field
TARGET_MODELS = {
    # Tier 0 (Deep Reasoning)
    "openai/o1-preview": {"tier": "Tier 0", "provider": "OpenAI", "name": "o1-preview"},
    "openai/o1-mini": {"tier": "Tier 0", "provider": "OpenAI", "name": "o1-mini"},
    
    # Tier 1 (Flagship)
    "anthropic/claude-3-opus": {"tier": "Tier 1", "provider": "Anthropic", "name": "Claude 3 Opus"},
    "openai/gpt-4o": {"tier": "Tier 1", "provider": "OpenAI", "name": "GPT-4o"},
    "google/gemini-1.5-pro": {"tier": "Tier 1", "provider": "Google", "name": "Gemini 1.5 Pro"},
    "meta-llama/llama-3.1-405b-instruct": {"tier": "Tier 1", "provider": "Meta", "name": "Llama 3.1 405B"},
    
    # Tier 2 (Sweet Spot)
    "anthropic/claude-3.5-sonnet": {"tier": "Tier 2", "provider": "Anthropic", "name": "Claude 3.5 Sonnet"},
    "meta-llama/llama-3.1-70b-instruct": {"tier": "Tier 2", "provider": "Meta", "name": "Llama 3.1 70B"},
    "mistralai/mistral-large": {"tier": "Tier 2", "provider": "Mistral", "name": "Mistral Large"},
    
    # Tier 3 (Fast & Cheap)
    "google/gemini-1.5-flash": {"tier": "Tier 3", "provider": "Google", "name": "Gemini 1.5 Flash"},
    "anthropic/claude-3-haiku": {"tier": "Tier 3", "provider": "Anthropic", "name": "Claude 3 Haiku"},
    "openai/gpt-4o-mini": {"tier": "Tier 3", "provider": "OpenAI", "name": "GPT-4o-mini"},
    "meta-llama/llama-3.1-8b-instruct": {"tier": "Tier 3", "provider": "Meta", "name": "Llama 3.1 8B"},
    "mistralai/mistral-nemo": {"tier": "Tier 3", "provider": "Mistral", "name": "Mistral NeMo"}
}


async def crawl_openrouter_pricing():
    """
    OpenRouter API를 호출하여 대상 모델들의 최신 가격 정보를 DB에 적재합니다.
    """
    logger.info("Starting OpenRouter pricing crawler...")
    
    try:
        response = requests.get(OPENROUTER_MODELS_API, timeout=10)
        response.raise_for_status()
        data = response.json()
        models = data.get("data", [])
    except Exception as e:
        logger.error(f"Failed to fetch OpenRouter models: {e}")
        # Telegram alert would go here (Phase 2)
        raise

    today = date.today()
    updated_count = 0
    engine = _build_engine()
    AsyncSessionLocal = _build_session_factory(engine)
    
    async with AsyncSessionLocal() as session:
        for model_data in models:
            model_id = model_data.get("id")
            if model_id not in TARGET_MODELS:
                continue

            # Extract pricing (OpenRouter returns price per token)
            # We multiply by 1,000,000 to get price per 1M tokens.
            pricing = model_data.get("pricing", {})
            try:
                input_price_per_token = float(pricing.get("prompt", 0))
                output_price_per_token = float(pricing.get("completion", 0))
            except (ValueError, TypeError):
                continue
                
            input_price_1m = input_price_per_token * 1_000_000
            output_price_1m = output_price_per_token * 1_000_000
            
            context_length = model_data.get("context_length")
            
            target_info = TARGET_MODELS[model_id]

            # 1. Upsert AIModelMaster
            stmt = select(AIModelMaster).where(AIModelMaster.model_code == model_id)
            result = await session.execute(stmt)
            master = result.scalars().first()
            
            if not master:
                master = AIModelMaster(
                    model_code=model_id,
                    name=target_info["name"],
                    provider=target_info["provider"],
                    tier=target_info["tier"],
                    context_length=context_length
                )
                session.add(master)
                await session.flush() # get ID
            else:
                master.context_length = context_length

            # 2. Insert or Update AIModelPriceHistory for today
            hist_stmt = select(AIModelPriceHistory).where(
                AIModelPriceHistory.model_id == master.id,
                AIModelPriceHistory.collected_date == today
            )
            hist_result = await session.execute(hist_stmt)
            history = hist_result.scalars().first()

            if not history:
                history = AIModelPriceHistory(
                    model_id=master.id,
                    collected_date=today,
                    input_price_1m=input_price_1m,
                    output_price_1m=output_price_1m
                )
                session.add(history)
            else:
                history.input_price_1m = input_price_1m
                history.output_price_1m = output_price_1m

            updated_count += 1

        await session.commit()
        logger.info(f"Successfully updated pricing for {updated_count} AI models.")

    return updated_count

if __name__ == "__main__":
    import asyncio
    # Simple manual run
    asyncio.run(crawl_openrouter_pricing())

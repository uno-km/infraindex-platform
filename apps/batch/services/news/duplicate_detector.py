"""
apps/services/news/duplicate_detector.py
Phase 8 - SimHash + URL 정규화 기반 뉴스 중복 감지 엔진

사용 방법:
    detector = DuplicateDetector()
    if not detector.is_duplicate(article):
        detector.register_article(article)
        await save_article(article)
"""
import hashlib
import re
import logging
from urllib.parse import urlparse, urlencode, parse_qsl, urlunparse
from typing import Dict, Any, Set, List, Optional

logger = logging.getLogger(__name__)

# UTM 및 트래킹 파라미터 (제거 대상)
_TRACKING_PARAMS = frozenset({
    "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
    "fbclid", "gclid", "msclkid", "ref", "source", "campaign",
    "_ga", "yclid", "mc_cid", "mc_eid",
})


class SimHash:
    """
    SimHash 알고리즘 구현.
    텍스트를 64비트 정수로 해싱하여 유사 문서 비교에 사용.
    """

    HASH_BITS = 64

    def __init__(self, text: str):
        self.value = self._compute(text)

    def _compute(self, text: str) -> int:
        """텍스트 → 64비트 SimHash 정수"""
        tokens = self._tokenize(text)
        if not tokens:
            return 0

        v = [0] * self.HASH_BITS
        for token in tokens:
            h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
            for i in range(self.HASH_BITS):
                bit = 1 if h & (1 << i) else -1
                v[i] += bit

        fingerprint = 0
        for i in range(self.HASH_BITS):
            if v[i] > 0:
                fingerprint |= (1 << i)
        return fingerprint

    def _tokenize(self, text: str) -> List[str]:
        """텍스트를 소문자 토큰으로 분리 (2-gram 포함)"""
        text = text.lower()
        words = re.findall(r"\w+", text)
        # unigram + bigram
        tokens = words[:]
        tokens += [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]
        return tokens

    def hamming_distance(self, other: "SimHash") -> int:
        """두 SimHash 간 해밍 거리 (비트 차이 수)"""
        xor = self.value ^ other.value
        return bin(xor).count("1")

    def similarity(self, other: "SimHash") -> float:
        """유사도 (0.0 ~ 1.0). 1.0이면 동일"""
        dist = self.hamming_distance(other)
        return 1.0 - dist / self.HASH_BITS


class DuplicateDetector:
    """
    SimHash + URL 해시 기반 뉴스 중복 감지기.

    사용 예:
        detector = DuplicateDetector(similarity_threshold=0.85)
        if not detector.is_duplicate({"url": "...", "title": "..."}):
            detector.register_article({"url": "...", "title": "..."})
    """

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        self._url_cache: Set[str] = set()
        # (simhash_value, title) 목록
        self._simhash_cache: List[SimHash] = []

    # ─────────────────────────────── URL 처리 ────────────────────────────────

    def normalize_url(self, url: str) -> str:
        """
        URL 정규화:
        1. trailing slash 제거
        2. UTM/트래킹 파라미터 제거
        3. 소문자 scheme/host
        """
        try:
            parsed = urlparse(url)
            # 의미있는 파라미터만 유지
            params = [
                (k, v) for k, v in parse_qsl(parsed.query)
                if k.lower() not in _TRACKING_PARAMS
            ]
            # 정렬하여 순서 무관
            params.sort()
            clean_query = urlencode(params)

            normalized = urlunparse((
                parsed.scheme.lower(),
                parsed.netloc.lower(),
                parsed.path.rstrip("/"),
                parsed.params,
                clean_query,
                "",  # fragment 제거
            ))
            return normalized
        except Exception:
            return url.rstrip("/")

    def url_to_hash(self, url: str) -> str:
        """URL → SHA-256 해시 (64자 hex 문자열)"""
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    def is_url_duplicate(self, url: str) -> bool:
        """URL이 이미 처리된 적 있으면 True"""
        h = self.url_to_hash(self.normalize_url(url))
        return h in self._url_cache

    def register_url(self, url: str) -> None:
        """URL을 중복 캐시에 등록"""
        h = self.url_to_hash(self.normalize_url(url))
        self._url_cache.add(h)

    # ─────────────────────────────── SimHash 처리 ────────────────────────────

    def compute_simhash(self, text: str) -> int:
        """텍스트 → SimHash 정수값"""
        return SimHash(text).value

    def compute_similarity(self, text1: str, text2: str) -> float:
        """두 텍스트의 SimHash 유사도 (0.0 ~ 1.0)"""
        sh1 = SimHash(text1)
        sh2 = SimHash(text2)
        return sh1.similarity(sh2)

    def is_title_duplicate(self, title: str) -> bool:
        """제목 SimHash가 기존 항목과 임계값 이상 유사하면 True"""
        sh = SimHash(title)
        for existing in self._simhash_cache:
            if sh.similarity(existing) >= self.similarity_threshold:
                return True
        return False

    def register_simhash(self, title: str) -> None:
        """제목 SimHash를 캐시에 등록"""
        self._simhash_cache.append(SimHash(title))

    # ─────────────────────────────── 통합 인터페이스 ─────────────────────────

    def is_duplicate(self, article: Dict[str, Any]) -> bool:
        """
        아티클이 중복인지 판별.
        1차: URL 해시 (빠름)
        2차: 제목 SimHash (정밀)
        """
        url = article.get("url", "")
        title = article.get("title", "")

        # 1차: URL 중복 체크
        if url and self.is_url_duplicate(url):
            logger.debug(f"[DuplicateDetector] URL 중복: {url}")
            return True

        # 2차: 제목 SimHash 중복 체크
        if title and self.is_title_duplicate(title):
            logger.debug(f"[DuplicateDetector] 제목 유사 중복: {title[:60]}")
            return True

        return False

    def register_article(self, article: Dict[str, Any]) -> None:
        """아티클을 중복 캐시에 등록"""
        url = article.get("url", "")
        title = article.get("title", "")

        if url:
            self.register_url(url)
        if title:
            self.register_simhash(title)

    @property
    def cache_size(self) -> Dict[str, int]:
        """현재 캐시 크기 반환"""
        return {
            "url_cache": len(self._url_cache),
            "simhash_cache": len(self._simhash_cache),
        }

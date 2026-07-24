"""
tests/unit/services/news/test_duplicate_detector_v2.py
Phase 8 - DuplicateDetector SimHash + URL 중복 감지 유닛 테스트
"""
import pytest
from unittest.mock import AsyncMock, MagicMock


class TestDuplicateDetector:
    """DuplicateDetector 중복 감지 엔진 유닛 테스트"""

    def test_import(self):
        """DuplicateDetector 임포트 가능해야 한다"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        assert DuplicateDetector is not None

    def test_url_normalization_strips_trailing_slash(self):
        """URL 정규화: trailing slash 제거"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        assert d.normalize_url("https://example.com/article/") == "https://example.com/article"

    def test_url_normalization_strips_utm(self):
        """URL 정규화: UTM 파라미터 제거"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        url = "https://example.com/article?utm_source=twitter&utm_medium=social"
        norm = d.normalize_url(url)
        assert "utm_source" not in norm
        assert "utm_medium" not in norm

    def test_url_normalization_keeps_significant_params(self):
        """URL 정규화: 의미있는 파라미터는 유지"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        url = "https://example.com/article?id=12345"
        norm = d.normalize_url(url)
        assert "id=12345" in norm

    def test_url_hash_consistent(self):
        """동일 URL은 항상 같은 해시를 반환해야 한다"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        url = "https://example.com/article"
        assert d.url_to_hash(url) == d.url_to_hash(url)

    def test_url_hash_is_string(self):
        """URL 해시는 16진수 문자열이어야 한다"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        h = d.url_to_hash("https://example.com/article")
        assert isinstance(h, str)
        assert len(h) == 64  # SHA-256

    def test_simhash_same_text_same_hash(self):
        """동일 텍스트는 동일 SimHash를 반환해야 한다"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        text = "NVIDIA announces new H200 GPU with improved HBM3 memory"
        assert d.compute_simhash(text) == d.compute_simhash(text)

    def test_simhash_similar_texts_high_similarity(self):
        """유사한 텍스트는 높은 유사도를 반환해야 한다 (≥ 0.75)"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        t1 = "NVIDIA announces H200 GPU for AI workloads"
        t2 = "NVIDIA unveils H200 GPU designed for AI workloads"
        sim = d.compute_similarity(t1, t2)
        assert sim >= 0.75, f"유사도 너무 낮음: {sim:.3f}"

    def test_simhash_different_texts_low_similarity(self):
        """완전히 다른 텍스트는 낮은 유사도를 반환해야 한다 (< 0.7)"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        t1 = "NVIDIA GPU market share reaches record high in datacenter"
        t2 = "Korean restaurant opens new branch in Gangnam district Seoul"
        sim = d.compute_similarity(t1, t2)
        assert sim < 0.7, f"유사도 너무 높음: {sim:.3f}"

    def test_is_url_duplicate_exact_match(self):
        """URL 해시가 캐시에 있으면 중복으로 판별해야 한다"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        url = "https://example.com/news/nvidia-h200"
        url_hash = d.url_to_hash(d.normalize_url(url))
        # 캐시에 미리 추가
        d._url_cache.add(url_hash)
        assert d.is_url_duplicate(url) is True

    def test_is_url_duplicate_new_url(self):
        """캐시에 없는 URL은 중복이 아니어야 한다"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        url = "https://new.example.com/brand-new-article"
        assert d.is_url_duplicate(url) is False

    def test_register_url(self):
        """URL 등록 후 중복으로 판별되어야 한다"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        url = "https://example.com/register-test"
        assert d.is_url_duplicate(url) is False
        d.register_url(url)
        assert d.is_url_duplicate(url) is True

    def test_threshold_default_is_085(self):
        """기본 유사도 임계값은 0.85여야 한다"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        assert d.similarity_threshold == 0.85

    def test_custom_threshold(self):
        """임계값 커스터마이징 가능해야 한다"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector(similarity_threshold=0.90)
        assert d.similarity_threshold == 0.90

    def test_is_duplicate_combines_url_and_simhash(self):
        """is_duplicate는 URL과 SimHash를 모두 고려해야 한다"""
        from apps.batch.services.news.duplicate_detector import DuplicateDetector
        d = DuplicateDetector()
        article1 = {"url": "https://example.com/article-1", "title": "NVIDIA H100 GPU price drops 20%"}
        article2 = {"url": "https://example.com/article-2", "title": "NVIDIA H100 GPU price drops 20%"}

        d.register_article(article1)

        # 다른 URL이지만 동일한 제목 → SimHash로 중복 감지 (임계값 0.85)
        result = d.is_duplicate(article2)
        # 제목이 완전히 동일하므로 SimHash 유사도 1.0 → 중복
        assert result is True

"""
tests/unit/services/news/test_tag_mapper.py
Phase 2 - classify_article() 키워드 분류(태그 매핑) 유닛 테스트
"""
import pytest
from apps.batch.services.news.config import classify_article, CATEGORY_KEYWORDS


class TestClassifyArticle:
    """classify_article 함수 단위 테스트"""

    def test_empty_text_returns_no_category(self):
        """빈 문자열은 아무 카테고리도 반환하지 않아야 한다"""
        result = classify_article("")
        assert result["categories"] == []
        assert result["primary_category"] is None
        assert result["is_semiconductor_related"] is False

    def test_none_text_returns_no_category(self):
        """None 입력도 안전하게 처리해야 한다"""
        result = classify_article(None)
        assert result["categories"] == []
        assert result["is_semiconductor_related"] is False

    def test_gpu_keywords_classified_as_gpu(self):
        """H100, RTX, NVIDIA 등 GPU 키워드가 포함된 텍스트는 GPU로 분류해야 한다"""
        texts = [
            "NVIDIA H100 GPU performance benchmark results",
            "RTX 4090 price drop announced by vendors",
            "Cloud GPU rental market sees price competition",
        ]
        for text in texts:
            result = classify_article(text)
            assert "GPU" in result["categories"], f"GPU 분류 실패: {text}"
            assert result["is_semiconductor_related"] is True

    def test_category_keywords_not_empty(self):
        """CATEGORY_KEYWORDS에 최소 2개 이상의 카테고리가 정의되어야 한다"""
        assert len(CATEGORY_KEYWORDS) >= 2

    def test_gpu_category_exists(self):
        """GPU 카테고리가 CATEGORY_KEYWORDS에 있어야 한다"""
        assert "GPU" in CATEGORY_KEYWORDS

    def test_datacenter_keyword_matched(self):
        """datacenter 키워드가 있는 텍스트는 반도체 관련으로 분류되어야 한다"""
        text = "New datacenter design uses liquid cooling for AI server clusters"
        result = classify_article(text)
        # datacenter는 인프라 카테고리에 있으므로 반도체 관련으로 분류
        assert result["is_semiconductor_related"] is True

    def test_multi_category_article(self):
        """여러 카테고리 키워드가 포함된 기사는 다중 카테고리 반환해야 한다"""
        text = "NVIDIA H100 GPU powers new datacenter with liquid cooling and HBM3e memory"
        result = classify_article(text)
        assert len(result["categories"]) >= 2

    def test_unrelated_text_returns_no_category(self):
        """반도체/GPU 무관 텍스트는 분류되지 않아야 한다"""
        text = "The best coffee shops in Seoul for remote work in 2026"
        result = classify_article(text)
        assert result["is_semiconductor_related"] is False
        assert result["categories"] == []

    def test_case_insensitive_matching(self):
        """키워드 매칭은 대소문자를 구분하지 않아야 한다"""
        upper_text = "NVIDIA GPU PRICE ANALYSIS"
        lower_text = "nvidia gpu price analysis"
        result_upper = classify_article(upper_text)
        result_lower = classify_article(lower_text)
        assert result_upper["is_semiconductor_related"] == result_lower["is_semiconductor_related"]

    def test_matched_keywords_returned(self):
        """매칭된 키워드 목록도 반환되어야 한다"""
        text = "nvidia rtx gpu performance analysis"
        result = classify_article(text)
        assert isinstance(result["matched_keywords"], list)
        assert len(result["matched_keywords"]) >= 1

    def test_primary_category_is_str_or_none(self):
        """primary_category는 문자열 또는 None이어야 한다"""
        result = classify_article("NVIDIA H100 GPU")
        assert isinstance(result["primary_category"], (str, type(None)))

"""
tests/unit/services/news/test_heuristic_predictor.py
Phase 2 - 뉴스 감성/관련도 휴리스틱 예측 유닛 테스트
"""
import pytest
from apps.services.news.config import classify_article, CATEGORY_KEYWORDS


class TestHeuristicPredictor:
    """뉴스 기사의 반도체/GPU 관련도 휴리스틱 예측 품질 테스트"""

    POSITIVE_CASES = [
        "Samsung and SK Hynix compete for HBM4 supply contract",
        "TSMC 2nm process node enters risk production phase",
        "NVIDIA H200 GPU cloud rental drops to $2.50 per hour",
        "Intel Foundry Services announces new packaging technology",
        "DDR5 memory prices decline amid oversupply concerns",
        "AI datacenter power consumption reaches record levels",
        "Micron releases new GDDR6 chip for consumer graphics",
        "RTX 5090 benchmark leaks show 60 percent improvement over 4090",
    ]

    NEGATIVE_CASES = [
        "Real estate prices in Seoul rise for third consecutive month",
        "New recipe: How to make perfect Korean BBQ at home",
        "Football World Cup 2026 predictions and analysis",
        "Local coffee shop chain expands to 100 locations",
    ]

    def test_precision_positive_cases(self):
        """Precision: 긍정 케이스 중 올바르게 분류된 비율이 75% 이상이어야 한다"""
        correct = sum(
            1 for text in self.POSITIVE_CASES
            if classify_article(text)["is_semiconductor_related"]
        )
        precision = correct / len(self.POSITIVE_CASES)
        assert precision >= 0.75, f"Precision 미달: {precision:.2f}"

    def test_specificity_negative_cases(self):
        """Specificity: 부정 케이스가 올바르게 무관으로 분류되어야 한다"""
        correct = sum(
            1 for text in self.NEGATIVE_CASES
            if not classify_article(text)["is_semiconductor_related"]
        )
        specificity = correct / len(self.NEGATIVE_CASES)
        assert specificity == 1.0, f"Specificity 미달: {specificity:.2f}"

    def test_nvidia_detected(self):
        """NVIDIA 키워드 감지 테스트"""
        result = classify_article("nvidia announces new gpu")
        assert result["is_semiconductor_related"] is True

    def test_tsmc_detected(self):
        """TSMC 키워드 감지 테스트"""
        result = classify_article("tsmc expands capacity")
        assert result["is_semiconductor_related"] is True

    def test_sk_hynix_detected(self):
        """SK Hynix 키워드 감지 테스트"""
        result = classify_article("sk hynix hbm production")
        assert result["is_semiconductor_related"] is True

    def test_micron_detected(self):
        """Micron 키워드 감지 테스트"""
        result = classify_article("micron dram chip shortage")
        assert result["is_semiconductor_related"] is True

    def test_primary_category_is_single(self):
        """primary_category는 단일 문자열 또는 None이어야 한다"""
        text = "NVIDIA H100 GPU powers new datacenter"
        result = classify_article(text)
        assert isinstance(result["primary_category"], (str, type(None)))

    def test_matched_keywords_are_from_config(self):
        """matched_keywords는 CATEGORY_KEYWORDS에 정의된 키워드여야 한다"""
        all_known_keywords = set()
        for kws in CATEGORY_KEYWORDS.values():
            all_known_keywords.update(kw.lower() for kw in kws)

        text = "nvidia gpu h100 dram memory"
        result = classify_article(text)
        for kw in result["matched_keywords"]:
            assert kw.lower() in all_known_keywords, f"알 수 없는 키워드: {kw}"

    def test_empty_input_graceful_handling(self):
        """빈/None 입력에 대해 예외 없이 기본값 반환해야 한다"""
        for inp in ["", None]:
            try:
                result = classify_article(inp)
                assert isinstance(result, dict)
                assert "is_semiconductor_related" in result
            except Exception as e:
                pytest.fail(f"입력 {inp!r}에서 예외 발생: {e}")

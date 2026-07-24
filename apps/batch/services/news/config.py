# apps/services/news/config.py

# 뉴스/유튜브 분류를 위한 키워드 사전
CATEGORY_KEYWORDS = {
    "GPU": [
        "gpu", "그래픽카드", "nvidia", "amd gpu", "intel gpu", 
        "geforce", "radeon", "rtx", "h100", "h200", "b100", "b200", 
        "blackwell", "gpu price", "gpu rental", "cloud gpu"
    ],
    "반도체": [
        "반도체", "semiconductor", "chip", "foundry", "fab", "wafer", 
        "packaging", "advanced packaging", "tsmc", "samsung semiconductor", 
        "sk hynix", "micron", "intel foundry"
    ],
    "메모리": [
        "dram", "ram", "memory", "nand", "hbm", "hbm3e", "hbm4", 
        "ddr4", "ddr5", "gddr6", "gddr7", "lpddr", "dram spot price", "memory price"
    ],
    "데이터센터": [
        "데이터센터", "data center", "datacenter", "ai server", "ai infrastructure", 
        "hyperscaler", "server gpu", "liquid cooling", "power infrastructure"
    ]
}

def classify_article(text: str):
    """
    제목이나 본문을 기반으로 카테고리와 키워드를 추출합니다.
    """
    if not text:
        return {
            "categories": [],
            "primary_category": None,
            "matched_keywords": [],
            "is_semiconductor_related": False
        }
        
    text = text.lower()
    matched_categories = set()
    matched_keywords = set()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                matched_categories.add(category)
                matched_keywords.add(kw)
                
    is_semi_related = len(matched_categories) > 0
    
    return {
        "categories": list(matched_categories),
        "primary_category": list(matched_categories)[0] if matched_categories else None,
        "matched_keywords": list(matched_keywords),
        "is_semiconductor_related": is_semi_related
    }

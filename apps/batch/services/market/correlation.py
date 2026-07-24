import math
from typing import List, Tuple, Dict, Any

def calculate_pearson(x: List[float], y: List[float]) -> float:
    n = len(x)
    if n == 0 or n != len(y):
        return 0.0

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
    sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)

    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    if denominator == 0:
        return 0.0

    return numerator / denominator


def calculate_spearman(x: List[float], y: List[float]) -> float:
    n = len(x)
    if n == 0 or n != len(y):
        return 0.0

    # Create ranks
    def get_ranks(arr: List[float]) -> List[float]:
        sorted_indices = sorted(range(len(arr)), key=lambda k: arr[k])
        ranks = [0.0] * len(arr)
        for rank, idx in enumerate(sorted_indices):
            ranks[idx] = rank + 1
        return ranks
        
    rank_x = get_ranks(x)
    rank_y = get_ranks(y)
    
    return calculate_pearson(rank_x, rank_y)


def normalize_series(data: List[float]) -> List[float]:
    """첫 번째 값을 100으로 기준잡고 정규화"""
    if not data or data[0] == 0:
        return data
    base = data[0]
    return [(val / base) * 100 for val in data]


def calculate_returns(data: List[float]) -> List[float]:
    """변화율 (수익률) 계산, 첫 값은 0"""
    if not data:
        return []
    returns = [0.0]
    for i in range(1, len(data)):
        prev = data[i-1]
        if prev == 0:
            returns.append(0.0)
        else:
            returns.append((data[i] - prev) / prev * 100)
    return returns


def analyze_correlation(series_a: List[Dict[str, Any]], series_b: List[Dict[str, Any]], value_key: str = "close") -> Dict[str, Any]:
    """
    두 시계열 데이터를 날짜 기준으로 Join 하고 상관관계를 분석합니다.
    """
    # 1. Join on date
    dict_b = {item["time"]: item[value_key] for item in series_b}
    
    joined_dates = []
    values_a = []
    values_b = []
    
    for item in series_a:
        date = item["time"]
        if date in dict_b:
            joined_dates.append(date)
            values_a.append(item[value_key])
            values_b.append(dict_b[date])
            
    if len(joined_dates) < 3:
        return {
            "error": "Not enough overlapping data points (minimum 3 required)."
        }
        
    # Calculate basic correlation
    pearson = calculate_pearson(values_a, values_b)
    spearman = calculate_spearman(values_a, values_b)
    
    # Calculate returns correlation
    returns_a = calculate_returns(values_a)
    returns_b = calculate_returns(values_b)
    pearson_returns = calculate_pearson(returns_a, returns_b)
    
    return {
        "n_observations": len(joined_dates),
        "dates": joined_dates,
        "values_a_raw": values_a,
        "values_b_raw": values_b,
        "values_a_normalized": normalize_series(values_a),
        "values_b_normalized": normalize_series(values_b),
        "pearson_correlation": round(pearson, 4),
        "spearman_correlation": round(spearman, 4),
        "pearson_correlation_returns": round(pearson_returns, 4),
        "warning": "상관관계는 인과관계를 의미하지 않습니다. 결측치나 시차(Lag) 문제가 존재할 수 있습니다."
    }

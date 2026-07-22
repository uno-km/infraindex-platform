import pytest
from apps.worker.adapters.vast_ai.parser import VastAiParser

def test_vast_ai_parser_valid_data():
    raw_data = [
        {
            "machine_id": 12345,
            "gpu_name": "RTX 4090",
            "num_gpus": 1,
            "dph_base": 0.45
        }
    ]
    
    result = VastAiParser.parse(raw_data)
    
    assert len(result) == 1
    assert result[0]["provider"] == "vast-ai"
    assert result[0]["machine_type"] == "1x RTX 4090"
    assert result[0]["hourly_price"] == 0.45
    assert result[0]["raw_offer_id"] == "12345"

def test_vast_ai_parser_missing_fields():
    raw_data = [
        {
            "machine_id": 12345,
            # Missing gpu_name
            "dph_base": 0.45
        }
    ]
    
    result = VastAiParser.parse(raw_data)
    assert len(result) == 0

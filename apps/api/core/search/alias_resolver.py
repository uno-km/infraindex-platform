from typing import Optional

class AliasResolver:
    # A simplified dictionary for Phase 9 vertical slice.
    # In production, this would be backed by an `AliasDictionary` DB table.
    ALIAS_MAP = {
        "에이치백": "H100",
        "에이치 백": "H100",
        "에이치100": "H100",
        "H백": "H100",
        "에이백": "A100",
        "에이100": "A100",
        "오공구공": "5090",
        "사공구공": "4090",
        "엘사십에스": "L40S"
    }
    
    @classmethod
    def resolve(cls, query: str) -> str:
        """
        Resolves Korean pronunciation and typos to canonical model names.
        """
        normalized_query = query.replace(" ", "")
        
        for k, v in cls.ALIAS_MAP.items():
            if k in normalized_query:
                return v
                
        return query

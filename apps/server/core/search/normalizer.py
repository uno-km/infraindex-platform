import re
import unicodedata

class QueryNormalizer:
    @staticmethod
    def normalize(query: str) -> str:
        """
        Applies Unicode normalization, removes noise characters,
        and standardizes spacing for GPU searches.
        (e.g., "h!)) " -> "H")
        """
        if not query:
            return ""
            
        # 1. Unicode NFKC normalization
        query = unicodedata.normalize("NFKC", query)
        
        # 2. Uppercase
        query = query.upper()
        
        # 3. Remove non-alphanumeric (except some safe symbols like -, _)
        query = re.sub(r'[^A-Z0-9\-\_가-힣\s]', '', query)
        
        # 4. Collapse whitespace
        query = re.sub(r'\s+', ' ', query).strip()
        
        return query

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class QuarantineService:
    @staticmethod
    def inspect(raw_data: List[Dict[str, Any]]) -> dict:
        """
        Inspects normalized data for quality issues before insertion.
        Returns a dictionary with 'passed' and 'quarantined' lists.
        """
        passed = []
        quarantined = []
        
        for item in raw_data:
            issues = []
            
            # Rule 1: Negative Price
            if item.get("hourly_price", 0) < 0:
                issues.append("negative_price")
                
            # Rule 2: Unreasonably high price (e.g. > $1000/hr)
            if item.get("hourly_price", 0) > 1000:
                issues.append("extreme_variance")
                
            if issues:
                quarantined.append({"data": item, "issues": issues})
                logger.warning(f"Item quarantined due to {issues}: {item}")
            else:
                passed.append(item)
                
        return {"passed": passed, "quarantined": quarantined}

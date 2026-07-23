import httpx
import feedparser
import logging
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ArXivCrawler:
    """
    arXiv API Crawler
    """
    BASE_URL = "https://export.arxiv.org/api/query"
    
    # Define primary search categories and keywords related to AI/Semiconductor
    SEARCH_QUERIES = [
        "cat:cs.AI",
        "cat:cs.LG",
        "cat:cs.CV",
        "all:semiconductor",
        "all:\"large language model\"",
        "all:\"transformer architecture\"",
        "all:\"NVIDIA GPU\""
    ]

    async def fetch_recent(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch recent papers from arXiv based on predefined queries.
        """
        all_papers = []
        # Join queries with OR to get a comprehensive recent list
        # ArXiv API uses +OR+
        query = "+OR+".join(self.SEARCH_QUERIES)
        
        params = {
            "search_query": query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": max_results
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                
                # Parse atom feed
                feed = feedparser.parse(response.text)
                
                for entry in feed.entries:
                    paper = self._parse_entry(entry)
                    if paper:
                        all_papers.append(paper)
                        
        except Exception as e:
            logger.error(f"[ArXivCrawler] Failed to fetch recent papers: {e}")
            
        return all_papers

    def _parse_entry(self, entry) -> Dict[str, Any]:
        """
        Convert feedparser entry to a structured dictionary.
        """
        try:
            # ArXiv ID is usually in the format: http://arxiv.org/abs/2501.12345v1
            # We want just 'arxiv:2501.12345'
            raw_id = entry.id.split('/abs/')[-1].split('v')[0]
            external_id = f"arxiv:{raw_id}"
            
            # Authors
            authors = [author.name for author in entry.authors] if hasattr(entry, 'authors') else []
            
            # Categories
            categories = [tag['term'] for tag in entry.tags] if hasattr(entry, 'tags') else []
            primary_category = categories[0] if categories else None
            
            # Published Date
            # format: 2023-10-23T18:24:23Z
            published_at = None
            if hasattr(entry, 'published'):
                published_at = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ").date()
            
            # PDF Link
            pdf_url = None
            for link in entry.links:
                if link.get('title') == 'pdf':
                    pdf_url = link.href
                    break
            
            # Build metadata JSON
            metadata = {
                "authors": authors,
                "abstract": entry.summary.replace('\n', ' ').strip(),
                "url": entry.link,
                "pdf_url": pdf_url,
                "categories": categories,
            }
            
            return {
                "external_id": external_id,
                "title": entry.title.replace('\n', ' ').strip(),
                "published_at": published_at,
                "category": primary_category,
                "metadata_json": metadata
            }
            
        except Exception as e:
            logger.warning(f"[ArXivCrawler] Error parsing entry {getattr(entry, 'id', 'unknown')}: {e}")
            return None

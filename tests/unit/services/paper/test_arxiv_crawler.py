import pytest
import datetime
from unittest.mock import patch, MagicMock

from apps.batch.services.paper.crawler_arxiv import ArXivCrawler

@pytest.mark.asyncio
async def test_fetch_recent_arxiv_papers():
    crawler = ArXivCrawler()
    
    with patch('feedparser.parse') as mock_parse:
        mock_feed = MagicMock()
        mock_entry = MagicMock()
        mock_entry.id = "http://arxiv.org/abs/2501.12345v1"
        mock_entry.published = "2025-01-20T18:24:23Z"
        mock_entry.title = "Dummy AI Paper"
        mock_entry.summary = "This is a dummy abstract."
        
        mock_author = MagicMock()
        mock_author.name = "John Doe"
        mock_entry.authors = [mock_author]
        
        mock_link_html = MagicMock()
        mock_link_html.get.return_value = None
        mock_link_html.href = "http://arxiv.org/abs/2501.12345v1"
        
        mock_link_pdf = MagicMock()
        mock_link_pdf.get.side_effect = lambda k: "pdf" if k == "title" else None
        mock_link_pdf.href = "http://arxiv.org/pdf/2501.12345v1"
        
        mock_entry.links = [mock_link_html, mock_link_pdf]
        
        mock_tag = MagicMock()
        # mock_tag is a dict-like object in feedparser, so we can mock __getitem__
        mock_entry.tags = [{'term': 'cs.AI'}]
        
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed
        
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_response = MagicMock()
            mock_response.text = "dummy_atom"
            mock_response.raise_for_status = MagicMock()
            mock_get.return_value.__aenter__.return_value = mock_response
            
            papers = await crawler.fetch_recent(max_results=1)
            
            assert len(papers) == 1
            assert papers[0]["external_id"] == "arxiv:2501.12345"
            assert papers[0]["title"] == "Dummy AI Paper"
            assert papers[0]["category"] == "cs.AI"
            assert papers[0]["published_at"] == datetime.date(2025, 1, 20)
            assert papers[0]["metadata_json"]["pdf_url"] == "http://arxiv.org/pdf/2501.12345v1"
            assert "John Doe" in papers[0]["metadata_json"]["authors"]

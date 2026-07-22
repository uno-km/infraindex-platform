import pytest
from apps.worker.providers.vast import VastCrawler
from apps.worker.providers.runpod import RunpodCrawler
from apps.worker.providers.aws import AWSCrawler

def test_crawler_factory_compliance():
    """
    Ensures all crawler implementations strictly comply with the BaseProviderCrawler contract
    and return the correct provider slugs.
    """
    vast = VastCrawler()
    assert vast.provider_slug == "vast-ai"
    assert hasattr(vast, "fetch_raw_data")
    assert hasattr(vast, "parse_instances")
    
    runpod = RunpodCrawler()
    assert runpod.provider_slug == "runpod"
    assert hasattr(runpod, "normalize_pricing")

    aws = AWSCrawler()
    assert aws.provider_slug == "aws"
    assert hasattr(aws, "execute_pipeline")

@pytest.mark.asyncio
async def test_stealth_http_client():
    """Test the Stealth HTTP Client instantiation."""
    from apps.worker.providers.common.http_client import StealthHttpClient
    
    client = StealthHttpClient()
    httpx_client = await client.get_client()
    headers = httpx_client.headers
    assert "user-agent" in headers
    # Ensure it's spoofing a real browser
    assert "Mozilla" in headers["user-agent"]

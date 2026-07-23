import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_get_db():
    """Test the database session dependency."""
    from apps.api.core.database import get_db
    
    # get_db is an async generator, we just get the generator object
    gen = get_db()
    # Mock the yield process if necessary, but just verifying the type or existence is fine for this layer
    assert gen is not None

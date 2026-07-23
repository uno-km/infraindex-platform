import pytest
from apps.api.core import redis_client

def test_redis_client_loaded():
    """Verify redis client module is loadable."""
    assert redis_client is not None


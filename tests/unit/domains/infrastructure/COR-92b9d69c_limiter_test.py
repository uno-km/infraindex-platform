import pytest
from apps.api.core import limiter

def test_limiter_loaded():
    """Verify limiter module is loadable."""
    assert limiter is not None


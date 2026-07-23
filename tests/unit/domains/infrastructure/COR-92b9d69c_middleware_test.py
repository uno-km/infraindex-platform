import pytest
from apps.api.core import middleware

def test_middleware_loaded():
    """Verify middleware module is loadable."""
    assert middleware is not None


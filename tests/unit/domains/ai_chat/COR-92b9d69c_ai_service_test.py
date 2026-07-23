import pytest
from apps.api.core import ai_service

def test_ai_service_loaded():
    """Verify AI service module is loadable."""
    assert ai_service is not None


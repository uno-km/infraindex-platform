import pytest
from apps.api.core import traffic_service

def test_traffic_service_loaded():
    """Verify traffic service module is loadable."""
    assert traffic_service is not None


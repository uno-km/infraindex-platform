import pytest
from apps.api.core import data_service

def test_data_service_loaded():
    """Verify data service module is loadable."""
    assert data_service is not None


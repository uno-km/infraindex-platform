import pytest
from apps.api.core.config import settings

def test_settings_loaded():
    """Test if configuration settings are loaded properly."""
    assert settings is not None
    assert hasattr(settings, "PROJECT_NAME")
    assert hasattr(settings, "DATABASE_URL") or hasattr(settings, "async_database_uri")

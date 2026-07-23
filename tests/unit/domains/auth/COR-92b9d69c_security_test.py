import pytest
from apps.api.core.security import get_password_hash, verify_password, create_access_token

def test_password_hashing():
    """Test password hashing and verification."""
    password = "supersecretpassword"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_create_access_token():
    """Test JWT access token creation."""
    subject_id = "12345-uuid"
    token = create_access_token(subject=subject_id)
    
    assert isinstance(token, str)
    assert len(token) > 0

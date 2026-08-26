import pytest
from app.utils.auth import get_password_hash, verify_password, create_access_token, decode_token
from app.models.user import TokenData

def test_password_hashing():
    password = "testpassword123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_token_creation_and_decoding():
    data = {"sub": "user123", "email": "test@example.com", "role": "user"}
    token = create_access_token(data)
    assert isinstance(token, str)
    
    decoded = decode_token(token)
    assert isinstance(decoded, TokenData)
    assert decoded.user_id == "user123"
    assert decoded.email == "test@example.com"
    assert decoded.role == "user"

def test_invalid_token():
    with pytest.raises(Exception):
        decode_token("invalid.token.string")

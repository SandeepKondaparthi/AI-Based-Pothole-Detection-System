import pytest
from datetime import timedelta
from fastapi import HTTPException
from app.utils.auth import (
    get_password_hash, verify_password, create_access_token, 
    create_refresh_token, decode_token, get_current_user, require_authority
)
from app.models.user import TokenData
from unittest.mock import MagicMock

def test_password_flow():
    pwd = "SecretPassword123"
    hashed = get_password_hash(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_tokens_flow():
    data = {"sub": "user_id_123", "email": "test@test.com", "role": "admin"}
    
    # Access Token
    token = create_access_token(data, expires_delta=timedelta(minutes=10))
    decoded = decode_token(token)
    assert decoded.user_id == "user_id_123"
    
    # Refresh Token
    refresh = create_refresh_token(data)
    decoded_refresh = decode_token(refresh)
    assert decoded_refresh.email == "test@test.com"

def test_decode_token_missing_fields():
    # Create a token with missing fields manually if possible or mock jwt.decode
    import jose.jwt as jwt
    from app.config import settings
    
    payload = {"sub": "123"} # Missing email and role
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    with pytest.raises(HTTPException) as exc:
        decode_token(token)
    assert exc.value.status_code == 401
    assert "Invalid token payload" in exc.value.detail

def test_decode_token_invalid():
    with pytest.raises(HTTPException) as exc:
        decode_token("not.a.token")
    assert exc.value.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user():
    credentials = MagicMock()
    credentials.credentials = create_access_token({"sub": "1", "email": "a@b.com", "role": "user"})
    user = await get_current_user(credentials)
    assert user.user_id == "1"

@pytest.mark.asyncio
async def test_require_authority_success():
    user = TokenData(user_id="1", email="a@b.com", role="authority")
    result = await require_authority(user)
    assert result == user

@pytest.mark.asyncio
async def test_require_authority_fail():
    user = TokenData(user_id="1", email="a@b.com", role="citizen")
    with pytest.raises(HTTPException) as exc:
        await require_authority(user)
    assert exc.value.status_code == 403

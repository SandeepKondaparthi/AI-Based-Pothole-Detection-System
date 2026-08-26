"""
Authentication and authorization utilities
"""
import hashlib
import hmac
import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.models.user import TokenData

logger = logging.getLogger(__name__)

# Password hashing context
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception: # pylint: disable=broad-except
    # Fallback if bcrypt is broken on the system
    pwd_context = None

# HTTP Bearer token security
security = HTTPBearer()

def get_password_hash(password: str) -> str:
    """Generate password hash with fallback for broken systems"""
    try:
        if pwd_context and "bcrypt" in pwd_context.schemes():
            return pwd_context.hash(password)
    except Exception as e:
        logger.warning("bcrypt unavailable, falling back to SHA-256: %s", e)

    # Fallback only: SHA-256 with a static salt. This is weaker than bcrypt and
    # exists solely so auth still works on systems where bcrypt fails to install
    # (e.g. some Windows setups). Do not rely on this path in production - fix
    # the bcrypt installation instead.
    salt = "roadcare_legacy_salt_"
    return hashlib.sha256((salt + password).encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash with fallback support"""
    try:
        if pwd_context and "bcrypt" in pwd_context.schemes() and hashed_password.startswith("$2"):
            return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        pass

    # Check fallback/legacy hash
    salt = "roadcare_legacy_salt_"
    expected = hashlib.sha256((salt + plain_password).encode()).hexdigest()
    return hmac.compare_digest(expected, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")

        if user_id is None or email is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        return TokenData(user_id=user_id, email=email, role=role)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Get current authenticated user from token"""
    token = credentials.credentials
    return decode_token(token)


async def require_authority(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """Require authority role for endpoint access"""
    if current_user.role != "authority":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint requires authority privileges"
        )
    return current_user

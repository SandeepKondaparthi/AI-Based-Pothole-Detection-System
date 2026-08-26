"""
User data models
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            )
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return ObjectId(v)
        raise ValueError("Invalid ObjectId type")


class UserBase(BaseModel):
    """Base user model"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    role: str = Field(..., pattern="^(user|authority)$")


class UserCreate(UserBase):
    """User creation model"""
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str


class UserInDB(UserBase):
    """User model as stored in database"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserResponse(UserBase):
    """User response model (without sensitive data)"""
    id: str = Field(..., alias="_id")
    created_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenWithUser(BaseModel):
    """JWT token response with user data"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    id: str
    name: str
    email: str
    phone: str
    role: str


class TokenData(BaseModel):
    """JWT token payload data"""
    user_id: str
    email: str
    role: str

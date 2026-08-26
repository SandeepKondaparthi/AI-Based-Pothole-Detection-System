"""
Authentication routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.config.database import get_database
from app.models.user import UserCreate, UserLogin, UserResponse, Token, UserInDB, TokenWithUser
from app.utils.auth import get_password_hash, verify_password, create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Register a new user

    - **name**: User's full name
    - **email**: Valid email address
    - **phone**: Phone number
    - **role**: Either 'user' or 'authority'
    - **password**: Minimum 6 characters
    """
    # Check if email already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = get_password_hash(user_data.password)

    # Create user document
    user = UserInDB(
        **user_data.dict(exclude={"password"}),
        hashed_password=hashed_password
    )

    # Insert into database
    result = await db.users.insert_one(user.dict(by_alias=True, exclude={"id"}))
    user.id = result.inserted_id

    # Return user response
    return UserResponse(
        _id=str(user.id),
        **user.dict(exclude={"id", "hashed_password"})
    )


@router.post("/login", response_model=TokenWithUser)
async def login(
    credentials: UserLogin,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Login with email and password

    Returns JWT access and refresh tokens with user data
    """
    # Find user by email
    user = await db.users.find_one({"email": credentials.email})

    # Check for testing credentials if user not found in DB
    is_test_user = False
    test_user_data = None

    from app.config import settings
    if not user and credentials.email == settings.TEST_AUTHORITY_EMAIL:
        if credentials.password == settings.TEST_AUTHORITY_PASSWORD:
            is_test_user = True
            test_user_data = {
                "_id": "000000000000000000000000",
                "name": "System Administrator",
                "email": settings.TEST_AUTHORITY_EMAIL,
                "phone": "0000000000",
                "role": "authority",
                "hashed_password": "" # Not used for test user
            }
            user = test_user_data

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Verify password if not a test user
    if not is_test_user and not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create tokens
    token_data = {
        "sub": str(user["_id"]),
        "email": user["email"],
        "role": user["role"]
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenWithUser(
        access_token=access_token,
        refresh_token=refresh_token,
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        phone=user["phone"],
        role=user["role"]
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_database),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get current authenticated user information"""
    from app.utils.auth import get_current_user

    # This endpoint would need the current user dependency
    # For now, returning a stub
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint under construction"
    )

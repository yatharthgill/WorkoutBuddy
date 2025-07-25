
from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate
from app.db.mongodb import db
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.auth import create_jwt_token
from app.utils.api_response import api_response

router = APIRouter()
users_collection = db["users"]

@router.post("/register")
async def register_user(payload: UserCreate):
    # Check if user already exists
    if await users_collection.find_one({"email": payload.email}):
        return api_response(
            message="Email already registered",
            status=status.HTTP_409_CONFLICT
        )

    # Create new user
    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        oauth_provider="local"
    )

    insert_result = await users_collection.insert_one(user.model_dump(by_alias=True))

    return api_response(
        message="User registered successfully",
        status=status.HTTP_201_CREATED,
        data={"user_id": str(insert_result.inserted_id)}
    )

@router.post("/login")
async def login_user(payload: LoginRequest):
    user = await users_collection.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password_hash"]):
        return api_response(
            message="Invalid email or password",
            status=status.HTTP_401_UNAUTHORIZED
        )
    token = create_jwt_token(data={"sub": user["email"]})

    return api_response(
        message="Login successful",
        status=status.HTTP_200_OK,
        data={
            "user_id": str(user["_id"]),
            "access_token": token,
            "token_type": "bearer"
        }
    )

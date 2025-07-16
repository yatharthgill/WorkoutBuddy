from fastapi import APIRouter
from app.api.routes import auth
from app.api.routes import users

api_router = APIRouter()
api_router.include_router(auth.router ,tags=["Auth"])
api_router.include_router(users.router ,tags=["Users"])

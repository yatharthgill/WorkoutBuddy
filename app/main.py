from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware  # ✅ Required for OAuth sessions
import os
from dotenv import load_dotenv

from app.api.api_v1 import api_router
from app.config.settings import settings
from app.db.mongodb import db
from app.api.routes import oauth

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Initialize FastAPI app
app = FastAPI(title=settings.APP_NAME)

# ✅ Add SessionMiddleware for OAuth session support
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "super-secret-key-change-this")  # use strong key in production
)

# ✅ Include routes
app.include_router(api_router, prefix="/api")
app.include_router(oauth.router, prefix="/auth", tags=["OAuth"])

# ✅ Database connection check
@app.on_event("startup")
async def test_db_connection():
    try:
        await db.command("ping")
        print("✅ Connected to MongoDB Atlas")
    except Exception as e:
        print("❌ Failed to connect to MongoDB Atlas:", e)

# ✅ Default root route
@app.get("/")
async def root():
    return {"message": "Welcome to Workout Buddy API!"}

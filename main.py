from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from core.database import get_db,Base,engine,SessionLocal
from core.config import settings
from sqlalchemy import text
from fastapi import FastAPI,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from starlette.staticfiles import StaticFiles
import os
# from src.routes.private import userPrivateRouter
from app.middleware.auth_middleware import jwt_auth
# from .routes.common import commonRouter
# from .routes.route import MlRouter
# from .config.db import Base,engine
from app.api.v1.routes_users import userRouter
from app.api.v1.routes_whatsapp import whatsappRouter
security = HTTPBearer()

import multiprocessing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App starting...")
    
    # ✅ Only for development (not production)
    if settings.ENV == "dev":
        Base.metadata.create_all(bind=engine)
    
    yield
    print("🛑 App shutting down...")



app = FastAPI(lifespan=lifespan)

# 📁 Static files
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# 🌍 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Routes
app.include_router(userRouter, prefix="/api/v1/user", tags=["User-API"])
app.include_router(whatsappRouter, prefix="/api/v1/whatsapp", tags=["WhatsApp-API"])


# Include routers
# app.include_router(commonRouter,prefix="/api",tags = ["File-Upload"])
# app.include_router(MlRouter, prefix="/api/ml", tags=["ML-API"])
# run.include_router(userRouter, prefix="/api/user", tags=["User-API"])
# app.include_router(userPrivateRouter, prefix="/api/user/private", tags=["User-Private-API"], dependencies=[Depends(security), Depends(jwt_auth)])
print(f" server runing on port : http://localhost:{settings.PORT}/docs")


@app.get("/health")
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except:
        return {"status": "unhealthy"}
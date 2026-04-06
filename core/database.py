from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# 🔥 Use your DB URL (SQLite / PostgreSQL)
DATABASE_URL = settings.SQLITE
# DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
# ✅ Production-ready engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # auto reconnect
    pool_size=5,
    max_overflow=10,
    echo=False            # ❌ disable logs in production
)

# ✅ Session (per request)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ Base for models
Base = declarative_base()


# ✅ Dependency (IMPORTANT)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL from environment variable, use SQLite as fallback for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./kuakuaqun.db")

print(f"Database mode: {'Production' if 'postgres' in DATABASE_URL else 'Local development'}")

# Modify URL for asyncpg if using PostgreSQL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

print(f"Connecting to database: {DATABASE_URL}")

# Configure engine based on database type
if "sqlite" in DATABASE_URL:
    # SQLite specific configuration
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True
    )

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

async def get_db():
    async with async_session() as session:
        yield session 
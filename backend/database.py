from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL from environment variable, use SQLite as fallback for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./kuakuaqun.db")

# Get deployment environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
print(f"Running in {ENVIRONMENT} environment")

# Handle different database configurations
if ENVIRONMENT == "production":
    # PythonAnywhere MySQL configuration
    DB_USERNAME = os.getenv("MYSQL_USERNAME")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
    DB_HOST = os.getenv("MYSQL_HOST")
    DB_NAME = os.getenv("MYSQL_DATABASE")
    
    if all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME]):
        DATABASE_URL = f"mysql+aiomysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    else:
        raise ValueError("Missing MySQL configuration in production environment")

print(f"Database mode: {'Production' if ENVIRONMENT == 'production' else 'Local development'}")
print(f"Connecting to database: {DATABASE_URL.replace(os.getenv('MYSQL_PASSWORD', ''), '****') if 'mysql' in DATABASE_URL else DATABASE_URL}")

# Configure engine based on database type
if "sqlite" in DATABASE_URL:
    # SQLite specific configuration
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False}
    )
else:
    # MySQL/PostgreSQL configuration
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
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
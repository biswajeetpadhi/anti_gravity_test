from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Default to SQLite for local development
DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"

# Create Async Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session Local
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session

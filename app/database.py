import os
from dotenv import load_dotenv  # Load environment variables from a .env file
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession  # Async database engine and session
from sqlalchemy.orm import sessionmaker, declarative_base  # ORM utilities
from typing import AsyncGenerator  # Type hint for async generator

# Load environment variables from the .env file
load_dotenv()

# Database connection URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an asynchronous database engine
engine = create_async_engine(
    DATABASE_URL,  # Database connection string
    echo=True,  # Enable SQL query logging
    pool_size=10,  # Number of connections in the pool
    max_overflow=20,  # Maximum number of connections beyond the pool size
    pool_timeout=30,  # Timeout for acquiring a connection
    pool_recycle=3600  # Recycle connections after this many seconds
)

# Create a session factory for database interactions
SessionLocal = sessionmaker(
    bind=engine,  # Bind the session to the async engine
    class_=AsyncSession,  # Use asynchronous sessions
    expire_on_commit=False  # Prevent automatic expiration of objects after commit
)

# Base class for ORM models
Base = declarative_base()

# Dependency for FastAPI routes to provide a database session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session for FastAPI routes.
    - Yields an AsyncSession instance.
    - Ensures the session is properly closed after use.
    """
    async with SessionLocal() as session:
        yield session
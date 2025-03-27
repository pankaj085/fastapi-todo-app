from fastapi import FastAPI
from .routers import tasks  # Import the tasks router
from .database import engine, Base  # Import database engine and Base for ORM
from contextlib import asynccontextmanager  # Import async context manager for lifespan

# Define the lifespan of the application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan function to handle application startup and shutdown events.
    - Creates all database tables on startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create database tables
    yield  # Yield control back to the application

# Initialize the FastAPI application
app = FastAPI(
    title="To-Do API",  # Title of the API
    description="A complete To-Do application with FastAPI and PostgreSQL",  # Description of the API
    version="1.0.0",  # Version of the API
    lifespan=lifespan  # Attach the lifespan function
)

# Include the tasks router
app.include_router(tasks.router)  # Add the tasks endpoints to the application

# Health check endpoint
@app.get("/health", tags=["monitoring"])
def health_check():
    """
    Health check endpoint to verify if the application is running.
    - Returns a JSON response with the status of the application.
    """
    return {"status": "healthy"}
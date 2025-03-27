import asyncio  # Import asyncio for running asynchronous functions
from app.database import engine, Base  # Import database engine and Base for ORM

# Define an asynchronous function to create database tables
async def create_tables():
    """
    Creates all database tables defined in the ORM models.
    - Uses the SQLAlchemy engine to execute the table creation commands.
    """
    async with engine.begin() as conn:  # Begin an asynchronous database connection
        await conn.run_sync(Base.metadata.create_all)  # Create all tables defined in Base

# Entry point of the script
if __name__ == "__main__":
    # Run the create_tables function asynchronously
    asyncio.run(create_tables())
    print("Tables created successfully")  # Print a success message after table creation
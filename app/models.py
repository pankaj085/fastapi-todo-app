from sqlalchemy import Column, Integer, String, Boolean, DateTime, Index  # Import SQLAlchemy column types and utilities
from sqlalchemy.sql import func  # Import SQL functions for default timestamps
from .database import Base  # Import the Base class for ORM models

# Define the Task model
class Task(Base):
    __tablename__ = "tasks"  # Name of the database table
    __table_args__ = (
        Index('ix_task_completed', 'completed'),  # Index on the 'completed' column for faster queries
    )

    # Columns in the tasks table
    id = Column(Integer, primary_key=True, index=True)  # Primary key with an index for faster lookups
    title = Column(String(100), nullable=False)  # Task title, required, max length 100 characters
    description = Column(String(500))  # Task description, optional, max length 500 characters
    completed = Column(Boolean, default=False)  # Boolean flag for task completion, defaults to False
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Auto-set timestamp when task is created
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # Auto-update timestamp when task is modified
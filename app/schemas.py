from pydantic import BaseModel  # Base class for Pydantic models
from typing import Optional, List  # Type hints for optional and list fields
from datetime import datetime  # For datetime fields

# Base schema for tasks
class TaskBase(BaseModel):
    title: str  # Task title, required
    description: Optional[str] = None  # Task description, optional
    completed: bool = False  # Task completion status, defaults to False

# Schema for creating tasks
class TaskCreate(BaseModel):
    title: str  # Task title, required
    description: Optional[str] = None  # Task description, optional

# Schema for updating tasks
class TaskUpdate(BaseModel):
    title: Optional[str] = None  # Task title, optional
    description: Optional[str] = None  # Task description, optional
    completed: Optional[bool] = None  # Task completion status, optional

# Schema for returning a single task
class TaskResponse(BaseModel):
    id: int  # Task ID
    title: str  # Task title
    description: str  # Task description
    completed: bool  # Task completion status
    created_at: datetime  # Timestamp when the task was created
    updated_at: datetime  # Timestamp when the task was last updated

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models

# Schema for listing multiple tasks
class TaskListResponse(BaseModel):
    count: int  # Total number of tasks
    tasks: List[TaskResponse]  # List of tasks
    
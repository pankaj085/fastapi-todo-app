from sqlalchemy import select, text  # Import SQLAlchemy utilities for queries and raw SQL execution
from sqlalchemy.ext.asyncio import AsyncSession  # Import asynchronous database session
from . import models, schemas  # Import ORM models and Pydantic schemas
from typing import Optional  # For optional return types
from datetime import datetime  # For handling timestamps

# Create Task
async def create_task(db: AsyncSession, task: schemas.TaskCreate) -> models.Task:
    """
    Create a new task in the database.
    - Accepts a TaskCreate schema and inserts it into the database.
    - Sets created_at and updated_at timestamps.
    """
    db_task = models.Task(**task.model_dump())  # Map schema data to the Task model
    db_task.created_at = datetime.utcnow()  # Set creation timestamp
    db_task.updated_at = datetime.utcnow()  # Set update timestamp
    db.add(db_task)  # Add the task to the session
    await db.commit()  # Commit the transaction
    await db.refresh(db_task)  # Refresh the task instance with the latest data
    return db_task  # Return the created task

# Read single task
async def get_task(db: AsyncSession, task_id: int) -> Optional[models.Task]:
    """
    Retrieve a single task by its ID.
    - Returns the task if found, otherwise None.
    """
    result = await db.execute(
        select(models.Task).filter(models.Task.id == task_id)  # Query for the task by ID
    )
    return result.scalars().first()  # Return the first result or None

# Read all tasks
async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Retrieve all tasks with pagination.
    - Supports skipping and limiting the number of results.
    """
    result = await db.execute(
        select(models.Task).offset(skip).limit(limit)  # Query with pagination
    )
    return result.scalars().all()  # Return all matching tasks as a list

# Update task
async def update_task(db: AsyncSession, task_id: int, task_update: schemas.TaskUpdate) -> Optional[models.Task]:
    """
    Update an existing task by its ID.
    - Accepts a TaskUpdate schema and updates only the provided fields.
    - Updates the updated_at timestamp.
    """
    db_task = await get_task(db, task_id)  # Retrieve the task by ID
    if db_task:
        update_data = task_update.model_dump(exclude_unset=True)  # Get only the fields to update
        for key, value in update_data.items():
            setattr(db_task, key, value)  # Update the task fields
        db_task.updated_at = datetime.utcnow()  # Update the timestamp
        await db.commit()  # Commit the transaction
        await db.refresh(db_task)  # Refresh the task instance with the latest data
    return db_task  # Return the updated task or None if not found

# Delete task
async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """
    Delete a task by its ID.
    - Returns True if the task was deleted, otherwise False.
    """
    db_task = await get_task(db, task_id)  # Retrieve the task by ID
    if db_task:
        await db.delete(db_task)  # Delete the task
        await db.commit()  # Commit the transaction
        return True  # Task was deleted
    return False  # Task not found

# Reset task ID sequence
async def reset_task_id_sequence(db: AsyncSession):
    """
    Reset the ID sequence for the tasks table.
    - Ensures new tasks start with ID 1 after all tasks are deleted.
    """
    await db.execute(text("ALTER SEQUENCE tasks_id_seq RESTART WITH 1"))  # Reset the sequence
    await db.commit()  # Commit the transaction
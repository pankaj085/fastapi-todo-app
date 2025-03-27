from fastapi import APIRouter, Depends, HTTPException, status  # FastAPI utilities for routing and dependency injection
from sqlalchemy.ext.asyncio import AsyncSession  # Async database session
from sqlalchemy import text  # For executing raw SQL queries
from typing import List  # Type hint for lists
from .. import schemas, crud  # Import schemas and CRUD operations
from ..database import get_db  # Dependency to get the database session

# Initialize the router for task-related endpoints
router = APIRouter(
    prefix="/tasks",  # Base URL for all task-related endpoints
    tags=["tasks"],  # Tag for grouping endpoints in the API documentation
    responses={404: {"description": "Task not found"}}  # Default response for 404 errors
)

# Endpoint to create a new task
@router.post(
    "/",
    response_model=schemas.TaskResponse,  # Response schema
    status_code=status.HTTP_201_CREATED,  # HTTP status code for successful creation
    summary="Create a new task"  # Short description for API documentation
)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new task with the following properties:
    - **title**: Required, the task title
    - **description**: Optional, task description
    - **completed**: Optional, defaults to False
    """
    return await crud.create_task(db, task)  # Call the create_task function from CRUD

# Endpoint to list all tasks with pagination
@router.get(
    "/",
    response_model=schemas.TaskListResponse,  # Response schema for multiple tasks
    summary="List all tasks"  # Short description for API documentation
)
async def list_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all tasks with pagination:
    - **skip**: Number of tasks to skip (for pagination)
    - **limit**: Maximum number of tasks to return
    """
    tasks = await crud.get_tasks(db, skip=skip, limit=limit)  # Call the get_tasks function from CRUD
    return {"tasks": tasks, "count": len(tasks)}  # Return tasks and their count

# Endpoint to delete all tasks and reset the ID sequence
@router.delete(
    "/reset",
    status_code=status.HTTP_204_NO_CONTENT,  # HTTP status code for successful deletion
    summary="Delete all tasks and reset ID sequence"  # Short description for API documentation
)
async def reset_tasks(db: AsyncSession = Depends(get_db)):
    """
    Delete all tasks and reset the ID sequence.
    """
    await db.execute(text("DELETE FROM tasks"))  # Delete all tasks from the database
    await crud.reset_task_id_sequence(db)  # Reset the ID sequence
    return None

# Endpoint to retrieve a single task by its ID
@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse,  # Response schema for a single task
    summary="Get a single task"  # Short description for API documentation
)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific task by its ID.
    """
    task = await crud.get_task(db, task_id=task_id)  # Call the get_task function from CRUD
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # HTTP status code for not found
            detail="Task not found"  # Error message
        )
    return task

# Endpoint to update all fields of a task
@router.put(
    "/{task_id}",
    response_model=schemas.TaskResponse,  # Response schema for the updated task
    summary="Update a task (full update)"  # Short description for API documentation
)
async def update_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update all fields of a task.
    Note: For partial updates, use PATCH.
    """
    updated_task = await crud.update_task(db, task_id=task_id, task_update=task)  # Call the update_task function from CRUD
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # HTTP status code for not found
            detail="Task not found"  # Error message
        )
    return updated_task

# Endpoint to partially update a task
@router.patch(
    "/{task_id}",
    response_model=schemas.TaskResponse,  # Response schema for the updated task
    summary="Partially update a task"  # Short description for API documentation
)
async def patch_task(task_id: int, task: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    """
    Partially update a task (only the provided fields will be updated).
    """
    existing_task = await crud.get_task(db, task_id=task_id)  # Call the get_task function from CRUD
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # HTTP status code for not found
            detail="Task not found"  # Error message
        )
    
    # Update only the fields that were provided
    update_data = task.dict(exclude_unset=True)
    updated_task = await crud.update_task(db, task_id=task_id, task_update=schemas.TaskUpdate(**update_data))  # Call the update_task function from CRUD
    return updated_task

# Endpoint to delete a task by its ID
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,  # HTTP status code for successful deletion
    summary="Delete a task"  # Short description for API documentation
)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a task by its ID.
    """
    if not await crud.delete_task(db, task_id=task_id):  # Call the delete_task function from CRUD
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # HTTP status code for not found
            detail="Task not found"  # Error message
        )
    return None
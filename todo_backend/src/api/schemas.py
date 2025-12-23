"""
schemas.py - Pydantic models for Todo API.
"""

from pydantic import BaseModel, Field
from typing import Optional

# PUBLIC_INTERFACE
class TaskIn(BaseModel):
    """Schema for incoming (create/update) tasks."""
    title: str = Field(..., description="The content/title of the task")
    completed: Optional[bool] = Field(False, description="Whether the task is completed")

# PUBLIC_INTERFACE
class Task(TaskIn):
    """Schema for outgoing (read) tasks, includes ID."""
    id: int = Field(..., description="The unique identifier of the task")

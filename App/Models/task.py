from ast import If
from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional
from enum import Enum


#An Enum lets you create a fixed list of allowed choices.
#Think of it as saying:
#"Priority can only be low, medium, or high."
#Nothing else.
#Enum → create a set of choices.
#str → store the values as strings.

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskCreate(BaseModel):
    user_id: Optional[str]= None
    title: str
    description: str

    priority: Priority= Priority.MEDIUM
    #This means:
    #If user doesn't provide priority → use medium as default priority
    #If user provides priority → validate it
    #If user provides invalid priority → raise validation error 
    #    (e.g. "Priority must be one of: low, medium, high")

    status: Status= Status.PENDING

    due_date: datetime | None = None
   # This means: due_date can be a datetime object or None
   # If user doesn't provide due_date → use None as default value
   # If user provides due_date → validate it as a datetime
   # If user provides invalid due_date → raise validation error
   # (e.g. "due_date must be a valid datetime in ISO format")
   #     2026-06-10T18:00:00
   #     2026 - 06 - 10 T 18 : 00 : 00
    #    │      │    │     │    │    │
    #    │      │    │     │    │    └── seconds
    #    │      │    │     │    └─────── minutes
    #    │      │    │     └──────────── hours
    #    │      │    └────────────────── day
    #    │      └─────────────────────── month
    #    └────────────────────────────── year

   # So:

   #     2026-06-10T18:00:00
   #     means:
   #     June 10, 2026 at 6:00 PM

    completed_at: Optional[datetime] = None

    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

class TaskUpdate(BaseModel):
    user_id: Optional[str]= None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: str
    user_id: Optional[str]= None
    title: str
    description: str
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    #Use priority,status due_date and completed_at as optional fields in response model, because they may not be set for all tasks.
    #For example, when a task is first created, it may not have a due_date or completed_at, because the user may not have provided those fields when creating the task.
    #By making them optional, we can still return a valid response for tasks that don't have those fields set, without causing validation errors.
    #It is need when we views all tasks.Some tasks may not have priority, status, due_date or completed_at set, but we still want to return those tasks in the response without causing validation errors.
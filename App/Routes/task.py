from ast import If
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status,Depends
from App.Models.task import TaskCreate, TaskResponse, TaskUpdate, Priority, Status
from App.utils.authentication import get_current_user
from App.CRUD.task import create_task, delete_task, filter_task, get_dashboard_data, get_task_by_id, get_tasks, paginate_tasks, search_tasks, sort_tasks, update_task

router = APIRouter(prefix="/tasks")
@router.post("/", response_model=dict)

async def create_task_api(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    task_data = task.model_dump()
    task_data["user_id"] = current_user["id"]
    new_task = TaskCreate(**task_data)
    await create_task(new_task)
    return {"message": "Task created successfully"}



@router.get("/filters", response_model=list[TaskResponse] )#eg filter URL: http://127.0.0.1:8000/tasks/filters?priority=high&status=pending&due_date=2026-07-08
async def filter_tasks(priority: Optional[Priority] = None, status: Optional[Status] = None, due_date: Optional[datetime] = None, current_user: dict = Depends(get_current_user)):
    tasks = await filter_task({})
    #We fetch all tasks from the database, and then we filter them in Python based on the provided filters (priority, status, due_date) and the current user's ID.

    filtered_tasks = []
    for task in tasks:
        if task["user_id"] != current_user["id"]:
            continue 
        #If task.get("user_id") != current_user["id"], continue runs and skips the remaining code for that task.
        #If task.get("user_id") == current_user["id"], continue does not run, and execution continues to the code below it.
        #So, if the task's user_id does not match the current user's ID, we skip that task and move on to the next one.
        #'continue' means: skip the rest of the code for this iteration of the loop, and move on to the next iteration.
        
        if priority and task.get("priority") != priority:
            continue
        #If priority is provided in the URL, and the task's priority does not match the provided priority, we skip that task and move on to the next one.
        #If priority is not provided in the URL, we do not filter by priority, and we include all tasks regardless of their priority.
        
        if status and task.get("status") != status:
            continue

        if due_date:
            task_due = task.get("due_date")

            if not task_due:
                continue

            if task_due.date() != due_date.date():
                continue

            #task_due=2026-07-08 18:30:00 / URL given due_date=2026-07-08
            #task_due.date()=2026-07-08 / URL given due_date.date()=2026-07-08 → match
            #Only compare the date part of due_date, not the time part, because user may only provide date in URL, without time.
            #If we compared the full datetime, then it would not match, because the time part would be different (task_due has time, but URL given due_date does not have time, 
            # so it would default to 00:00:00, which would not match the actual due_date of the task).

        filtered_tasks.append(TaskResponse(id=str(task["_id"]), **task))
    return filtered_tasks

#router.get("/filters") must be defined before router.get("/{task_id}"),
# because if we define router.get("/{task_id}") first,
# then the URL /tasks/filters would match the route /tasks/{task_id} with task_id="filters", which is not what we want.
# By defining router.get("/filters") first, we ensure that the URL /tasks/filters matches the correct route for filtering tasks, and not the route for getting a task by ID.

@router.get("/search", response_model=list[TaskResponse])#eg search URL: http://127.0.0.1:8000/tasks/search?keyword=test
async def search_tasks_api(keyword: str, current_user: dict = Depends(get_current_user)):
    tasks = await search_tasks(keyword)
    searched_tasks = []
    for task in tasks:
        if task["user_id"] != current_user["id"]:
            continue
        searched_tasks.append(TaskResponse(id=str(task["_id"]), **task))
    return searched_tasks

@router.get("/sort", response_model=list[TaskResponse])#eg sort URL: http://127.0.0.1:8000/tasks/sort?field=due_date&order=1
async def sort_tasks_api(field: str, order: int, current_user: dict = Depends(get_current_user)):
    tasks = await sort_tasks(field, order)
    sorted_tasks = []
    for task in tasks:
        if task["user_id"] != current_user["id"]:
            continue
        sorted_tasks.append(TaskResponse(id=str(task["_id"]), **task))
    return sorted_tasks

@router.get("/paginate", response_model=list[TaskResponse])#eg pagination URL: http://
async def paginate_tasks_api(page: int, limit: int, current_user: dict = Depends(get_current_user)):
    skip = (page - 1) * limit
    #If page=1 and limit=10 → skip=0 → return tasks 1-10
    #If page=2 and limit=10 → skip=10 → return tasks 11-20
    #If page=3 and limit=10 → skip=20 → return tasks 21-30

    tasks = await paginate_tasks(skip, limit)
    paginated_tasks = []
    for task in tasks:
        if task["user_id"] != current_user["id"]:
            continue
        paginated_tasks.append(TaskResponse(id=str(task["_id"]), **task))
    return paginated_tasks

@router.get("/dashboard", response_model=dict) #eg dashboard URL: http://127.0.0.1:8000/tasks/dashboard
async def dashboard(current_user: dict = Depends(get_current_user)):
    tasks = await get_dashboard_data({"user_id": current_user["id"]})
    total_tasks = 0
    completed_tasks = 0
    pending_tasks = 0
    in_progress_tasks = 0
    for task in tasks:
        if task["user_id"] != current_user["id"]:
            continue
        total_tasks += 1
        if task.get("status") == Status.COMPLETED:
            completed_tasks += 1
        elif task.get("status") == Status.PENDING:
            pending_tasks += 1
        elif task.get("status") == Status.IN_PROGRESS:
            in_progress_tasks += 1
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "in_progress_tasks": in_progress_tasks
    }

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
    task = await get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse(
        id=str(task["_id"]),

        #user_id=task["user_id"]
        user_id=task.get("user_id"),
        title=task.get("title"),
        description=task.get("description"),
        priority=task.get("priority"),
        status=task.get("status"),
        due_date=task.get("due_date"),
        completed_at=task.get("completed_at"),
        created_at=task["created_at"],
        updated_at=task["updated_at"]

        #user_id=task["user_id"],This line can crash.
        #A safer version is: user_id=task.get("user_id"),
        #until all your documents contain a user_id.
    )

@router.get("/", response_model=list[TaskResponse])
async def get_tasks_api(current_user: dict = Depends(get_current_user)):
    tasks = await get_tasks()
    return [TaskResponse(id=str(task["_id"]), **task) for task in tasks]

@router.put("/{task_id}", response_model=TaskUpdate)
async def update_task_api(task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user)):
    task_update_data = task_update.model_dump(exclude_unset=True)
    task_update_data["user_id"] = current_user["id"]

    task_update_data["updated_at"] = datetime.utcnow() 
    # Update the updated_at field to current time, so we can track when the task was last updated.
    # Without this, the updated_at field would not change when we update the task, which would make it harder to track when the task was last updated.

    if task_update.status == Status.COMPLETED:
        task_update_data["completed_at"] = datetime.utcnow()
    else:
        task_update_data["completed_at"] = None
        # If the status is not completed, we set completed_at to None, because the task is not completed yet.
        # This way we can track when the task was completed, and also when it was marked as not completed again.

    updated_task = TaskUpdate(**task_update_data)
    updated = await update_task(task_id, updated_task)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update task")
    return updated_task

@router.delete("/{task_id}")
async def delete_task_api(task_id: str):
    deleted = await delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete task")
    return {"message": "Task deleted successfully"} 


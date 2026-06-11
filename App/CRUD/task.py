from App.Routes.db import db
from App.Models.task import TaskCreate, TaskUpdate
from bson import ObjectId

tasks_collection = db["tasks"]

async def create_task(task: TaskCreate):
    task_dict = task.model_dump()
    result = await tasks_collection.insert_one(task_dict)
    return True

async def get_task_by_id(task_id: str):
    return await tasks_collection.find_one({"_id": ObjectId(task_id)})

async def get_tasks():
    return await tasks_collection.find().to_list(length=100)

async def get_dashboard_data(data: dict):
    return await tasks_collection.find(data).to_list(length=100)


async def filter_task(filters:dict):
    return await tasks_collection.find(filters).to_list(length=100)

async def search_tasks(keyword: str):
    return await tasks_collection.find(
        {"$or": [
            {"title": {"$regex": keyword, "$options": "i"}},
            {"description": {"$regex": keyword, "$options": "i"}}
        ]}
    ).to_list(length=100)
#$or means:Condition A OR Condition B
#If either one is true, MongoDB returns the document.
#without $or, MongoDB would return documents that match both conditions,
#which is not what we want for a search functionality.
#We want to return documents that match either condition, so we use $or.
#eg- If user searches for "meeting", we want to return tasks that have "meeting" in the title OR in the description,
#not just those that have "meeting" in both title and description.
#options: "i" means case-insensitive search, so it will match "Meeting", "meeting", "MEETING", etc.

async def sort_tasks(field: str, order: int):
    return await tasks_collection.find().sort(field, order).to_list(length=100)
#field: The field to sort by (e.g. "due_date", "priority", "created_at", etc.)
#order: The sort order (1 for ascending, -1 for descending)

async def paginate_tasks(skip: int, limit: int):
    return await tasks_collection.find().skip(skip).limit(limit).to_list(length=limit)
#skip: The number of documents to skip (for pagination)
#limit: The maximum number of documents to return (for pagination)

async def update_task(task_id: str, task: TaskUpdate):
    result = await tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": task.model_dump(exclude_unset=True)},
        #exclude_unset=True means: Only include fields that have been set (not None) .
        #eg- If user only provides title → only update title, not other fields like description or priority. 
        #Only update fields that user has provided, not all fields.Without exclude_unset=True → it would set all fields, even those not provided by user, to None. """
    )
    return result.modified_count > 0

async def delete_task(task_id: str):
    result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return result.deleted_count > 0
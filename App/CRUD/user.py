from App.Models.user import UserRegister, UserLogin
from App.Routes.db import db
from App.utils.password import hash

users_collection=db["users"]

async def create_user(user: UserRegister):
    hashed_password = hash(user.password)
    user_dict = user.model_dump()
    user_dict["password"] = hashed_password
    result = await users_collection.insert_one(user_dict)
    return str(result.inserted_id)

async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

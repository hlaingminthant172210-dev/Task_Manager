from fastapi import FastAPI
from App.Routes import user
from App.Routes import task

app=FastAPI()
app.include_router(user.router)
app.include_router(task.router)
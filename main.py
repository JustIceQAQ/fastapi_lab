from fastapi import FastAPI

from apps.routers import root_routers
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(root_routers)
app.mount("/static", StaticFiles(directory="static"), name="static")

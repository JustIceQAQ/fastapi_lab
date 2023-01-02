from fastapi import FastAPI

from apps.routers import root_routers

app = FastAPI()

app.include_router(root_routers)

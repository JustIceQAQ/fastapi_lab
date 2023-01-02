from fastapi import APIRouter

from apps.users.api import user_router

root_routers = APIRouter(prefix="/api")

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(user_router)

root_routers.include_router(v1_router)


@root_routers.get("/")
async def root():
    return {"message": "Hello World"}


@root_routers.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

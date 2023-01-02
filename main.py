from fastapi import FastAPI

from apps.routers import root_routers
from db.database import engine
from apps.users import models

app = FastAPI()

app.include_router(root_routers)

models.Base.metadata.create_all(bind=engine)




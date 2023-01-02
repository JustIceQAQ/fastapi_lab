from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, WebSocket, Request
from fastapi.templating import Jinja2Templates

from starlette.websockets import WebSocketDisconnect

from apps.irises import schemas, crud
from apps.irises.ws import IrisesConnectionManager
from db.database import get_db

irises_router = APIRouter(prefix="/irises", tags=["Irises"])
irises_manager = IrisesConnectionManager()


def get_all_irises():
    db = next(get_db())
    return [schemas.Irises.from_orm(iris).dict() for iris in crud.get_irises(db)]


@irises_router.get(
    "/",
    response_model=List[schemas.Irises],
    status_code=status.HTTP_200_OK)
async def get_irises(db: Session = Depends(get_db)):
    return crud.get_irises(db)


@irises_router.get(
    "/{iris_id}",
    response_model=schemas.Irises,
    status_code=status.HTTP_200_OK)
async def get_iris(iris_id: int, db: Session = Depends(get_db)):
    return crud.get_iris(db, iris_id=iris_id)


@irises_router.post(
    "/",
    response_model=schemas.Irises,
    status_code=status.HTTP_201_CREATED)
async def post_iris(iris: schemas.IrisBase, db: Session = Depends(get_db)):
    data = crud.create_iris(db, iris.dict())
    await irises_manager.broadcast(get_all_irises())
    return data


@irises_router.put(
    "/{iris_id}",
    response_model=schemas.Irises,
    status_code=status.HTTP_200_OK)
async def put_iris(iris_id: int, iris_data: schemas.IrisBase, db: Session = Depends(get_db)):
    data = crud.update_iris(db, iris_id=iris_id, iris_data=iris_data.dict())
    await irises_manager.broadcast(get_all_irises())
    return data


@irises_router.patch(
    "/{iris_id}",
    response_model=schemas.Irises,
    status_code=status.HTTP_200_OK)
async def patch_iris(iris_id: int, iris_data: schemas.PatchIris, db: Session = Depends(get_db)):
    data = crud.update_iris(db, iris_id=iris_id, iris_data=iris_data.dict(exclude_unset=True))
    await irises_manager.broadcast(get_all_irises())
    return data


@irises_router.delete(
    "/{iris_id}",
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_iris(iris_id: int, db: Session = Depends(get_db)):
    data = crud.delete_iris(db, iris_id=iris_id)
    await irises_manager.broadcast(get_all_irises())
    return data


templates = Jinja2Templates(directory="templates")


@irises_router.get("/farm/")
async def farm_iris(request: Request):
    return templates.TemplateResponse("farm.html", {"request": request})


@irises_router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await irises_manager.connect(websocket)
    try:
        while True:
            await irises_manager.broadcast(get_all_irises())
            await websocket.receive_text()
    except WebSocketDisconnect:
        irises_manager.disconnect(websocket)

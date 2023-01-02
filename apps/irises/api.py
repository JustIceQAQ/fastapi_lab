from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from apps.irises import schemas, crud
from db.database import get_db

irises_router = APIRouter(prefix="/irises", tags=["Irises"])


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
    return crud.create_iris(db, iris.dict())


@irises_router.put(
    "/{iris_id}",
    response_model=schemas.Irises,
    status_code=status.HTTP_200_OK)
async def put_iris(iris_id: int, iris_data: schemas.IrisBase, db: Session = Depends(get_db)):
    return crud.update_iris(db, iris_id=iris_id, iris_data=iris_data.dict())


@irises_router.patch(
    "/{iris_id}",
    response_model=schemas.Irises,
    status_code=status.HTTP_200_OK)
async def patch_iris(iris_id: int, iris_data: schemas.PatchIris, db: Session = Depends(get_db)):
    return crud.update_iris(db, iris_id=iris_id, iris_data=iris_data.dict(exclude_unset=True))


@irises_router.delete(
    "/{iris_id}",
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_iris(iris_id: int, db: Session = Depends(get_db)):
    return crud.delete_iris(db, iris_id=iris_id)

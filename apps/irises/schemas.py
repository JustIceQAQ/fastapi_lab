from typing import Union

from pydantic import BaseModel


class IrisBase(BaseModel):
    sepal_length: int
    sepal_width: int
    petal_length: int
    petal_width: int
    class_type: str


class Irises(IrisBase):
    id: int

    class Config:
        orm_mode = True


class PatchIris(BaseModel):
    sepal_length: Union[int, None] = None
    sepal_width: Union[int, None] = None
    petal_length: Union[int, None] = None
    petal_width: Union[int, None] = None
    class_type: Union[str, None] = None

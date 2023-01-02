from typing import Dict, Optional, Any

from sqlalchemy.orm import Session

from apps.irises.models import Irises


def get_irises(db: Session):
    return db.query(Irises).all()


def get_iris(db: Session, iris_id: int) -> Optional[Irises]:
    return db.query(Irises).where(Irises.id == iris_id).first()


def create_iris(db: Session, iris: Dict):
    db_iris = Irises(**iris)
    db.add(db_iris)
    db.commit()
    db.refresh(db_iris)
    return db_iris


def update_iris(db: Session, iris_id: int, iris_data: Dict):
    db_iris = get_iris(db, iris_id)
    if db_iris:
        for key, value in iris_data.items():
            if hasattr(db_iris, key):
                setattr(db_iris, key, value)
        db.merge(db_iris)
    db.commit()
    db.refresh(db_iris)
    return db_iris


def delete_iris(db: Session, iris_id: int):
    db_iris = get_iris(db, iris_id)
    if db_iris:
        db.delete(db_iris)
    db.commit()

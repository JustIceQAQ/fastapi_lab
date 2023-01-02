from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from db.database import Base, engine


class Irises(Base):
    __tablename__ = "Irises"
    id = Column(Integer, primary_key=True, index=True)
    sepal_length = Column(Integer)
    sepal_width = Column(Integer)
    petal_length = Column(Integer)
    petal_width = Column(Integer)
    class_type = Column(String(100))

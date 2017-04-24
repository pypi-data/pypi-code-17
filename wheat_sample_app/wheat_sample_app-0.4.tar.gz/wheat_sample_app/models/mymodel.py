from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

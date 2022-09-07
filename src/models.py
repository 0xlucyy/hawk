from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from src.exceptions import DatabaseError
from sqlalchemy import (
    create_engine,
    Column,
    String,
    ForeignKey,
    BigInteger, 
    Integer,
    LargeBinary,
    Text,
    DateTime,
    JSON,
    UniqueConstraint,
    Boolean
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
)
from typing import (
    Dict,
    List
)


BASE = declarative_base()




def init_db(uri):
    engine = create_engine(uri,  echo=True, future=True)
    BASE.metadata.create_all(bind=engine)
    return engine
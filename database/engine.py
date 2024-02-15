from fastapi import Depends
from typing import Annotated, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

from core.config import settings


engine = create_engine(settings.DATABASE_URL)

Base = declarative_base()


def get_db() -> Generator:
    with Session(engine) as session:
        yield session


# db dependency
SessionDep = Annotated[Session, Depends(get_db)]

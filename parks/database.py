from parks.config import db_url
from sqlmodel import create_engine, Session
from typing import Generator

engine = create_engine(db_url, echo=False)


async def session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


from typing import Annotated, Generator
from fastapi import Depends, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# 定义重用的类型别名
DBDep = Annotated[Session, Depends(get_db)]

from datetime import datetime, timezone
from typing import Any, TypeVar

from sqlalchemy import Column, DateTime, Integer
import sqlalchemy as sa
import sqlalchemy.orm as so

T = TypeVar("T", bound="BaseDBModel")

class BaseDBModel():
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

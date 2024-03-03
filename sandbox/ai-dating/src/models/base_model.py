from datetime import datetime, timezone

from src.app import db

import sqlalchemy as sa
import sqlalchemy.orm as so

class BaseModel(db.Model):
    __abstract__ = True
    created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))

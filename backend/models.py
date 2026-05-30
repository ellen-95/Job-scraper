from datetime import datetime

from sqlalchemy import DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    company: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    location: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    date_posted: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    url: Mapped[str] = mapped_column(String(768), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

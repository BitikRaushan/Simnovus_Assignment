from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    last_heartbeat: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    cpu_usage: Mapped[float | None] = mapped_column(Float, nullable=True)
    signal_strength: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def is_online(self, timeout_seconds: int = 30) -> bool:
        if self.last_heartbeat is None:
            return False

        heartbeat = self.last_heartbeat
        if heartbeat.tzinfo is None:
            heartbeat = heartbeat.replace(tzinfo=timezone.utc)

        age = (datetime.now(timezone.utc) - heartbeat).total_seconds()
        return age <= timeout_seconds

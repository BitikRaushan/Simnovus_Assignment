from datetime import datetime
from pydantic import BaseModel, ConfigDict

class DeviceCreate(BaseModel):
    id: str
    name: str

class HeartbeatRequest(BaseModel):
    timestamp: datetime | None = None
    status: str = "OK"
    cpu_usage: float | None = None
    signal_strength: float | None = None

class DeviceResponse(BaseModel):
    id: str
    name: str
    status: str
    last_heartbeat: datetime | None
    last_reported_status: str | None = None
    cpu_usage: float | None = None
    signal_strength: float | None = None

class HeartbeatResponse(BaseModel):
    message: str
    device: DeviceResponse

class FleetSummary(BaseModel):
    total: int
    online: int
    offline: int

import os
from datetime import datetime, timezone
from pathlib import Path
from fastapi.responses import FileResponse

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Device
from .schemas import (
    DeviceCreate,
    DeviceResponse,
    FleetSummary,
    HeartbeatRequest,
    HeartbeatResponse,
)

TIMEOUT_SECONDS = int(os.getenv("HEARTBEAT_TIMEOUT_SECONDS", "30"))

app = FastAPI(
    title="Mini Device Fleet Monitor",
    description="REST API for monitoring simulated device heartbeats.",
    version="1.0.0",
)



Base.metadata.create_all(bind=engine)

#Dashboard

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(STATIC_DIR / "index.html")

def to_response(device: Device) -> DeviceResponse:
    return DeviceResponse(
        id=device.id,
        name=device.name,
        status="ONLINE" if device.is_online(TIMEOUT_SECONDS) else "OFFLINE",
        last_heartbeat=device.last_heartbeat,
        last_reported_status=device.last_status,
        cpu_usage=device.cpu_usage,
        signal_strength=device.signal_strength,
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post(
    "/devices",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    device = Device(id=payload.id, name=payload.name)
    db.add(device)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="device already exists",
        )

    db.refresh(device)
    return to_response(device)

@app.post(
    "/devices/{device_id}/heartbeat",
    response_model=HeartbeatResponse,
)
def receive_heartbeat(
    device_id: str,
    payload: HeartbeatRequest,
    db: Session = Depends(get_db),
):
    device = db.get(Device, device_id)

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="device not found",
        )

    device.last_heartbeat = payload.timestamp or datetime.now(timezone.utc)
    device.last_status = payload.status
    device.cpu_usage = payload.cpu_usage
    device.signal_strength = payload.signal_strength

    db.commit()
    db.refresh(device)

    return {
        "message": "heartbeat received",
        "device": to_response(device),
    }

@app.get("/devices", response_model=list[DeviceResponse])
def list_devices(db: Session = Depends(get_db)):
    devices = db.scalars(select(Device).order_by(Device.id)).all()
    return [to_response(device) for device in devices]

@app.get("/devices/{device_id}", response_model=DeviceResponse)
def get_device(device_id: str, db: Session = Depends(get_db)):
    device = db.get(Device, device_id)

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="device not found",
        )

    return to_response(device)

@app.get("/summary", response_model=FleetSummary)
def fleet_summary(db: Session = Depends(get_db)):
    devices = db.scalars(select(Device)).all()
    online = sum(device.is_online(TIMEOUT_SECONDS) for device in devices)

    return FleetSummary(
        total=len(devices),
        online=online,
        offline=len(devices) - online,
    )

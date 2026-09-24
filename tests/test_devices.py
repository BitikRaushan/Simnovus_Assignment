from datetime import datetime, timezone, timedelta

def test_register_device(client):
    response = client.post("/devices", json={
        "id": "device-01",
        "name": "Lab Device 01",
    })

    assert response.status_code == 201
    assert response.json()["id"] == "device-01"
    assert response.json()["status"] == "OFFLINE"

def test_heartbeat_handling(client):
    client.post("/devices", json={
        "id": "device-01",
        "name": "Lab Device 01",
    })

    response = client.post(
        "/devices/device-01/heartbeat",
        json={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "OK",
            "cpu_usage": 42,
            "signal_strength": -71,
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "heartbeat received"
    assert response.json()["device"]["status"] == "ONLINE"

def test_device_details(client):
    client.post("/devices", json={
        "id": "device-01",
        "name": "Lab Device 01",
    })

    response = client.get("/devices/device-01")

    assert response.status_code == 200
    assert response.json()["name"] == "Lab Device 01"

def test_device_becomes_offline_after_30_seconds(client):
    client.post("/devices", json={
        "id": "device-01",
        "name": "Lab Device 01",
    })

    old_timestamp = (
        datetime.now(timezone.utc) - timedelta(seconds=31)
    ).isoformat()

    client.post(
        "/devices/device-01/heartbeat",
        json={
            "timestamp": old_timestamp,
            "status": "OK",
        },
    )

    response = client.get("/devices/device-01")

    assert response.status_code == 200
    assert response.json()["status"] == "OFFLINE"

def test_summary(client):
    for i in range(2):
        client.post("/devices", json={
            "id": f"device-{i}",
            "name": f"Device {i}",
        })

    client.post(
        "/devices/device-0/heartbeat",
        json={"timestamp": datetime.now(timezone.utc).isoformat()},
    )

    response = client.get("/summary")
    data = response.json()

    assert data["total"] == 2
    assert data["online"] == 1
    assert data["offline"] == 1

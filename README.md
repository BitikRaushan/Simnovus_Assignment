# Mini Device Fleet Monitor

A lightweight device fleet monitoring application built with **Python, FastAPI, PostgreSQL, and SQLAlchemy**.

The application simulates a fleet of devices that periodically send heartbeat information to a REST API. The backend stores the latest device information in PostgreSQL and determines whether each device is **ONLINE** or **OFFLINE** based on the time since its most recent heartbeat.

A simple browser-based dashboard is also included for monitoring the devices and viewing their current status and telemetry information.

---

## 1. What the Project Does

The Mini Device Fleet Monitor provides a small backend system for monitoring connected devices.

The system supports:

- Registering devices
- Receiving device heartbeats
- Storing device information in PostgreSQL
- Tracking the latest heartbeat time
- Monitoring CPU usage
- Monitoring signal strength
- Automatically determining ONLINE/OFFLINE status
- Viewing all devices
- Viewing individual device details
- Viewing fleet-level statistics
- Simulating multiple devices
- Stopping an individual simulated device
- Automatically detecting when a device becomes offline
- Testing the backend using automated tests
- Interactive API testing through Swagger UI
- A simple web dashboard for monitoring the fleet

---

## 2. Design / Architecture

The application consists of four main parts:

1. FastAPI backend
2. PostgreSQL database
3. Python device simulator
4. HTML/CSS/JavaScript monitoring dashboard

### Architecture

```text
                    +----------------------+
                    |   Device Simulator   |
                    |       Python         |
                    +----------+-----------+
                               |
                               | HTTP POST
                               | Heartbeat
                               v
                    +----------------------+
                    |       FastAPI        |
                    |      REST API        |
                    +----------+-----------+
                               |
                         SQLAlchemy ORM
                               |
                               v
                    +----------------------+
                    |      PostgreSQL      |
                    |       Database       |
                    +----------------------+

                               ^
                               |
                            REST API
                               |
                    +----------+-----------+
                    |    Web Dashboard     |
                    |    HTML/CSS/JS       |
                    +----------------------+
```

### Data Flow

```text
Device Simulator
       |
       | POST /devices/{id}/heartbeat
       v
    FastAPI
       |
       | SQLAlchemy
       v
   PostgreSQL
       |
       | GET /devices
       | GET /summary
       | GET /devices/{id}
       v
   Web Dashboard
```

### Heartbeat Status Logic

```text
Current Time - Last Heartbeat <= 30 seconds
                         |
                         v
                      ONLINE
```

If the difference is greater than 30 seconds, the device is:

```text
OFFLINE
```

The status is calculated when device information is requested, so a separate background process is not required just to mark devices offline.

---

## 3. Prerequisites

Install:

- Python 3.10 or newer
- PostgreSQL
- pip
- Git

No Node.js or separate frontend server is required because the dashboard uses HTML, CSS, and JavaScript and is served by FastAPI.

### Tech Stack

**Backend**
- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy

**Database**
- PostgreSQL

**Simulator**
- Python
- Requests

**Frontend**
- HTML5
- CSS3
- JavaScript

**Testing**
- Pytest

**API Documentation**
- OpenAPI / Swagger UI
- ReDoc

---

## 4. How to Build the Application

Clone the repository:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd device-fleet-monitor-fastapi
```

Create a virtual environment.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### PostgreSQL Configuration

Create the database:

```bash
createdb device_fleet
```

Or:

```bash
psql postgres
```

Then:

```sql
CREATE DATABASE device_fleet;
```

Exit:

```sql
\q
```

Copy the environment template:

```bash
cp .env.example .env
```

Configure `.env`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/device_fleet
```

Replace the username and password with the local PostgreSQL credentials.

Do not commit `.env` to GitHub.

---

## 5. How to Run the Application

Activate the environment:

```bash
source .venv/bin/activate
```

Start FastAPI:

```bash
python run.py
```

The API runs at:

```text
http://127.0.0.1:8000
```

### Web Dashboard

Open:

```text
http://127.0.0.1:8000/
```

The dashboard shows:

- Total devices
- Online devices
- Offline devices
- Device IDs
- Device names
- Status
- Last heartbeat
- CPU usage
- Signal strength

### Swagger

Open:

```text
http://127.0.0.1:8000/docs
```

Alternative:

```text
http://127.0.0.1:8000/redoc
```

---

## 6. How to Run the Simulator

The simulator represents external devices.

By default it runs five devices:

```text
device-01
device-02
device-03
device-04
device-05
```

In another terminal:

```bash
source .venv/bin/activate
python simulator/simulator.py
```

Example output:

```text
device-01 heartbeat: 200
device-02 heartbeat: 200
device-03 heartbeat: 200
device-04 heartbeat: 200
device-05 heartbeat: 200
```

A `200` response means the heartbeat was accepted successfully.

### Stop an Individual Device

Example:

```bash
python simulator/simulator.py --stop device-03
```

The selected device stops sending heartbeats while the other devices continue.

After more than 30 seconds without a heartbeat, `device-03` becomes:

```text
OFFLINE
```

This demonstrates the automatic timeout mechanism.

---

## 7. How to Run the Tests

Run:

```bash
pytest -q
```

The tests cover:

- Device registration
- Heartbeat processing
- Device retrieval
- Device details
- ONLINE status
- OFFLINE status after timeout
- Fleet summary
- API validation
- Error handling

---

## 8. Example API Requests

### Register a Device

```http
POST /devices
```

```json
{
  "id": "device-01",
  "name": "Lab Device 01"
}
```

### Send a Heartbeat

```http
POST /devices/device-01/heartbeat
```

```json
{
  "status": "OK",
  "cpu_usage": 42,
  "signal_strength": -71
}
```

### Get All Devices

```http
GET /devices
```

### Get Device Details

```http
GET /devices/device-01
```

### Get Fleet Summary

```http
GET /summary
```

Example:

```json
{
  "total": 5,
  "online": 4,
  "offline": 1
}
```

---

## 9. Assumptions

1. Device IDs are unique.
2. A device should be registered before sending heartbeats.
3. PostgreSQL is used for persistent storage.
4. The simulator represents external devices.
5. A device is ONLINE when its latest heartbeat is no more than 30 seconds old.
6. A device is OFFLINE when its latest heartbeat is more than 30 seconds old.
7. A device with no heartbeat is considered offline.
8. Heartbeats contain CPU usage and signal strength.
9. Authentication is outside the assignment scope.
10. The dashboard is intended for local monitoring and demonstration.

---

## 10. Known Limitations

- No authentication or API keys
- No MQTT/message broker
- No production rate limiting
- No heartbeat history
- No historical telemetry graphs
- No Alembic migrations
- Simple Python simulator
- Basic monitoring dashboard
- No production deployment configuration
- No advanced alerting
- PostgreSQL is expected to be available locally

These limitations keep the project small and focused on the assignment requirements.

---

## 11. What I Would Improve With One Additional Day

### 1. Device Authentication

Add API keys or token-based authentication.

### 2. Heartbeat History

Store historical heartbeat records to support uptime and telemetry analysis.

### 3. Better Dashboard

Add charts for CPU usage, signal strength, uptime, and heartbeat history.

### 4. Database Migrations

Add Alembic for proper schema migrations.

### 5. Containerization

Add Docker and Docker Compose for easier deployment.

### 6. Alerting

Notify operators when a device remains offline for a configurable period.

### 7. Structured Logging

Add structured application logging for debugging and production monitoring.

---

## API Endpoint Summary

| Method | Endpoint | Description |
|---|---|---|
| POST | `/devices` | Register a device |
| POST | `/devices/{id}/heartbeat` | Send device heartbeat |
| GET | `/devices` | List all devices |
| GET | `/devices/{id}` | Get device details |
| GET | `/summary` | Get fleet summary |
| GET | `/docs` | Swagger API documentation |
| GET | `/redoc` | ReDoc API documentation |

---

## Project Structure

```text
device-fleet-monitor-fastapi/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── simulator/
│   └── simulator.py
│
├── static/
│   └── index.html
│
├── tests/
│   └── ...
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

---

## Complete Local Demo

### Terminal 1

```bash
source .venv/bin/activate
python run.py
```

Open:

```text
http://127.0.0.1:8000/
```

### Terminal 2

```bash
source .venv/bin/activate
python simulator/simulator.py
```

The dashboard should show the simulated devices as ONLINE.

To demonstrate the offline mechanism:

```bash
python simulator/simulator.py --stop device-03
```

Wait for more than 30 seconds.

The dashboard should show:

```text
Total:    5
Online:   4
Offline:  1
```

with `device-03` marked OFFLINE.

---

## Use of AI

AI tools were used as development assistance for:

- Brainstorming project structure
- Reviewing API design
- Identifying edge cases
- Generating initial implementation ideas
- Reviewing test cases
- Improving documentation
- Debugging development issues

The final project was kept intentionally simple and focused on the assignment requirements.

The implementation was manually tested for:

- PostgreSQL connectivity
- Device registration
- Heartbeat processing
- Device status calculation
- 30-second timeout behaviour
- Individual device stopping
- Fleet summary
- Dashboard integration
- Swagger documentation
- Automated tests

AI-generated suggestions were reviewed before being incorporated.

---

## Quick Start

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd device-fleet-monitor-fastapi

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

createdb device_fleet

cp .env.example .env

python run.py
```

Open the dashboard:

```text
http://127.0.0.1:8000/
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

In another terminal:

```bash
source .venv/bin/activate
python simulator/simulator.py
```

Run tests:

```bash
pytest -q
```

---

## Summary

The **Mini Device Fleet Monitor** demonstrates how simulated devices communicate with a backend through REST APIs.

The project combines:

**Python + FastAPI + SQLAlchemy + PostgreSQL + HTML/CSS/JavaScript**

and demonstrates:

- REST API development
- Database persistence
- Device heartbeat monitoring
- Automatic ONLINE/OFFLINE detection
- Device simulation
- Individual device control
- Automated testing
- Interactive API documentation
- Browser-based monitoring

The architecture is intentionally simple so that the complete system can be understood, run, tested, and demonstrated locally.

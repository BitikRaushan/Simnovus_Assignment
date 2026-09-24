# Simnovus_Assignment
# Mini Device Fleet Monitor

A lightweight device fleet monitoring system built with **Python, FastAPI, PostgreSQL, and SQLAlchemy**.

The application simulates a fleet of devices that periodically send heartbeat data to a REST API. The backend stores device information in PostgreSQL and automatically determines whether a device is **ONLINE** or **OFFLINE** based on the freshness of its latest heartbeat.

A simple web dashboard is also included for monitoring the fleet through a browser.

---

## Features

- Register devices
- Receive device heartbeats
- Store device data in PostgreSQL
- Automatic ONLINE/OFFLINE status detection
- 30-second heartbeat timeout
- List all devices
- View individual device details
- Fleet-wide device summary
- Five-device Python simulator
- Stop an individual simulated device
- Real-time dashboard with automatic refresh
- CPU usage and signal strength monitoring
- REST API
- Swagger/OpenAPI documentation
- Automated backend tests

---

## Tech Stack

### Backend

- **Python** – Main programming language
- **FastAPI** – REST API framework
- **Uvicorn** – ASGI server
- **Pydantic** – Request and response validation
- **SQLAlchemy** – ORM and database interaction

### Database

- **PostgreSQL** – Persistent data storage

### Device Simulator

- **Python**
- **Requests** – HTTP communication with the FastAPI backend

### Frontend

- **HTML5**
- **CSS3**
- **JavaScript**

The frontend is intentionally lightweight and does not require React, Node.js, or a separate frontend server.

### Testing & Documentation

- **Pytest** – Automated testing
- **Swagger / OpenAPI** – Interactive API documentation

---

## Architecture

```text
                  +----------------------+
                  |   Device Simulator   |
                  |       Python         |
                  +----------+-----------+
                             |
                             | HTTP Heartbeat
                             v
                  +----------------------+
                  |       FastAPI        |
                  |      REST API        |
                  +----------+-----------+
                             |
                         SQLAlchemy
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


## Data Flow
Device Simulator
       |
       | POST heartbeat
       v
    FastAPI
       |
       | Store latest heartbeat
       v
   PostgreSQL
       |
       | GET device information
       v
   Dashboard
       |
       v
ONLINE / OFFLINE

## Project Structure
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

## Requirements
*Before running the project, make sure you have:
- Python 3.10+
- PostgreSQL
- pip

## installation

1. clone the repository
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd device-fleet-monitor-fastapi

2. Create a virtual environment
python3 -m venv .venv

3.Activate it
macOS / Linux
source .venv/bin/activate

windows

.venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5.PostgreSQL Setup
createdb device_fleet


## Running the Application
python run.py
The server will start at:
http://127.0.0.1:8000


## Web Dashboard
http://127.0.0.1:8000/



## Quick Start
# Clone repository
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd device-fleet-monitor-fastapi

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create PostgreSQL database
createdb device_fleet

# Configure environment
cp .env.example .env

# Start FastAPI
python run.py






## Project Summary
Mini Device Fleet Monitor demonstrates a complete device-monitoring workflow using:
Python + FastAPI + SQLAlchemy + PostgreSQL + HTML/CSS/JavaScript
The project focuses on:
- REST API design
- PostgreSQL persistence
- Device heartbeat monitoring
- Automatic 30-second timeout detection
- Device simulation
- Automated testing
- API documentation
- Simple browser-based monitoring
The architecture is intentionally small and understandable while covering the core requirements of a device fleet monitoring system.








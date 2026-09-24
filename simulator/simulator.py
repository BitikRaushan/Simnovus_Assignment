import argparse
import random
import threading
import time

import requests


BASE_URL = "http://127.0.0.1:8000"


def send_heartbeat(device_id):
    url = f"{BASE_URL}/devices/{device_id}/heartbeat"

    payload = {
        "status": "OK",
        "cpu_usage": random.randint(20, 80),
        "signal_strength": random.randint(-80, -60),
    }

    try:
        response = requests.post(url, json=payload)

        print(f"{device_id} heartbeat: {response.status_code}")

    except requests.RequestException as e:
        print(f"{device_id} error: {e}")


def device_loop(device_id, stopped_device):
    while True:

        # Don't send heartbeat for the selected stopped device
        if device_id != stopped_device:
            send_heartbeat(device_id)

        time.sleep(5)


def main():

    parser = argparse.ArgumentParser(
        description="Device Fleet Simulator"
    )

    parser.add_argument(
        "--stop",
        help="Stop heartbeat for a specific device, e.g. device-03",
        default=None
    )

    args = parser.parse_args()

    devices = [
        "device-01",
        "device-02",
        "device-03",
        "device-04",
        "device-05",
    ]

    if args.stop and args.stop not in devices:
        print(f"Unknown device: {args.stop}")
        print("Available devices:", ", ".join(devices))
        return

    print("Running 5 simulated devices.")
    print("Heartbeat interval: 5 seconds")

    if args.stop:
        print(f"STOPPED DEVICE: {args.stop}")
        print(f"{args.stop} will NOT send heartbeats.")

    print("Press Ctrl+C to stop the simulator.\n")

    threads = []

    for device_id in devices:

        thread = threading.Thread(
            target=device_loop,
            args=(device_id, args.stop),
            daemon=True
        )

        thread.start()

        threads.append(thread)

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("\nSimulator stopped.")


if __name__ == "__main__":
    main()
import os
import requests

# Grab env vars for DB URL
DB_API_URL = os.getenv("DB_API_URL", "http://db-api:8000")


def send_write_request(key: str, value: str) -> dict:
    response = requests.post(
        f"{DB_API_URL}/write",
        json={"key": key, "value": value},
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def send_retrieve_request(key: str) -> dict:
    response = requests.get(
        f"{DB_API_URL}/retrieve/{key}",
        timeout=5,
    )
    response.raise_for_status()
    return response.json()
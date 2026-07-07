"""API response handling and data export/import with JSON & CSV."""
import json
import csv
from pathlib import Path


def fetch_api_response() -> dict:
    return {"status": "ok", "data": {"users": [{"id": 1, "name": "Eleven", "powers": ["telekinesis", "scream"]}, {"id": 2, "name": "Mike", "powers": ["leadership"]}, {"id": 3, "name": "Dustin", "powers": ["intelligence", "wit"]}], "total": 3}}


def save_users_json(users: list, path: str) -> None:
    with open(path, "w") as f:
        json.dump(users, f, indent=2)


def users_to_csv(users: list, path: str) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "powers"])
        for u in users:
            writer.writerow([u["id"], u["name"], "; ".join(u["powers"])])


def csv_to_users(path: str) -> list:
    users = []
    with open(path) as f:
        for row in csv.DictReader(f):
            users.append({"id": int(row["id"]), "name": row["name"], "powers": row["powers"].split("; ")})
    return users


response = fetch_api_response()
users = response["data"]["users"]
save_users_json(users, "/tmp/users.json")
users_to_csv(users, "/tmp/users.csv")
reloaded = csv_to_users("/tmp/users.csv")
print("Reloaded:", json.dumps(reloaded, indent=2))
Path("/tmp/users.json").unlink()
Path("/tmp/users.csv").unlink()

"""Phase 05 — Practice Exercise Solutions."""
import csv
import json
import math
import random
import re
import shutil
import hashlib
import secrets
import uuid
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


def ex1_parse_ini():
    def parse_ini(path):
        config = {}
        current_section = None
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("[") and line.endswith("]"):
                    current_section = line[1:-1]
                    config[current_section] = {}
                elif "=" in line and current_section:
                    k, v = line.split("=", 1)
                    config[current_section][k.strip()] = v.strip()
        return config
    with open("/tmp/test.ini", "w") as f:
        f.write("[database]\nhost=localhost\nport=5432\n[app]\ndebug=true\n")
    result = parse_ini("/tmp/test.ini")
    assert result["database"]["host"] == "localhost"
    Path("/tmp/test.ini").unlink()
    print("1. INI parser: OK")


def ex2_dice_roller():
    def roll_dice(num=2, sides=6):
        rolls = [random.randint(1, sides) for _ in range(num)]
        return rolls, sum(rolls)
    rolls, total = roll_dice(3, 6)
    assert len(rolls) == 3
    assert sum(rolls) == total
    print("2. Dice roller: OK")


def ex3_meeting_scheduler():
    def find_slots(booked, duration, start_hour=9, end_hour=17):
        all_slots = []
        current = datetime(2024, 1, 1, start_hour, 0)
        end = datetime(2024, 1, 1, end_hour, 0)
        while current + timedelta(minutes=duration) <= end:
            slot_end = current + timedelta(minutes=duration)
            if not any(s <= current < e or s < slot_end <= e for s, e in booked):
                all_slots.append((current.strftime("%H:%M"), slot_end.strftime("%H:%M")))
            current += timedelta(minutes=30)
        return all_slots
    booked = [(datetime(2024, 1, 1, 10, 0), datetime(2024, 1, 1, 11, 0))]
    slots = find_slots(booked, 30)
    assert len(slots) > 0
    print("3. Meeting scheduler: OK")


def ex4_csv_aggregator():
    def aggregate_csv(in_path, out_path, group_by_col, value_col):
        totals = {}
        with open(in_path) as f:
            for row in csv.DictReader(f):
                key = row[group_by_col]
                totals[key] = totals.get(key, 0) + int(row[value_col])
        with open(out_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow([group_by_col, f"total_{value_col}"])
            for k, v in sorted(totals.items()):
                w.writerow([k, v])
    rows = [["dept", "sales"], ["A", "100"], ["B", "200"], ["A", "50"]]
    with open("/tmp/sales.csv", "w", newline="") as f:
        csv.writer(f).writerows(rows)
    aggregate_csv("/tmp/sales.csv", "/tmp/agg.csv", "dept", "sales")
    result = list(csv.DictReader(open("/tmp/agg.csv")))
    assert len(result) == 2
    Path("/tmp/sales.csv").unlink()
    Path("/tmp/agg.csv").unlink()
    print("4. CSV aggregator: OK")


def ex5_organize_by_date():
    def organize_by_date(directory):
        base = Path(directory)
        for f in base.iterdir():
            if f.is_file():
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                target = base / str(mtime.year) / f"{mtime.month:02d}"
                target.mkdir(parents=True, exist_ok=True)
                f.rename(target / f.name)
    tmp = Path("/tmp/org_test")
    tmp.mkdir(exist_ok=True)
    (tmp / "test.txt").write_text("test")
    organize_by_date(tmp)
    assert any(tmp.rglob("test.txt"))
    shutil.rmtree(tmp)
    print("5. Organize by date: OK")


def ex6_json_validator():
    def validate_users(json_path):
        with open(json_path) as f:
            users = json.load(f)
        required = {"id", "name", "email"}
        errors = []
        for i, user in enumerate(users):
            missing = required - set(user.keys())
            if missing:
                errors.append({"index": i, "missing": list(missing)})
        return errors
    users = [{"id": 1, "name": "Alice", "email": "a@b.com"}, {"id": 2, "name": "Bob"}]
    with open("/tmp/users.json", "w") as f:
        json.dump(users, f)
    errors = validate_users("/tmp/users.json")
    assert len(errors) == 1 and errors[0]["index"] == 1
    Path("/tmp/users.json").unlink()
    print("6. JSON validator: OK")


def ex7_regex_log_parser():
    def analyze_log(log_path):
        errors_by_module = Counter()
        error_msgs = Counter()
        hourly_counts = Counter()
        with open(log_path) as f:
            for line in f:
                m = re.match(r"(\d{4}-\d{2}-\d{2}) (\d{2}):\d{2}:\d{2} (ERROR|WARN|INFO) ([\w.]+): (.+)", line)
                if m:
                    _, hour, level, module, msg = m.groups()
                    hourly_counts[hour] += 1
                    if level == "ERROR":
                        errors_by_module[module] += 1
                        error_msgs[msg] += 1
        return {"errors_by_module": dict(errors_by_module), "top_errors": [m for m, _ in error_msgs.most_common(5)], "hourly_counts": dict(sorted(hourly_counts.items()))}
    logs = [
        "2024-01-15 10:30:45 ERROR db: Connection refused",
        "2024-01-15 10:31:12 INFO app: Started",
        "2024-01-15 11:00:00 ERROR db: Timeout",
        "2024-01-15 11:01:00 ERROR api: Rate limit",
    ]
    with open("/tmp/test.log", "w") as f:
        f.write("\n".join(logs))
    result = analyze_log("/tmp/test.log")
    assert result["errors_by_module"]["db"] == 2
    Path("/tmp/test.log").unlink()
    print("7. Log parser: OK")


def ex8_password_manager():
    def store_passwords(path, accounts):
        data = {}
        for service, password in accounts:
            salt = secrets.token_hex(16)
            hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
            data[service] = {"salt": salt, "hash": hashed.hex(), "id": str(uuid.uuid4())}
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def retrieve_password(path, service):
        with open(path) as f:
            data = json.load(f)
        return data.get(service)
    store_passwords("/tmp/passwords.json", [("email", "pass123"), ("bank", "secure456")])
    entry = retrieve_password("/tmp/passwords.json", "email")
    assert "salt" in entry and "hash" in entry
    Path("/tmp/passwords.json").unlink()
    print("8. Password manager: OK")


def ex9_backup_script():
    def backup_project(source, dest):
        before = shutil.disk_usage(source).used
        archive = shutil.make_archive(str(Path(dest) / "backup"), "zip", source)
        after = shutil.disk_usage(source).used
        return {"archive": archive, "before_bytes": before, "after_bytes": after}
    tmp = Path("/tmp/backup_src")
    tmp.mkdir(exist_ok=True)
    (tmp / "file.txt").write_text("data")
    result = backup_project(tmp, "/tmp")
    assert Path(result["archive"]).exists()
    shutil.rmtree(tmp)
    Path(result["archive"]).unlink()
    print("9. Backup script: OK")


def ex10_markdown_links():
    def extract_markdown_links(md_text):
        return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", md_text)
    md = "Check [Google](https://google.com) and [GitHub](https://github.com)"
    links = extract_markdown_links(md)
    assert links == [("Google", "https://google.com"), ("GitHub", "https://github.com")]
    print("10. Markdown links: OK")


if __name__ == "__main__":
    print("=== Phase 05 Solutions ===\n")
    ex1_parse_ini()
    ex2_dice_roller()
    ex3_meeting_scheduler()
    ex4_csv_aggregator()
    ex5_organize_by_date()
    ex6_json_validator()
    ex7_regex_log_parser()
    ex8_password_manager()
    ex9_backup_script()
    ex10_markdown_links()
    print("\nAll solutions passed!")

"""Log parsing, data validation, and text extraction with regex."""
import re


def parse_log_line(line: str) -> dict | None:
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (ERROR|WARN|INFO) ([\w.]+): (.+)"
    m = re.match(pattern, line)
    if m:
        return {"timestamp": m.group(1), "level": m.group(2), "module": m.group(3), "message": m.group(4)}
    return None


def extract_emails(text: str) -> list:
    return re.findall(r"[\w.]+@[\w.]+\.\w+", text)


def validate_phone(phone: str) -> bool:
    return bool(re.fullmatch(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", phone.strip()))


def extract_hashtags(text: str) -> list:
    return re.findall(r"#\w+", text)


logs = ["2024-01-15 10:30:45 ERROR db.connection: Connection refused", "2024-01-15 10:31:12 INFO app.startup: Server started"]
for line in logs:
    print(parse_log_line(line))

print("Emails:", extract_emails("Contact: eleven@lab.gov or mike@hawkins.org"))
print("Valid phone?", validate_phone("(555) 123-4567"))
print("Hashtags:", extract_hashtags("#Python #regex is #powerful"))

"""Email with Flask-Mail: sending, templates, attachments, async send."""
from typing import Any, Optional
from datetime import datetime
import json
import time
import threading
import smtplib


# ======================== Email System ========================

class EmailMessage:
    def __init__(self, subject: str = "", recipients: list[str] = None, body: str = "", html: str = "",
                 sender: str = "noreply@example.com", cc: list[str] = None, bcc: list[str] = None):
        self.subject = subject
        self.recipients = recipients or []
        self.body = body
        self.html = html
        self.sender = sender
        self.cc = cc or []
        self.bcc = bcc or []
        self.attachments: list[dict] = []
        self.sent_at: Optional[str] = None
        self.status = "pending"

    def attach(self, filename: str, content: bytes, content_type: str = "application/octet-stream"):
        self.attachments.append({"filename": filename, "content": content, "content_type": content_type})

    def to_dict(self) -> dict:
        return {
            "subject": self.subject,
            "to": self.recipients,
            "cc": self.cc,
            "bcc": self.bcc,
            "sender": self.sender,
            "body_length": len(self.body),
            "has_html": bool(self.html),
            "attachments": len(self.attachments),
            "status": self.status,
            "sent_at": self.sent_at,
        }


class Mail:
    """Simulates Flask-Mail."""
    def __init__(self, server: str = "smtp.example.com", port: int = 587, username: str = "",
                 password: str = "", use_tls: bool = True):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.sent: list[EmailMessage] = []
        self._fail_mode = False

    def send(self, message: EmailMessage):
        try:
            time.sleep(0.02)
            message.status = "sent"
            message.sent_at = datetime.now().isoformat()
            self.sent.append(message)
            return True
        except Exception as e:
            message.status = "failed"
            return False

    def async_send(self, message: EmailMessage):
        thread = threading.Thread(target=self.send, args=(message,), daemon=True)
        thread.start()
        return thread

    def send_template(self, subject: str, recipients: list[str], template: str, **context) -> EmailMessage:
        body = template
        for key, val in context.items():
            body = body.replace(f"{{{{{key}}}}}", str(val))
        msg = EmailMessage(subject=subject, recipients=recipients, body=body)
        self.send(msg)
        return msg

    def get_stats(self) -> dict:
        return {"total_sent": len(self.sent), "server": self.server, "port": self.port}


mail = Mail(server="smtp.gmail.com", port=587, username="app@example.com")


class Flask:
    def __init__(self):
        self.routes: list[dict] = []
        self.mail = mail

    def route(self, path, methods=None):
        methods = methods or ["GET"]
        def deco(f):
            self.routes.append({"path": path, "methods": methods, "handler": f}); return f
        return deco

    def __call__(self, method, path, **kw):
        for r in self.routes:
            if method in r["methods"] and r["path"] == path:
                result = r["handler"](**kw)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}

app = Flask()


# ======================== Routes ========================

@app.route("/email/send", methods=["POST"])
def send_email(**kw):
    msg = EmailMessage(
        subject=kw.get("subject", "No Subject"),
        recipients=[kw.get("to", "user@example.com")],
        body=kw.get("body", ""),
        sender=kw.get("sender", "noreply@example.com"),
    )
    success = app.mail.send(msg)
    return {"sent": success, "message": msg.to_dict()}


@app.route("/email/welcome", methods=["POST"])
def send_welcome(**kw):
    username = kw.get("username", "User")
    email = kw.get("email", "user@example.com")

    template = f"""
    Welcome {username}!
    Thank you for registering.
    Your email: {email}
    Best regards,
    The Team
    """

    msg = app.mail.send_template(
        subject=f"Welcome to FlaskApp, {username}!",
        recipients=[email],
        template=template,
    )
    return {"sent": True, "message": msg.to_dict()}


@app.route("/email/async", methods=["POST"])
def send_async(**kw):
    msg = EmailMessage(
        subject="Async Email",
        recipients=[kw.get("to", "user@example.com")],
        body="This was sent asynchronously!",
    )
    thread = app.mail.async_send(msg)
    thread.join(timeout=1)
    return {"sent": msg.status == "sent", "message": msg.to_dict(), "async": True}


@app.route("/email/bulk", methods=["POST"])
def send_bulk(**kw):
    recipients = kw.get("recipients", "user@example.com").split(",")
    results = []
    for email in recipients:
        msg = EmailMessage(subject="Bulk Email", recipients=[email.strip()], body="You're receiving this bulk email.")
        success = app.mail.send(msg)
        results.append({"email": email.strip(), "sent": success})
    return {"results": results, "total": len(results), "success": sum(1 for r in results if r["sent"])}


@app.route("/email/stats")
def email_stats():
    return app.mail.get_stats()


@app.route("/email/history")
def email_history():
    return {"emails": [m.to_dict() for m in app.mail.sent]}


# ======================== Demo ========================
print("=== Email Demo ===\n")

print("1. Send welcome email:")
r = app("POST", "/email/welcome", username="Alice", email="alice@example.com")
print(f"   Sent: {r['data']['sent']}")
print(f"   Subject: {r['data']['message']['subject']}")
print(f"   To: {r['data']['message']['to']}\n")

print("2. Send plain email:")
r = app("POST", "/email/send", subject="Hello!", to="bob@example.com", body="Just saying hi")
print(f"   Sent: {r['data']['sent']}\n")

print("3. Async send:")
r = app("POST", "/email/async", to="async@example.com")
print(f"   Sent: {r['data']['sent']} (async={r['data']['async']})\n")

print("4. Bulk send:")
r = app("POST", "/email/bulk", recipients="a@test.com,b@test.com,c@test.com")
print(f"   Success: {r['data']['success']}/{r['data']['total']}\n")

print("5. Email stats:")
r = app("GET", "/email/stats")
print(f"   {json.dumps(r['data'])}\n")

print("6. Email history:")
r = app("GET", "/email/history")
for msg in r["data"]["emails"]:
    print(f"   [{msg['status']}] To: {msg['to']}, Subject: {msg['subject']}")

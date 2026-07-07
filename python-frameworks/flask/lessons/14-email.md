# ✉️ Email with Flask-Mail
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Send emails, templates, attachments, async sending, bulk emails.

## Install

```bash
pip install flask-mail
```

## Configuration

```python
from flask_mail import Mail, Message

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your@email.com"
app.config["MAIL_PASSWORD"] = "your-password"
app.config["MAIL_DEFAULT_SENDER"] = "noreply@example.com"

mail = Mail(app)
```

## Sending Basic Emails

```python
@app.route("/email/send", methods=["POST"])
def send_email():
    msg = Message(
        subject="Hello from Flask",
        recipients=["user@example.com"],
        body="This is a test email.",
    )
    mail.send(msg)
    return {"message": "Email sent"}
```

## HTML Emails

```python
msg = Message("Welcome!", recipients=[email])
msg.html = render_template("emails/welcome.html", username=username)
mail.send(msg)
```

## Email with Attachments

```python
msg = Message("Report", recipients=["admin@example.com"])
msg.body = "Please find the report attached."
with app.open_resource("report.pdf") as fp:
    msg.attach("report.pdf", "application/pdf", fp.read())
mail.send(msg)
```

## Bulk Emails

```python
@app.route("/email/bulk", methods=["POST"])
def send_bulk():
    recipients = request.form["recipients"].split(",")
    with mail.connect() as conn:
        for email in recipients:
            msg = Message("Bulk Email", recipients=[email.strip()])
            msg.body = "You're receiving this bulk email."
            conn.send(msg)
    return {"sent": len(recipients)}
```

## Async Sending

```python
import threading

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.route("/email/async", methods=["POST"])
def send_async():
    msg = Message("Async Email", recipients=["user@example.com"], body="Sent async!")
    thread = threading.Thread(target=send_async_email, args=(app, msg))
    thread.start()
    return {"message": "Email queued"}
```

<!-- 🤔 For production, use a task queue (Celery/RQ) instead of raw threads. -->

## Run the Code

```bash
python code/14-email.py
```

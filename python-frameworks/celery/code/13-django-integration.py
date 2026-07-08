"""Django integration — Celery with Django settings pattern."""
from celery import Celery


print("=== Django Integration ===\n")

app = Celery('django_project', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

app.conf.task_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.timezone = 'UTC'

@app.task
def send_welcome_email(user_email, username):
    print(f"  [EMAIL] To: {user_email}")
    print(f"  [EMAIL] Subject: Welcome {username}!")
    print(f"  [EMAIL] Body: Thanks for joining!")
    return f"email sent to {user_email}"

@app.task
def generate_thumbnail(image_path, size=(150, 150)):
    print(f"  [THUMB] Processing: {image_path}")
    print(f"  [THUMB] Size: {size}")
    return f"thumbnail_{image_path}"

@app.task
def cleanup_expired_sessions():
    print(f"  [CLEANUP] Removing expired sessions...")
    return "cleaned"

r1 = send_welcome_email.delay("user@example.com", "Alice")
print(f"  → {r1.get()}\n")

r2 = generate_thumbnail.delay("/uploads/photo.jpg", (300, 300))
print(f"  → {r2.get()}\n")

r3 = cleanup_expired_sessions.delay()
print(f"  → {r3.get()}\n")

print("Django pattern:")
print("  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')")
print("  app.config_from_object('django.conf:settings', namespace='CELERY')")
print("  app.autodiscover_tasks()")

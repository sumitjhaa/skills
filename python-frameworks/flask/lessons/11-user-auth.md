# 🔐 User Authentication
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** Password hashing, login/logout, `@login_required` decorator, Flask-Login.

## Install

```bash
pip install flask-login
```

## Password Hashing

Never store plain-text passwords. Use `werkzeug.security`:

```python
from werkzeug.security import generate_password_hash, check_password_hash

hash = generate_password_hash("secret123")
check_password_hash(hash, "secret123")  # True
```

## Flask-Login Setup

```python
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

## Registration

```python
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing = User.query.filter_by(username=request.form["username"]).first()
        if existing:
            flash("Username taken", "error")
        else:
            user = User(username=request.form["username"])
            user.password_hash = generate_password_hash(request.form["password"])
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Welcome!", "success")
            return redirect(url_for("profile"))
    return render_template("register.html")
```

## Login/Logout

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password_hash, request.form["password"]):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "error")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("home"))
```

## Protected Routes

```python
@app.route("/dashboard")
@login_required
def dashboard():
    return {"user": current_user.username, "id": current_user.id}
```

<!-- 🤔 `current_user` is available in all templates and views after setup. -->

## Custom Unauthorized Handler

```python
@login_manager.unauthorized_handler
def unauthorized():
    flash("Please log in first", "warning")
    return redirect(url_for("login"))
```

## Run the Code

```bash
python code/11-user-auth.py
```

# 🗄️ SQLAlchemy + FastAPI
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Define SQLAlchemy models, create sessions, perform CRUD in FastAPI endpoints.

## Install

```bash
pip install sqlalchemy
```

## Define Models

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(String(5000))
    user_id = Column(Integer, ForeignKey("users.id"))
```

<!-- 🧩 `declarative_base()` creates a base class. Each model maps to a table. -->

## Database Session Pattern

```python
engine = create_engine("sqlite:///./app.db")
Base.metadata.create_all(bind=engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
```

<!-- 🔄 `yield` + `finally` = automatic cleanup. FastAPI calls `get_db` per request. -->

## CRUD in Endpoints

```python
@app.post("/users")
def create_user(username: str, email: str, db: Session = Depends(get_db)):
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Relationships

```python
class User(Base):
    posts = relationship("Post", back_populates="author")

class Post(Base):
    author = relationship("User", back_populates="posts")

# Usage: user.posts or post.author
```

## Run the Code

```bash
python code/11-sqlalchemy-models.py
```

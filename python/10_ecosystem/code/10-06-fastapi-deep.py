"""FastAPI Deep — social-media analytics API with DI, middleware, WebSocket.
Run: uvicorn 10-06-fastapi-deep:app --reload
or:  python 10-06-fastapi-deep.py
"""

from fastapi import FastAPI, Depends, HTTPException, WebSocket, BackgroundTasks, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import asyncio

app = FastAPI(title="Social Analytics API")


class PostCreate(BaseModel):
    content: str = Field(min_length=1, max_length=280)
    user_id: int = Field(gt=0)


class PostResponse(BaseModel):
    id: int
    content: str
    user_id: int
    likes: int = 0
    created_at: str


fake_db: list[dict] = []
next_id: int = 1


def get_db() -> list[dict]:
    return fake_db


def get_current_user(api_key: str = Query(...)) -> dict:
    if api_key != "secret":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {"user_id": 1, "name": "Analyst"}


@app.post("/posts", response_model=PostResponse, status_code=201)
def create_post(
    post: PostCreate,
    bg: BackgroundTasks,
    db: list[dict] = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> dict:
    global next_id
    record = {
        "id": next_id,
        "content": post.content,
        "user_id": post.user_id,
        "likes": 0,
        "created_at": datetime.now().isoformat(),
    }
    next_id += 1
    db.append(record)
    bg.add_task(send_notification, record["id"], user["user_id"])
    return record


@app.get("/posts", response_model=list[PostResponse])
def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: list[dict] = Depends(get_db),
) -> list[dict]:
    return db[skip : skip + limit]


@app.get("/posts/{post_id}", response_model=Optional[PostResponse])
def get_post(post_id: int, db: list[dict] = Depends(get_db)) -> Optional[dict]:
    for record in db:
        if record["id"] == post_id:
            return record
    raise HTTPException(404, "Post not found")


@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: list[dict] = Depends(get_db)) -> None:
    for i, record in enumerate(db):
        if record["id"] == post_id:
            db.pop(i)
            return
    raise HTTPException(404, "Post not found")


@app.middleware("http")
async def timing_middleware(request: object, call_next):
    import time
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    return response


@app.websocket("/ws/analytics")
async def analytics_websocket(websocket: WebSocket):
    await websocket.accept()
    for i in range(10):
        await asyncio.sleep(1)
        await websocket.send_json({"event": "analytics_update", "value": i})
    await websocket.close()


async def send_notification(post_id: int, user_id: int) -> None:
    await asyncio.sleep(0.1)
    print(f"Notification sent for post {post_id} to user {user_id}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("10-06-fastapi-deep:app", host="0.0.0.0", port=8000, reload=True)

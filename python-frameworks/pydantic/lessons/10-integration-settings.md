# 🏁 Integration: Settings & API Client
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** Settings management with `BaseSettings`, API response validation, full integration demo.

## Settings with BaseSettings

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str = "sqlite:///dev.db"
    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

## API Response Validation

```python
class ApiResponse(BaseModel):
    status: str
    data: dict | list
    error: str | None = None

def call_api(url: str) -> ApiResponse:
    resp = httpx.get(url)
    return ApiResponse(**resp.json())
```

## Request Schemas

```python
class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(pattern=r"^\S+@\S+\.\S+$")
    role: Literal["admin", "user"] = "user"

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
```

## Full Pipeline

```python
# 1. Load config
settings = Settings()

# 2. Validate input
request = CreateUserRequest(**input_data)

# 3. Process (DB insert, etc.)

# 4. Return validated response
return UserResponse(id=1, **request.model_dump(), created_at=datetime.now())
```

## Run the Code

```bash
python code/10-integration-settings.py
```

"""OpenAPI customization: schema metadata, tags, examples, custom responses."""
from typing import Any, Optional
from datetime import datetime
import json


# ======================== OpenAPI Schema Generator ========================

class OpenAPIGenerator:
    """Generates OpenAPI 3.0 schema from route metadata."""
    def __init__(self, title: str = "API", version: str = "1.0.0", description: str = ""):
        self.schema = {
            "openapi": "3.0.3",
            "info": {
                "title": title,
                "version": version,
                "description": description,
            },
            "paths": {},
            "components": {
                "schemas": {},
                "securitySchemes": {
                    "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
                },
            },
            "tags": [],
            "servers": [{"url": "http://localhost:8000", "description": "Development"}],
        }
        self._tag_set: set[str] = set()

    def add_path(self, method: str, path: str, metadata: dict):
        if path not in self.schema["paths"]:
            self.schema["paths"][path] = {}
        method_lower = method.lower()
        path_item = self.schema["paths"][path]

        operation = {
            "summary": metadata.get("summary", ""),
            "description": metadata.get("description", ""),
            "operationId": metadata.get("operation_id", ""),
            "tags": metadata.get("tags", []),
            "parameters": self._build_parameters(metadata.get("parameters", [])),
            "requestBody": self._build_request_body(metadata.get("request_body")),
            "responses": self._build_responses(metadata.get("responses", {200: {"description": "Successful"}})),
            "security": metadata.get("security", []),
        }

        for tag in operation["tags"]:
            self._tag_set.add(tag)

        path_item[method_lower] = operation

    def _build_parameters(self, params: list) -> list:
        return [
            {
                "name": p["name"],
                "in": p.get("in", "query"),
                "required": p.get("required", False),
                "schema": {"type": p.get("type", "string")},
                "description": p.get("description", ""),
            }
            for p in params
        ]

    def _build_request_body(self, body: dict | None) -> dict | None:
        if body is None:
            return None
        return {
            "required": body.get("required", True),
            "content": {
                "application/json": {
                    "schema": {"$ref": f"#/components/schemas/{body['schema']}"}
                }
            },
        }

    def _build_responses(self, responses: dict) -> dict:
        result = {}
        for code, resp in responses.items():
            entry = {"description": resp.get("description", "")}
            if "schema" in resp:
                entry["content"] = {
                    "application/json": {
                        "schema": {"$ref": f"#/components/schemas/{resp['schema']}"}
                    }
                }
            result[str(code)] = entry
        return result

    def add_schema(self, name: str, properties: dict, required: list[str] | None = None):
        self.schema["components"]["schemas"][name] = {
            "type": "object",
            "properties": {k: {"type": v} for k, v in properties.items()},
        }
        if required:
            self.schema["components"]["schemas"][name]["required"] = required

    def set_servers(self, servers: list[dict]):
        self.schema["servers"] = servers

    def get_schema(self) -> dict:
        self.schema["tags"] = [{"name": t, "description": f"Operations about {t}"} for t in sorted(self._tag_set)]
        return self.schema


# ======================== FastAPI App ========================

class FastAPI:
    def __init__(self, title: str = "API", version: str = "1.0.0", description: str = ""):
        self.routes: list[dict] = []
        self.openapi = OpenAPIGenerator(title=title, version=version, description=description)
        self.title = title

    def _register(self, method: str, path: str, metadata: dict):
        def deco(func):
            route = {"path": path, "method": method, "handler": func, "metadata": metadata}
            self.routes.append(route)

            # Register in OpenAPI schema
            self.openapi.add_path(method, path, metadata)
            return func
        return deco

    def get(self, path: str, **metadata):
        return self._register("GET", path, metadata)

    def post(self, path: str, **metadata):
        return self._register("POST", path, metadata)

    def delete(self, path: str, **metadata):
        return self._register("DELETE", path, metadata)

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


# ======================== Create App ========================

app = FastAPI(
    title="Custom API",
    version="2.0.0",
    description="A fully documented API with custom OpenAPI schema",
)


# ======================== Register Schemas ========================

app.openapi.add_schema("Item", {"id": "integer", "name": "string", "price": "number"}, required=["name", "price"])
app.openapi.add_schema("User", {"id": "integer", "username": "string", "email": "string"}, required=["username", "email"])
app.openapi.add_schema("Error", {"detail": "string", "code": "integer"})
app.openapi.add_schema("ItemCreate", {"name": "string", "price": "number"}, required=["name", "price"])
app.openapi.add_schema("UserCreate", {"username": "string", "email": "string", "password": "string"}, required=["username", "email", "password"])


# ======================== Endpoints with Metadata ========================

@app.get("/items",
    summary="List all items",
    description="Returns a paginated list of items. Supports filtering by category.",
    operation_id="listItems",
    tags=["items"],
    parameters=[
        {"name": "category", "in": "query", "type": "string", "description": "Filter by category", "required": False},
        {"name": "limit", "in": "query", "type": "integer", "description": "Results per page", "required": False},
    ],
    responses={
        200: {"description": "List of items", "schema": "Item"},
    },
)
def list_items():
    return {"items": [{"id": 1, "name": "Laptop", "price": 999.99}]}


@app.post("/items",
    summary="Create a new item",
    description="Create an item with name and price. Returns the created item.",
    operation_id="createItem",
    tags=["items"],
    request_body={"schema": "ItemCreate"},
    responses={
        201: {"description": "Created item", "schema": "Item"},
        422: {"description": "Validation error", "schema": "Error"},
    },
    security=[{"bearerAuth": []}],
)
def create_item(name: str = "New Item", price: float = 0.0):
    return {"id": 1, "name": name, "price": price}


@app.get("/users",
    summary="List all users",
    operation_id="listUsers",
    tags=["users"],
    responses={200: {"description": "List of users", "schema": "User"}},
)
def list_users():
    return {"users": [{"id": 1, "username": "alice", "email": "alice@example.com"}]}


@app.post("/users",
    summary="Create a new user",
    operation_id="createUser",
    tags=["users"],
    request_body={"schema": "UserCreate"},
    responses={201: {"description": "Created user", "schema": "User"}},
    security=[{"bearerAuth": []}],
)
def create_user(username: str = "newuser", email: str = "user@example.com", password: str = "secret"):
    return {"id": 2, "username": username, "email": email}


@app.get("/health",
    summary="Health check",
    operation_id="healthCheck",
    tags=["system"],
    responses={200: {"description": "Service health"}},
)
def health_check():
    return {"status": "healthy", "version": "2.0.0", "timestamp": datetime.now().isoformat()}


@app.get("/openapi.json",
    summary="OpenAPI schema",
    operation_id="getOpenAPI",
    tags=["system"],
)
def get_openapi():
    return app.openapi.get_schema()


# ======================== Demo ========================
print("=== OpenAPI Customization Demo ===\n")

print(f"1. API Info:")
schema = app.openapi.get_schema()
info = schema["info"]
print(f"   Title: {info['title']}")
print(f"   Version: {info['version']}")
print(f"   Description: {info['description']}\n")

print(f"2. Servers:")
for srv in schema["servers"]:
    print(f"   - {srv['url']} ({srv['description']})")

print(f"\n3. Tags:")
for tag in schema["tags"]:
    print(f"   - {tag['name']}: {tag['description']}")

print(f"\n4. Security Schemes:")
for name, scheme in schema["components"]["securitySchemes"].items():
    print(f"   - {name}: {scheme['type']} ({scheme['scheme']})")

print(f"\n5. Schemas:")
for name, sch in schema["components"]["schemas"].items():
    props = ", ".join(sch["properties"].keys())
    print(f"   - {name}: {{{props}}}")

print(f"\n6. Paths ({len(schema['paths'])}):")
for path, methods in schema["paths"].items():
    for method, op in methods.items():
        print(f"   {method.upper():6s} {path:20s} → {op['summary']}")

print(f"\n7. Full schema preview (paths only):")
print(json.dumps(schema["paths"], indent=2)[:2000])

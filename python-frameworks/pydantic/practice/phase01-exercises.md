# 📝 Pydantic Practice

## Exercise 1: User Profile

Create a `UserProfile` model with fields: username (alphanumeric, 3-30 chars), email (validated), age (18-120), bio (optional, max 500). Write a validator that ensures username is lowercase.

## Exercise 2: Nested Config

Model an app config:
- `Database` (host, port, name, user, password)
- `Server` (host, port, workers, timeout)
- `AppConfig` (app_name, debug, database: Database, server: Server)

Create a nested config from a dict, serialize to JSON with indentation.

## Exercise 3: Order Validation

Create models for an order system:
- `OrderItem` (product_id, quantity > 0, unit_price > 0)
- `Order` (items: list[OrderItem], coupon: str | None)
- Model validator: if coupon is used, minimum order total must be $50
- Field validator: coupon codes must be uppercase, 5-10 chars

Test with valid and invalid inputs.

## Exercise 4: API Response Generic

Create a generic `ApiResponse[T]` with fields: success (bool), data (T), error (str | None). Then create `LoginRequest` (email, password) and `LoginResponse` (token, expires_at) models. Demonstrate a full request → validation → response pipeline.

## Exercise 5: Settings with Validation

Create a `Settings` model with:
- `environment` (Literal["dev", "staging", "prod"])
- `database_url` — must be a valid scheme
- `secret_key` — must be at least 32 chars
- `allowed_hosts` — list of strings, at least 1
- `debug` — only True if environment is "dev"

Test loading from a dict and catching errors.

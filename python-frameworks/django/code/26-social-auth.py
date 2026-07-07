"""Social auth (OAuth) simulation: Google, GitHub login flow."""
from typing import Optional
import secrets
import hashlib


# ======================== OAuth Provider Simulation ========================

class OAuthProvider:
    """Simulates an OAuth2 provider (Google, GitHub, etc.)."""

    def __init__(self, name: str, client_id: str, client_secret: str):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self._token_cache: dict[str, str] = {}  # code → access_token

    def get_auth_url(self, redirect_uri: str, state: str) -> str:
        """Return the OAuth authorization URL."""
        return f"https://{self.name}.com/oauth/authorize?client_id={self.client_id}&redirect_uri={redirect_uri}&state={state}&response_type=code"

    def exchange_code(self, code: str, redirect_uri: str) -> Optional[str]:
        """Exchange authorization code for access token. Deterministic for same code."""
        if code.startswith("valid_"):
            if code not in self._token_cache:
                self._token_cache[code] = f"access_token_{hashlib.md5(code.encode()).hexdigest()[:12]}"
            return self._token_cache[code]
        return None

    def get_user_info(self, access_token: str) -> Optional[dict]:
        """Fetch user profile from provider. Deterministic for same token."""
        if access_token and access_token.startswith("access_token_"):
            # Use a deterministic ID based on the token
            user_id = hashlib.md5(access_token.encode()).hexdigest()[:12]
            return {
                "id": f"{self.name}_{user_id}",
                "email": f"user@{self.name}.com",
                "name": f"User from {self.name}",
                "avatar": f"https://{self.name}.com/avatar.png",
            }
        return None


# ======================== Social Auth Adapter ========================

SOCIAL_ACCOUNTS: dict[str, int] = {}  # provider_uid → user_id
USERS: dict[int, dict] = {}
SESSIONS: dict[str, int] = {}
PK = 1


class User:
    def __init__(self, username: str, email: str):
        global PK
        self.id = PK
        self.username = username
        self.email = email
        self.is_authenticated = False
        self.is_active = True
        self.social_accounts: list[str] = []
        USERS[PK] = self
        PK += 1


class SocialAuthBackend:
    """Handle OAuth flow: redirect → callback → login/create user."""

    def __init__(self):
        self.providers: dict[str, OAuthProvider] = {}
        self._state_store: dict[str, str] = {}  # state → provider_name

    def register_provider(self, provider: OAuthProvider):
        self.providers[provider.name] = provider

    def get_login_url(self, provider_name: str, redirect_uri: str) -> Optional[str]:
        provider = self.providers.get(provider_name)
        if not provider:
            return None
        state = secrets.token_urlsafe(16)
        self._state_store[state] = provider_name
        return provider.get_auth_url(redirect_uri, state)

    def callback(self, provider_name: str, code: str, redirect_uri: str) -> Optional[dict]:
        """Handle OAuth callback: exchange code → get user info → login/register."""
        provider = self.providers.get(provider_name)
        if not provider:
            return None

        token = provider.exchange_code(code, redirect_uri)
        if not token:
            return None

        info = provider.get_user_info(token)
        if not info:
            return None

        # Check existing social account
        uid = f"{provider_name}_{info['id']}"
        if uid in SOCIAL_ACCOUNTS:
            user_id = SOCIAL_ACCOUNTS[uid]
            user = USERS[user_id]
        else:
            # Create new user
            username = info.get("name", f"{provider_name}_user").lower().replace(" ", "_")
            email = info.get("email", f"{uid}@example.com")
            user = User(username, email)
            user.social_accounts.append(uid)

        is_new = uid not in SOCIAL_ACCOUNTS
        if is_new:
            SOCIAL_ACCOUNTS[uid] = user.id

        user.is_authenticated = True
        session_id = secrets.token_hex(16)
        SESSIONS[session_id] = user.id

        return {
            "user": user,
            "session_id": session_id,
            "is_new": is_new,
        }


# ======================== Views ========================

def social_login_view(backend: SocialAuthBackend, request: dict) -> dict:
    provider_name = request.get("provider", "google")
    redirect_uri = request.get("redirect_uri", "http://localhost:8000/auth/callback/")

    url = backend.get_login_url(provider_name, redirect_uri)
    if not url:
        return {"status": 400, "error": f"Unknown provider: {provider_name}"}
    return {"status": 302, "location": url}


def social_callback_view(backend: SocialAuthBackend, request: dict) -> dict:
    provider = request.get("provider", "google")
    code = request.get("code", "")
    redirect_uri = request.get("redirect_uri", "http://localhost:8000/auth/callback/")

    result = backend.callback(provider, code, redirect_uri)
    if not result:
        return {"status": 401, "error": "Authentication failed"}
    return {
        "status": 200,
        "message": f"Logged in as {result['user'].username}",
        "is_new_user": result["is_new"],
        "user_id": result["user"].id,
    }


# ======================== Demo ========================
print("=== Social Auth Demo ===")

# Setup
backend = SocialAuthBackend()
backend.register_provider(OAuthProvider("google", "google_client_id", "google_secret"))
backend.register_provider(OAuthProvider("github", "github_client_id", "github_secret"))

# Step 1: Get login URL
url_result = social_login_view(backend, {"provider": "google"})
print(f"Redirect to: {url_result['location'][:60]}...")

# Step 2: Simulate callback with valid code
callback_result = social_callback_view(backend, {
    "provider": "google",
    "code": "valid_auth_code",
})
print(f"Callback result: {callback_result}")

# Step 3: Login again (existing account)
callback_result2 = social_callback_view(backend, {
    "provider": "google",
    "code": "valid_auth_code",
})
print(f"Second login  : {callback_result2}")

# Step 4: Invalid code
bad_result = social_callback_view(backend, {
    "provider": "google",
    "code": "bad_code",
})
print(f"Bad code     : {bad_result}")

# Step 5: GitHub login
gh_result = social_callback_view(backend, {
    "provider": "github",
    "code": "valid_github_code",
})
print(f"GitHub login : {gh_result}")

#  django-allauth equivalents
print("\n--- django-allauth URL patterns ---")
print("  /accounts/google/login/")
print("  /accounts/google/login/callback/")
print("  /accounts/github/login/")
print("  /accounts/social/connections/")
print("  /accounts/social/account/connections/")

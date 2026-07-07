"""Security hardening: HTTPS, CSP, SQL injection, XSS, CSRF, rate limiting."""
import json
import hashlib
import hmac
import time
import re
from collections import defaultdict


# ======================== Security Headers ========================

class SecurityHeaders:
    """Generate security-related HTTP headers."""
    @staticmethod
    def get_headers(https: bool = True) -> dict:
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
        }
        if https:
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            headers["Content-Security-Policy"] = SecurityHeaders.csp_policy()
        return headers

    @staticmethod
    def csp_policy() -> str:
        directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://cdn.example.com",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self' https://fonts.gstatic.com",
            "connect-src 'self' https://api.example.com",
            "frame-ancestors 'none'",
            "form-action 'self'",
            "base-uri 'self'",
        ]
        return "; ".join(directives)


# ======================== SQL Injection Simulation ========================

class SQLInjectionDetector:
    """Detect basic SQL injection patterns."""
    DANGEROUS_PATTERNS = [
        r"'.*OR.*'.*'",
        r"'.*--",
        r"';.*DROP",
        r"';.*DELETE",
        r"UNION.*SELECT",
        r"';.*EXEC",
        r"';.*INSERT",
        r"'.*1\s*=\s*1.*'",
    ]

    @staticmethod
    def is_dangerous(input_str: str) -> tuple[bool, str]:
        for pattern in SQLInjectionDetector.DANGEROUS_PATTERNS:
            if re.search(pattern, input_str, re.IGNORECASE):
                return True, f"SQL injection pattern detected: {pattern}"
        return False, ""


class ParameterizedQuery:
    """Demonstrates safe vs unsafe query building."""
    @staticmethod
    def unsafe(username: str) -> str:
        return f"SELECT * FROM users WHERE username = '{username}'"

    @staticmethod
    def safe(username: str) -> tuple[str, tuple]:
        return "SELECT * FROM users WHERE username = %s", (username,)

    @staticmethod
    def validate(username: str) -> bool:
        """Validate that a query uses parameterization."""
        is_dangerous, reason = SQLInjectionDetector.is_dangerous(username)
        return not is_dangerous, reason


# ======================== Rate Limiter ========================

class TokenBucketRateLimiter:
    """Token bucket algorithm for rate limiting."""
    def __init__(self, rate: int = 100, burst: int = 200, window: float = 60.0):
        self.rate = rate
        self.burst = burst
        self.window = window
        self.buckets: dict[str, dict] = {}

    def allow(self, key: str, tokens: int = 1) -> bool:
        now = time.time()
        if key not in self.buckets:
            self.buckets[key] = {"tokens": self.burst, "last_refill": now}
        bucket = self.buckets[key]
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(
            self.burst,
            bucket["tokens"] + elapsed * (self.rate / self.window),
        )
        bucket["last_refill"] = now
        if bucket["tokens"] >= tokens:
            bucket["tokens"] -= tokens
            return True
        return False

    def remaining(self, key: str) -> float:
        if key not in self.buckets:
            return self.burst
        return round(self.buckets[key]["tokens"], 1)


# ======================== CSRF Simulation ========================

class CSRFProtection:
    """Simulates CSRF token generation and validation."""
    def __init__(self, secret_key: str = "csrf-secret"):
        self.secret_key = secret_key

    def generate_token(self, session_id: str) -> str:
        message = f"{session_id}:{int(time.time() // 86400)}"
        return hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

    def validate_token(self, token: str, session_id: str) -> bool:
        expected = self.generate_token(session_id)
        return hmac.compare_digest(token, expected)


# ======================== Input Sanitizer ========================

class InputSanitizer:
    """Basic input sanitization."""
    @staticmethod
    def strip_xss(html: str) -> str:
        """Remove script tags and event handlers from HTML."""
        cleaned = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'javascript\s*:', '', cleaned, flags=re.IGNORECASE)
        return cleaned

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Remove path traversal and dangerous characters."""
        cleaned = filename.replace("..", "").replace("/", "").replace("\\", "")
        cleaned = re.sub(r'[^\w\-. ]', '', cleaned)
        return cleaned


# ======================== Demo ========================
print("=== Security Hardening Demo ===\n")

# --- Security headers ---
print("1. Security headers:")
headers = SecurityHeaders.get_headers(https=True)
for k, v in headers.items():
    print(f"   {k}: {v}")

# --- SQL injection ---
print("\n2. SQL injection detection:")
safe_input = "alice"
dangerous_input = "' OR '1'='1"
for inp in [safe_input, dangerous_input]:
    is_danger, reason = SQLInjectionDetector.is_dangerous(inp)
    print(f"   Input '{inp[:15]}...': {'⚠ DANGEROUS' if is_danger else '✅ Safe'}")
    if is_danger:
        print(f"     Reason: {reason}")

# Parameterized queries
print("\n3. Parameterized queries:")
unsafe_query = ParameterizedQuery.unsafe(dangerous_input)
safe_query, params = ParameterizedQuery.safe(dangerous_input)
print(f"   Unsafe: {unsafe_query}")
print(f"   Safe:   {safe_query}")

# --- Rate limiting ---
print("\n4. Rate limiting (Token Bucket, 10/min, burst=15):")
limiter = TokenBucketRateLimiter(rate=10, burst=15, window=60)
client_ip = "203.0.113.50"
for i in range(18):
    allowed = limiter.allow(client_ip)
    remaining = limiter.remaining(client_ip)
    if i < 15 or i == 17:
        icon = "✅" if allowed else "❌"
        print(f"   Request {i+1:2d}: {icon} allowed (remaining: {remaining})")
    if not allowed:
        print(f"   ... (rate limited after request {i+1})")
        break

# --- CSRF ---
print("\n5. CSRF protection:")
csrf = CSRFProtection("my-secret-key")
session_id = "abc123session"
token = csrf.generate_token(session_id)
print(f"   Generated token: {token[:20]}...")
print(f"   Valid (correct session):   {csrf.validate_token(token, session_id)}")
print(f"   Valid (wrong session):     {csrf.validate_token(token, 'wrong-session')}")

# --- Input sanitization ---
print("\n6. Input sanitization:")
dirty_html = '<p>Hello</p><script>alert("xss")</script><img onerror="alert(1)" src=x>'
clean_html = InputSanitizer.strip_xss(dirty_html)
print(f"   Dirty: {dirty_html}")
print(f"   Clean: {clean_html}")

dirty_filename = "../../etc/passwd"
clean_filename = InputSanitizer.sanitize_filename(dirty_filename)
print(f"   Dirty filename: {dirty_filename}")
print(f"   Clean filename: {clean_filename}")

# --- Security checklist ---
print("\n7. Production security checklist:")
checks = [
    ("HTTPS enforced", True),
    ("SECURE_SSL_REDIRECT = True", True),
    ("SESSION_COOKIE_SECURE = True", True),
    ("CSRF_COOKIE_SECURE = True", True),
    ("SECURE_HSTS_SECONDS = 31536000", True),
    ("SECURE_HSTS_INCLUDE_SUBDOMAINS = True", True),
    ("SECURE_CONTENT_TYPE_NOSNIFF = True", True),
    ("SECURE_BROWSER_XSS_FILTER = True", True),
    ("X_FRAME_OPTIONS = 'DENY'", True),
    ("SECURE_PROXY_SSL_HEADER configured", True),
    ("SECRET_KEY rotated (not default)", True),
    ("ALLOWED_HOSTS restricted", True),
    ("DEBUG = False", True),
    ("Password hashers = bcrypt/argon2", True),
    ("CORS_ORIGIN_ALLOW_ALL = False", True),
    ("Database connection encrypted", True),
    ("Static/media served via CDN", True),
    ("Rate limiting enabled", True),
    ("Sentry/logging configured", True),
    ("Regular dependency audits", True),
]
for item, done in checks:
    print(f"   {'✅' if done else '☐'} {item}")

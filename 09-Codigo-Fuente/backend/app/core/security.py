import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from datetime import date, datetime

from app.core.config import settings

ALGO_SEPARATOR = "$"


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return ALGO_SEPARATOR.join(
        ("pbkdf2_sha256", base64.urlsafe_b64encode(salt).decode(), base64.urlsafe_b64encode(digest).decode())
    )


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, salt_b64, digest_b64 = stored.split(ALGO_SEPARATOR)
        if algo != "pbkdf2_sha256":
            return False
        salt = base64.urlsafe_b64decode(salt_b64)
        expected = base64.urlsafe_b64decode(digest_b64)
        got = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
        return hmac.compare_digest(got, expected)
    except (ValueError, TypeError):
        return False


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _b64url_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def _sign(payload_b64: str) -> str:
    secret = settings.secret_key.encode("utf-8")
    digest = hmac.new(secret, payload_b64.encode("utf-8"), hashlib.sha256).digest()
    return _b64url(digest)


def create_access_token(sub: str, expires_minutes: int | None = None) -> str:
    minutes = expires_minutes or settings.access_token_minutes
    now = int(time.time())
    body = {"sub": str(sub), "iat": now, "exp": now + minutes * 60}
    header = {"alg": settings.jwt_algorithm, "typ": "JWT"}
    header_b64 = _b64url(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64url(json.dumps(body, separators=(",", ":")).encode())
    signing_input = f"{header_b64}.{payload_b64}"
    return f"{signing_input}.{_sign(signing_input)}"


def decode_access_token(token: str) -> dict | None:
    try:
        header_b64, payload_b64, signature = token.split(".")
        if not hmac.compare_digest(signature, _sign(f"{header_b64}.{payload_b64}")):
            return None
        body = json.loads(_b64url_decode(payload_b64))
        if int(body.get("exp", 0)) < int(time.time()):
            return None
        return body
    except (ValueError, TypeError, json.JSONDecodeError):
        return None


def to_iso(value: datetime | date | None) -> str | None:
    return value.isoformat() if value else None
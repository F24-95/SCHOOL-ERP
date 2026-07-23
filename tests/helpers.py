from datetime import UTC, datetime, timedelta

from jose import jwt

from app.api.config import settings


def create_test_token(
    sub: str,
    role: str = "admin",
    expires_delta: timedelta | None = None,
) -> str:
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=30))
    payload = {"sub": sub, "role": role, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

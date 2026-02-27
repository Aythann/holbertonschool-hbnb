import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def require_str(name: str, value, *, min_len=1, max_len=255) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    v = value.strip()
    if len(v) < min_len:
        raise ValueError(f"{name} must be at least {min_len} chars")
    if len(v) > max_len:
        raise ValueError(f"{name} must be at most {max_len} chars")
    return v


def require_email(value) -> str:
    v = require_str("email", value, min_len=3, max_len=254).lower()
    if not EMAIL_RE.match(v):
        raise ValueError("email is invalid")
    return v


def require_float(name: str, value, *, min_value=None, max_value=None) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a number")

    if min_value is not None and v < min_value:
        raise ValueError(f"{name} must be >= {min_value}")
    if max_value is not None and v > max_value:
        raise ValueError(f"{name} must be <= {max_value}")
    return v


def require_int(name: str, value, *, min_value=None, max_value=None) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer")
    try:
        v = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be an integer")

    if min_value is not None and v < min_value:
        raise ValueError(f"{name} must be >= {min_value}")
    if max_value is not None and v > max_value:
        raise ValueError(f"{name} must be <= {max_value}")
    return v
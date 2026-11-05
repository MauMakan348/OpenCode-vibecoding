from app.errors import ValidationError


def require_text(value, field):
    """Return a trimmed non-empty string or raise ValidationError."""
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} is required")
    return value.strip()


def require_non_negative_int(value, field):
    """Return an int >= 0. Booleans are rejected."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValidationError(f"{field} must be a non-negative integer")
    return value


def require_positive_int(value, field):
    """Return an int > 0. Booleans are rejected."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValidationError(f"{field} must be a positive integer")
    return value

"""Security utilities for password hashing and verification."""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    Args:
        password: Plain-text password to hash

    Returns:
        str: Bcrypt hashed password

    Note:
        Bcrypt has a 72-byte limit. We truncate to 72 bytes to prevent
        ValueError while maintaining password security (72 bytes is plenty).

    Example:
        >>> hashed = hash_password("SecurePass123")
        >>> print(hashed)
        $2b$12$EixZaYVK1fsbw1ZfbX3OXe...
    """
    # Bcrypt has a 72-byte limit, truncate if necessary
    # 72 bytes is still more than enough for secure passwords
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    # Hash the password with 12 rounds (recommended for security)
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password.

    Args:
        plain_password: Plain-text password to verify
        hashed_password: Bcrypt hashed password to check against

    Returns:
        bool: True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("SecurePass123")
        >>> verify_password("SecurePass123", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    # Truncate to 72 bytes to match hashing behavior
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password meets security requirements.

    Requirements (from FR-003):
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 number

    Args:
        password: Plain-text password to validate

    Returns:
        tuple: (is_valid, error_message)
            - is_valid: True if password meets requirements
            - error_message: Empty string if valid, error description if invalid

    Example:
        >>> is_valid, msg = validate_password_strength("Weak")
        >>> print(is_valid, msg)
        False Password must be at least 8 characters
        >>> is_valid, msg = validate_password_strength("SecurePass123")
        >>> print(is_valid, msg)
        True
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least 1 uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least 1 lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least 1 number"

    return True, ""

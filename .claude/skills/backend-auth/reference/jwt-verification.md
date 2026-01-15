# JWT Verification Reference

Complete guide to JWT verification in FastAPI.

## Dependencies

```bash
pip install python-jose passlib[bcrypt]
```

## Environment Variables

```bash
# .env
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Verification Function

```python
from jose import JWTError, jwt
from fastapi import HTTPException
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

def verify_jwt_token(token: str) -> dict:
    """
    Verify JWT token and return payload.
    Raises HTTPException 401 if invalid.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )

def extract_user_id(token: str) -> str:
    """
    Extract user_id from JWT token.
    """
    payload = verify_jwt_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token does not contain user identifier"
        )

    return user_id
```

## Token Structure

Tokens from Better Auth contain:

```json
{
  "sub": "user-uuid-or-id",
  "exp": 1704067200,
  "iat": 1704063600,
  "iss": "better-auth"
}
```

- **sub**: Subject (user ID)
- **exp**: Expiration time
- **iat**: Issued at time
- **iss**: Issuer

## Verification Options

```python
from jose import jwt

# Full verification
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM],
    options={
        "verify_exp": True,     # Verify expiration
        "verify_iat": True,     # Verify issued at
        "verify_iss": True,     # Verify issuer
        "require": ["sub", "exp"]  # Required claims
    }
)

# Skip expiration check (not recommended for production)
payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=[ALGORITHM],
    options={"verify_exp": False}
)
```

## Error Handling

```python
from jose import JWTError, ExpiredSignatureError, jwt

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
except ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token has expired")
except JWTError as e:
    raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
```

## Common Errors

| Error | Status | Message |
|-------|--------|---------|
| Missing header | 401 | Authorization header is required |
| Invalid format | 401 | Use: Bearer <token> |
| Invalid signature | 401 | Invalid token |
| Expired token | 401 | Token has expired |
| Missing sub claim | 401 | Token does not contain user identifier |

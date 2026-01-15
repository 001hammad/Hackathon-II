# Common Attacks and Prevention

Security vulnerabilities and how to prevent them.

## 1. Token Theft

### Attack
Attacker steals JWT from network or client.

### Prevention
```python
# Use HTTPS only
# Server sets: Strict-Transport-Security: max-age=31536000; includeSubDomains

# Use httpOnly, Secure cookies (Better Auth does this)
```

## 2. Token Replay

### Attack
Attacker reuses a valid token.

### Prevention
```python
# Short token expiration (15-30 minutes)
# Store token IDs in a blacklist (Redis)
# Use refresh tokens for longer sessions
```

## 3. User Isolation Bypass

### Attack
User modifies user_id in URL or request body.

### Prevention
```python
# NEVER trust user_id from URL
# ALWAYS extract user_id from JWT
# ALWAYS filter by user_id from JWT

# BAD:
task = db.query(Task).filter(Task.id == task_id).first()

# GOOD:
task = db.query(Task).filter(
    Task.id == task_id,
    Task.user_id == current_user_id  # From JWT!
).first()
```

## 4. SQL Injection

### Attack
Attacker injects SQL through input parameters.

### Prevention
```python
# Use parameterized queries (SQLAlchemy does this)
# Never concatenate user input into queries

# BAD:
query = f"SELECT * FROM tasks WHERE id = '{task_id}'"

# GOOD:
task = db.query(Task).filter(Task.id == task_id).first()
```

## 5. Privilege Escalation

### Attack
Regular user accesses admin resources.

### Prevention
```python
# Check user role in addition to user_id
# Use role-based access control (RBAC)
# Return 404 (not 403) to avoid revealing resource exists
```

## 6. Token Forgery

### Attack
Attacker creates fake tokens with forged user_id.

### Prevention
```python
# Use strong SECRET_KEY (32+ random characters)
# Use HMAC-SHA256 algorithm
# Verify token signature

# BAD: Using weak secret
SECRET_KEY = "password123"

# GOOD: Using random secret
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")  # 32+ random chars
```

## 7. Cross-Site Request Forgery (CSRF)

### Attack
Attacker tricks user into making authenticated requests.

### Prevention
```python
# Use SameSite cookies
# Validate Origin/Referer headers
# Use CSRF tokens for state-changing operations
```

## 8. Information Disclosure

### Attack
Error messages reveal sensitive information.

### Prevention
```python
# Use generic error messages
# Don't reveal if email exists in login

# BAD:
raise HTTPException(status_code=401, detail="Email not found")

# GOOD:
raise HTTPException(status_code=401, detail="Invalid email or password")
```

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Strong SECRET_KEY (32+ random characters)
- [ ] Short token expiration (15-30 minutes)
- [ ] Always verify JWT signature
- [ ] Always filter by user_id from JWT
- [ ] Use parameterized queries
- [ ] Generic error messages
- [ ] Return 404 (not 403) for ownership errors
- [ ] Log authentication failures
- [ ] Rate limit authentication endpoints
- [ ] Use httpOnly, Secure cookies
- [ ] Implement CORS properly

# Security Best Practices

Frontend authentication security guidelines.

## Token Storage

✅ **DO: Use httpOnly cookies (Better Auth default)**
```typescript
// Better Auth stores tokens in httpOnly cookies automatically
// No manual storage needed!
```

❌ **DON'T: Store JWT in localStorage**
```typescript
// NEVER DO THIS - vulnerable to XSS
localStorage.setItem('token', jwt)
```

## HTTPS

✅ Always use HTTPS in production
```bash
NEXT_PUBLIC_API_URL=https://api.example.com
```

## Password Requirements

✅ Minimum 8 characters
✅ Include validation in signup form
```typescript
if (password.length < 8) {
  setError("Password must be at least 8 characters")
  return
}
```

## Error Handling

✅ Generic error messages (don't reveal if email exists)
```typescript
setError("Invalid email or password")
```

❌ Don't reveal specific errors
```typescript
// DON'T: setError("Email not found")
// DON'T: setError("Wrong password")
```

## Auto-redirect on 401

```typescript
if (response.status === 401) {
  window.location.href = "/login"
}
```

## CSRF Protection

Better Auth handles CSRF automatically with httpOnly cookies.

## Rate Limiting

Backend should rate limit login attempts (3-5 per minute).

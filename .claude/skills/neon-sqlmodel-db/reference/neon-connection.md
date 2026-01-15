# Neon Connection Reference

Comprehensive guide to connecting to Neon Serverless PostgreSQL.

## Connection String Format

### Standard Connection String

```
postgresql://<username>:<password>@<host>.aws.neon.tech/<database>?sslmode=require
```

Example:
```
postgresql://alex:AbC123dEf@ep-cool-moon-123456.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Async Connection String

```
postgresql+asyncpg://<username>:<password>@<host>.aws.neon.tech/<database>?sslmode=require
```

### Connection String Components

| Component | Description | Example |
|-----------|-------------|---------|
| `username` | Neon database username | `alex` |
| `password` | Neon database password | `AbC123dEf` |
| `host` | Endpoint host | `ep-cool-moon-123456` |
| `region` | AWS region | `us-east-1` |
| `database` | Database name | `neondb` |
| `sslmode` | SSL requirement | `require` (required) |

## Environment Variables

### Required Variables

```bash
# .env
DATABASE_URL="postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"
DATABASE_URL_ASYNC="postgresql+asyncpg://user:pass@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"
```

### Optional Variables

```bash
# Connection pool settings
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_TIMEOUT=10

# SSL options
DATABASE_SSL_CERT_PATH="/path/to/cert.pem"
```

## Neon-Specific Configuration

### Serverless Connection Settings

```python
# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine

async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require",
    # Neon serverless-specific settings
    pool_size=1,  # Start with minimal connections
    max_overflow=5,  # Allow scaling
    pool_pre_ping=True,  # Verify connection health
    pool_recycle=300,  # Recycle more frequently for serverless
    connect_args={
        "server_settings": {
            "application_name": "my_todo_app",
            "timezone": "UTC"
        },
        "timeout": 10,
        "command_timeout": 60
    }
)
```

### Connection Timeout Configuration

```python
# Different timeout scenarios

# Query timeout (statement_timeout)
await session.execute(
    text("SET statement_timeout = '30s'")
)

# Lock wait timeout
await session.execute(
    text("SET lock_timeout = '5s'")
)

# Idle connection timeout (server-side)
await session.execute(
    text("SET idle_in_transaction_session_timeout = '5m'")
)
```

## SSL Configuration

### Required SSL Settings

Neon requires SSL for all connections. The `sslmode=require` parameter ensures this.

```python
# Explicit SSL configuration
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

async_engine = create_async_engine(
    DATABASE_URL_ASYNC,
    connect_args={
        "ssl": ssl_context
    }
)
```

### Self-Signed Certificate (Development)

```python
# For local development with self-signed cert
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async_engine = create_async_engine(
    DATABASE_URL_ASYNC,
    connect_args={
        "ssl": ssl_context
    }
)
```

## Connection Pooling

### Neon Pooler vs Direct Connection

```python
# Direct connection (default)
# Connects directly to the compute endpoint
DATABASE_URL_DIRECT = "postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Pooled connection (connection pooling)
# Uses Neon's built-in connection pooler
DATABASE_URL_POOLED = "postgres://user:pass@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require&pool=true"
```

### Pool Configuration Recommendations

```python
# Recommended pool settings for Neon
from sqlalchemy.ext.asyncio import create_async_engine

async_engine = create_async_engine(
    DATABASE_URL_ASYNC,
    # Pool sizing
    pool_size=5,              # Base connections
    max_overflow=10,          # Additional connections under load
    pool_recycle=1800,        # Recycle connections every 30 min

    # Connection health
    pool_pre_ping=True,       # Verify before use
    pool_reset_on_return="commit",  # Reset after commit

    # Timeouts
    pool_timeout=30,          # Wait up to 30s for connection
    max_overflow=10,          # Max additional connections

    connect_args={
        "timeout": 10,        # Connection timeout
        "command_timeout": 60 # Query timeout
    }
)
```

### Pool Monitoring

```python
# Monitor pool health
from app.database import async_engine

def get_pool_metrics():
    pool = async_engine.pool

    return {
        "current_size": pool.size(),
        "available_connections": pool.checkedin(),
        "used_connections": pool.checkedout(),
        "overflow": pool.overflow(),
        "invalid_connections": pool.invalid()
    }


# Check before heavy operations
async def ensure_pool_health():
    metrics = get_pool_metrics()

    if metrics["used_connections"] >= pool.size():
        raise Exception("Pool exhausted, cannot acquire connection")

    return metrics
```

## Regional Endpoints

### Available Regions

```python
# Neon regional endpoints
REGIONS = {
    "us-east-1": "aws.neon.tech",
    "us-west-2": "aws.neon.tech",
    "eu-west-1": "aws.neon.tech",
    "ap-northeast-1": "aws.neon.tech"
}


def build_connection_string(
    username: str,
    password: str,
    endpoint: str,
    database: str = "neondb",
    region: str = "us-east-1"
) -> str:
    """Build Neon connection string."""
    host = f"{endpoint}.{region}"
    return f"postgresql://{username}:{password}@{host}/{database}?sslmode=require"


# Multi-region example
EU_CONNECTION = build_connection_string(
    username="eu_user",
    password="password",
    endpoint="ep-eu-endpoint",
    database="neondb",
    region="eu-west-1"
)
```

## Connection Testing

### Test Connection Health

```python
# app/tests/test_connection.py
import pytest
from sqlalchemy import text
from app.database import AsyncSessionLocal


@pytest.mark.asyncio
async def test_database_connection():
    """Verify database is reachable."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_ssl_connection():
    """Verify SSL is enforced."""
    from sqlalchemy import create_engine

    # This should work with sslmode=require
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SHOW ssl"))
        assert result.scalar() == "on"


@pytest.mark.asyncio
async def test_connection_timeout():
    """Verify timeout settings work."""
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(
        DATABASE_URL_ASYNC,
        connect_args={"timeout": 1}  # 1 second timeout
    )

    try:
        async with engine.connect() as conn:
            await asyncio.sleep(2)  # Should timeout
    except Exception as e:
        assert "timeout" in str(e).lower() or "timed out" in str(e).lower()
```

### Connection Troubleshooting

```python
# Common connection errors and solutions

# Error: "connection refused"
# Solution: Check endpoint URL and ensure Neon compute is active

# Error: "ssl negotiation failed"
# Solution: Add ?sslmode=require to connection string

# Error: "password authentication failed"
# Solution: Verify credentials in connection string

# Error: "remaining connection slots are reserved"
# Solution: Reduce pool_size or wait for connections to release

# Error: "could not translate host name"
# Solution: Check endpoint name is correct


def diagnose_connection(connection_string: str) -> dict:
    """Diagnose common connection issues."""
    issues = []

    if "sslmode=require" not in connection_string:
        issues.append("Missing sslmode=require parameter")

    if "@ep-" not in connection_string:
        issues.append("Invalid endpoint format")

    if "neondb" not in connection_string:
        issues.append("Database name should be 'neondb'")

    return {
        "healthy": len(issues) == 0,
        "issues": issues
    }
```

## Connection String Security

### Environment-Based Configuration

```python
# app/config.py
import os
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration from environment."""
    DATABASE_URL: str
    DATABASE_URL_ASYNC: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_TIMEOUT: int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Never log or expose connection strings
settings = DatabaseSettings()

# Use in engine creation
DATABASE_URL = settings.DATABASE_URL_ASYNC
```

### Credential Rotation

```python
# For rotating credentials without downtime

def rotate_credentials(
    old_url: str,
    new_url: str
) -> None:
    """
    Rotate database credentials with zero downtime.

    Process:
    1. Update environment with new credentials
    2. Create new engine with fresh connections
    3. Let old connections drain
    4. Deprecate old engine
    """
    import os
    from sqlalchemy.ext.asyncio import create_async_engine

    # Update environment
    os.environ["DATABASE_URL_ASYNC"] = new_url

    # Create new engine
    new_engine = create_async_engine(new_url)

    # Test new engine
    async with new_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    # Replace old engine reference
    global async_engine
    async_engine = new_engine
```

## Connection in Different Contexts

### FastAPI Application

```python
# app/main.py
from fastapi import FastAPI
from app.database import get_async_session, async_engine
from sqlalchemy import event

app = FastAPI()


# Close connections on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    await async_engine.dispose()


# Usage in routes
@app.get("/tasks")
async def get_tasks(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Task))
    return result.scalars().all()
```

### Background Tasks

```python
# For Celery or similar background workers

def get_background_session():
    """Session factory for background tasks."""
    from app.database import AsyncSessionLocal

    return AsyncSessionLocal()


async def background_task(task_id: int):
    """Task running in background worker."""
    session = get_background_session()

    try:
        async with session:
            # Do work
            pass
    finally:
        await session.close()
```

### CLI Scripts

```python
# scripts/seed_data.py
import asyncio
from app.database import get_session_context
from app.models.task import Task


async def seed_database():
    """Seed database with sample data."""
    async with get_session_context() as session:
        tasks = [
            Task(title="Sample task 1", user_id="test-user"),
            Task(title="Sample task 2", user_id="test-user"),
        ]

        for task in tasks:
            session.add(task)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_database())
```

## Performance Optimization

### Prepared Statement Caching

```python
# Enable prepared statement caching for better performance
async_engine = create_async_engine(
    DATABASE_URL_ASYNC,
    # SQLAlchemy 2.0 style
    future=True,
    echo=False,
    pool_pre_ping=True
)

# Use with sessions
async with async_engine.connect() as conn:
    # Statements are cached automatically
    await conn.execute(select(Task).where(Task.id == 1))
    await conn.execute(select(Task).where(Task.id == 2))
```

### Batch Operations

```python
# Use executemany for batch inserts
from sqlalchemy.dialects.postgresql import insert

async def bulk_insert_tasks(tasks_data: list[dict], session: AsyncSession):
    """Efficient bulk insert."""
    stmt = insert(Task).values(tasks_data).on_conflict_do_nothing()
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount
```

"""Core configuration module - loads environment variables."""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Application settings loaded from environment variables.

    All sensitive configuration (database URLs, secrets) should be
    stored in environment variables, never hardcoded.
    """

    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_URL_ASYNC: str = os.getenv("DATABASE_URL_ASYNC", "")

    # Authentication Configuration
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")
    )  # 24 hours default

    # Application Configuration
    APP_NAME: str = "Phase II Todo API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # CORS Configuration
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Next.js frontend
        "http://127.0.0.1:3000",
    ]

    def validate(self) -> None:
        """
        Validate that all required environment variables are set.
        Raises ValueError if any required variables are missing.
        """
        required_vars = {
            "DATABASE_URL": self.DATABASE_URL,
            "BETTER_AUTH_SECRET": self.BETTER_AUTH_SECRET,
        }

        missing_vars = [
            var_name for var_name, var_value in required_vars.items() if not var_value
        ]

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        # Validate BETTER_AUTH_SECRET length
        if len(self.BETTER_AUTH_SECRET) < 32:
            raise ValueError(
                "BETTER_AUTH_SECRET must be at least 32 characters long for security"
            )


# Create global settings instance
settings = Settings()

# Validate settings on module import (will raise ValueError if misconfigured)
try:
    settings.validate()
    print("Configuration loaded successfully")
except ValueError as e:
    print(f"Configuration validation failed: {e}")
    print("Please check your .env file and ensure all required variables are set")

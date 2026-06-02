""" 
© 2026 Rozendox. 
All rights reserved.
Proprietary and confidential.  

api_integration_broker.config.py

SINGLE RESPONSIBILITY PRINCIPLE: This module is responsible for
managing the configuration settings of the project.

"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class to manage configuration settings for the project.
    """
    PROJECT_NAME: str = "Integration Hub"
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str
    
    # Security
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Encryption key for external credentials (AES-256)
    ENCRYPTION_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

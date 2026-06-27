from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    ENV: str = "development"
    PORT: int = 3000
    
    META_APP_ID: str
    META_APP_SECRET: str
    META_VERIFY_TOKEN: str
    META_ACCESS_TOKEN: str
    META_PHONE_NUMBER_ID: str
    META_API_URL: str = "https://graph.facebook.com/v19.0"
    
    MONGODB_URI: Optional[str] = None
    REDIS_URL: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL: str = "google/gemini-2.0-flash-exp:free"
    FALLBACK_MODEL: str = "deepseek/deepseek-r1:free"
    HUBSPOT_API_KEY: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASS: Optional[str] = None

    # Ensure the .env file is correctly located when the package is executed
    # from the project root. The original relative path ".env" looked for the file
    # in the current working directory, which may not be the package directory.
    # By specifying the path relative to this file, we guarantee the environment
    # variables are loaded.
    model_config = SettingsConfigDict(env_file="whatsapp_bots/.env", extra="ignore")

settings = Settings()

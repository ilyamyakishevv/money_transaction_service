from pathlib import Path

from .base import BaseSetting

BASE_DIR = Path(__file__).parent.parent

class AppSettings(BaseSetting):
    BASE_DIR: Path = BASE_DIR
    ENVIRONMENT: str = "local"
    DEBUG: bool = False
    APP_RELEASE: str = "0.0.1"
    UVICORN_WORKERS: int = 1

    AUTH_SERVICE_NAME: str = "Authentication Service"
    AUTH_SERVICE_VERSION: str = "1.0.0"
    AUTH_SERVICE_PORT: int = 8001
    AUTH_API_VERSION: str = "v1"

    TRANSACTION_SERVICE_NAME: str = "Money Transaction Service"
    TRANSACTION_SERVICE_VERSION: str = "1.0.0"
    TRANSACTION_SERVICE_PORT: int = 8002
    TRANSACTION_API_VERSION: str = "v1"

    EXTERNAL_SERVICE_SCHEMA: str = "http"
    EXTERNAL_SERVICE_HOST: str = "localhost"
    EXTERNAL_SERVICE_PORT: int = 80

    @property
    def auth_service_url(self) -> str:
        return (
            f"{self.EXTERNAL_SERVICE_SCHEMA}://"
            f"{self.EXTERNAL_SERVICE_HOST}:"
            f"{self.AUTH_SERVICE_PORT}/api/"
            f"{self.AUTH_API_VERSION}"
        )

    @property
    def transaction_service_url(self) -> str:
        return (
            f"{self.EXTERNAL_SERVICE_SCHEMA}://"
            f"{self.EXTERNAL_SERVICE_HOST}:"
            f"{self.TRANSACTION_SERVICE_PORT}/api/"
            f"{self.TRANSACTION_API_VERSION}"
        )

    @property
    def full_url(self) -> str:
        return (
            f"{self.EXTERNAL_SERVICE_SCHEMA}://"
            f"{self.EXTERNAL_SERVICE_HOST}:"
            f"{self.EXTERNAL_SERVICE_PORT}"
        )

    @property
    def front_url(self) -> str:
        return (
            f"{self.EXTERNAL_SERVICE_SCHEMA}://"
            f"{self.EXTERNAL_SERVICE_HOST}"
        )


class DBSettings(BaseSetting):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


class JWTSettings(BaseSetting):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES: int  
    JWT_REFRESH_TOKEN_EXPIRES: int  


class LogSettings(BaseSetting):
    LOG_FILE: str = "/logs/service.log"
    LOG_LEVEL: str = "INFO"


class PasswordSettings(BaseSetting):
    PASSWORD_SCORE_MIN: int = 1



app_settings = AppSettings()
db_settings = DBSettings()
jwt_settings = JWTSettings()
log_settings = LogSettings()
password_settings = PasswordSettings()

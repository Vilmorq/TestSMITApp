from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SCHEMA: str
    HOSTNAME: str
    API_PATH: str
    DEBUG: bool
    BACKEND_CORS_ORIGINS: str

    @property
    def service_url(self) -> str:
        return f"{self.SCHEMA}://{self.HOSTNAME}{self.API_PATH}"

    @property
    def get_backend_cors_origins(self) -> list[str]:
        return self.BACKEND_CORS_ORIGINS.split(",")


settings = Settings()

from pydantic_settings import BaseSettings

from app.core.settings.base import settings


class ApiSettings(BaseSettings):
    root_path: str = settings.API_PATH
    servers: list[dict[str, str]] = [
        {"url": f"{settings.service_url}", "description": ""}
    ]
    root_path_in_servers: bool = False
    openapi_url: str = "/openapi.json"
    version: str = "1.0.1"
    docs_url: str | None = "/docs" if settings.DEBUG else None
    redoc_url: str | None = "/redoc" if settings.DEBUG else None


api_settings = ApiSettings()

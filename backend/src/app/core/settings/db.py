from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    USER: str
    PASSWORD: str
    SERVER: str
    PORT: int
    DB: str
    ASYNC_PREFIX: str

    @property
    def db_uri(self) -> str:
        return f"{self.USER}:{self.PASSWORD}@{self.SERVER}:{self.PORT}/{self.DB}"

    @property
    def db_url(self) -> str:
        return f"{self.ASYNC_PREFIX}{self.db_uri}"

    class Config:
        env_prefix = "POSTGRES_"


db_settings = DBSettings()

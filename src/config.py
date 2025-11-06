from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Database
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    # Security
    SECRET_KEY: str
    ALGORITHM:  str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def sync_database_url(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


config = Config()


__all__ = [
    'config'
]

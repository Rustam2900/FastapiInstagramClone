from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite_db: str
    sqlite_db_url: str

    class Config:
        env_file = '../../.env'


settings = Settings()

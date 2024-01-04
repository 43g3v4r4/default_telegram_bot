from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # DB_HOST: str
    # DB_PORT: int
    # DB_USER: str
    # DB_PASS: str
    # DB_NAME: str
    BOT_TOKEN: str

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DATABASE_URL_psycopg(self):
        # DSN
        # postgresql+psycopg://postgres:postgres@localhost:5432/sa
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DATABASE_URL_sqlite(self):
        # sqlite:////path/to/database.db
        return f'sqlite:///db/base.db'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
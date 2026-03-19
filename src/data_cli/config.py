from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "data-cli"
    log_level: str = "INFO"

    class Config:
        env_prefix = "DATA_CLI_"


settings = Settings()
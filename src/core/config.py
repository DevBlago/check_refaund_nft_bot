from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class BotConfig(BaseModel):
    token: SecretStr
    admin: str

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra = "ignore",
        env_file_encoding="utf-8",
        env_nested_delimiter="_"
    )

    bot: BotConfig

settings = Settings()
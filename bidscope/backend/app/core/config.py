from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_env: str = "local"
    storage_dir: Path = Field(default=Path("./storage"), alias="BIDSCOPE_STORAGE_DIR")
    bid_api_base_url: str = Field(default="", alias="BID_API_BASE_URL")
    bid_api_key: str = Field(default="", alias="BID_API_KEY")

settings = Settings()
settings.storage_dir.mkdir(parents=True, exist_ok=True)

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """项目配置。企业项目中一般把配置统一放在 core/config.py。"""

    app_name: str = "Campus QA Agent"
    app_env: str = "dev"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    web_port: int = 8501

    llm_provider: str = "mock"
    llm_base_url: str = ""
    llm_model: str = "qwen-plus"
    llm_api_key: str = ""
    llm_timeout: int = 60

    knowledge_base_dir: str = "data/knowledge_base"
    upload_dir: str = "data/uploads"
    log_dir: str = "logs"
    chunk_size: int = 450
    chunk_overlap: int = 80
    default_top_k: int = 4
    enable_local_fallback: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def knowledge_path(self) -> Path:
        return Path(self.knowledge_base_dir)

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir)

    @property
    def log_path(self) -> Path:
        return Path(self.log_dir)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.knowledge_path.mkdir(parents=True, exist_ok=True)
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    settings.log_path.mkdir(parents=True, exist_ok=True)
    return settings


settings = get_settings()

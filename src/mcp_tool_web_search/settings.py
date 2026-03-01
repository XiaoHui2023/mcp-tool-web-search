from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

def find_env_file() -> Path | None:
    """从当前文件所在目录开始，逐层向上查找 .env"""
    start = Path(__file__).resolve().parent
    for parent in [start, *start.parents]:
        env_file = parent / ".env"
        if env_file.is_file():
            return env_file
    return None

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_env_file(),
        env_file_encoding="utf-8",
    )

    llm_api_key: str
    "LLM API 密钥"
    llm_base_url: str
    "LLM 基础 URL"
    llm_model: str
    "LLM 模型"
    bocha_api_key: str
    "Bocha API 密钥"

settings = Settings()
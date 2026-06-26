from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AUTODATA_")

    app_name: str = "autodata-agent"
    environment: str = "dev"
    max_rounds: int = Field(default=8, ge=1)
    weak_rollouts: int = Field(default=2, ge=1)
    strong_rollouts: int = Field(default=2, ge=1)
    acceptance_gap: float = Field(default=0.25, ge=0.0)
    min_quality_score: float = Field(default=0.7, ge=0.0, le=1.0)
    max_budget_steps: int = Field(default=50, ge=1)
    trace_store_dir: str = "artifacts/traces"
    dataset_store_dir: str = "artifacts/datasets"

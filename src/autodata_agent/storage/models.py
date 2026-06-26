from pydantic import BaseModel, Field


class RoundMetrics(BaseModel):
    round_id: int = Field(ge=1)
    accepted: bool
    weak_score: float = Field(ge=0.0, le=1.0)
    strong_score: float = Field(ge=0.0, le=1.0)
    quality_score: float = Field(ge=0.0, le=1.0)

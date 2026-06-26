from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class AttemptStatus(StrEnum):
    accepted = "accepted"
    rejected = "rejected"


class CandidateExample(BaseModel):
    prompt: str
    expected_schema: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SolverRollout(BaseModel):
    solver_name: str
    output_text: str
    parsed_output: dict[str, Any] = Field(default_factory=dict)
    latency_ms: int = Field(default=0, ge=0)
    tokens_used: int = Field(default=0, ge=0)


class EvalScore(BaseModel):
    name: str
    score: float = Field(ge=0.0, le=1.0)
    rationale: str


class AttemptTrace(BaseModel):
    round_id: int
    candidate: CandidateExample
    weak_rollouts: list[SolverRollout]
    strong_rollouts: list[SolverRollout]
    weak_score: float = Field(ge=0.0, le=1.0)
    strong_score: float = Field(ge=0.0, le=1.0)
    quality_score: float = Field(ge=0.0, le=1.0)
    accepted: bool
    failure_reasons: list[str] = Field(default_factory=list)


class AcceptanceDecision(BaseModel):
    status: AttemptStatus
    reason: str
    score_gap: float
    quality_score: float


class PromptVariant(BaseModel):
    variant_id: str
    prompt_template: str
    parent_id: str | None = None
    fitness: float = Field(default=0.0, ge=0.0, le=1.0)
    generation: int = Field(default=0, ge=0)

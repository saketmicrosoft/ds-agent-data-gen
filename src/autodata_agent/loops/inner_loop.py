from dataclasses import dataclass

from autodata_agent.agents.base import ChallengerAgent, SolverAgent
from autodata_agent.config import Settings
from autodata_agent.evaluators.base import Evaluator
from autodata_agent.schemas import AcceptanceDecision, AttemptStatus, AttemptTrace
from autodata_agent.storage.repository import ArtifactRepository


@dataclass
class InnerLoopResult:
    accepted: int
    rejected: int


class InnerLoopRunner:
    def __init__(
        self,
        settings: Settings,
        challenger: ChallengerAgent,
        weak_solver: SolverAgent,
        strong_solver: SolverAgent,
        evaluators: list[Evaluator],
        repository: ArtifactRepository,
    ) -> None:
        self.settings = settings
        self.challenger = challenger
        self.weak_solver = weak_solver
        self.strong_solver = strong_solver
        self.evaluators = evaluators
        self.repository = repository

    def run(self, budget_steps: int) -> InnerLoopResult:
        feedback: str | None = None
        accepted = 0
        rejected = 0

        for round_id in range(1, budget_steps + 1):
            candidate = self.challenger.propose(feedback)

            weak_rollouts = [
                self.weak_solver.solve(candidate)
                for _ in range(self.settings.weak_rollouts)
            ]
            strong_rollouts = [
                self.strong_solver.solve(candidate)
                for _ in range(self.settings.strong_rollouts)
            ]

            scores = [e.score(candidate, weak_rollouts, strong_rollouts) for e in self.evaluators]
            weak_score = min(1.0, sum(s.score for s in scores) / max(1, len(scores)) * 0.8)
            strong_score = min(1.0, sum(s.score for s in scores) / max(1, len(scores)))

            decision = self._decide(weak_score, strong_score)
            trace = AttemptTrace(
                round_id=round_id,
                candidate=candidate,
                weak_rollouts=weak_rollouts,
                strong_rollouts=strong_rollouts,
                weak_score=weak_score,
                strong_score=strong_score,
                quality_score=decision.quality_score,
                accepted=decision.status == AttemptStatus.accepted,
                failure_reasons=(
                    []
                    if decision.status == AttemptStatus.accepted
                    else [decision.reason]
                ),
            )
            self.repository.write_trace(trace)

            if decision.status == AttemptStatus.accepted:
                accepted += 1
                self.repository.write_dataset_example(trace)
                feedback = "Increase novelty and task complexity while preserving verifiability."
            else:
                rejected += 1
                feedback = f"Rejected because: {decision.reason}"

        return InnerLoopResult(accepted=accepted, rejected=rejected)

    def _decide(self, weak_score: float, strong_score: float) -> AcceptanceDecision:
        gap = max(0.0, strong_score - weak_score)
        quality_score = strong_score
        if gap >= self.settings.acceptance_gap and quality_score >= self.settings.min_quality_score:
            return AcceptanceDecision(
                status=AttemptStatus.accepted,
                reason="accepted",
                score_gap=gap,
                quality_score=quality_score,
            )

        return AcceptanceDecision(
            status=AttemptStatus.rejected,
            reason="insufficient_gap_or_quality",
            score_gap=gap,
            quality_score=quality_score,
        )

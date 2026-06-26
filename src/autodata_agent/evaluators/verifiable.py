from autodata_agent.evaluators.base import Evaluator
from autodata_agent.schemas import CandidateExample, EvalScore, SolverRollout


class CapabilityGapEvaluator(Evaluator):
    """Scores whether strong solver outputs look materially better than weak outputs."""

    @property
    def name(self) -> str:
        return "capability_gap"

    def score(
        self,
        candidate: CandidateExample,
        weak_rollouts: list[SolverRollout],
        strong_rollouts: list[SolverRollout],
    ) -> EvalScore:
        weak_avg = sum(len(r.output_text) for r in weak_rollouts) / max(1, len(weak_rollouts))
        strong_avg = sum(len(r.output_text) for r in strong_rollouts) / max(1, len(strong_rollouts))
        gap = max(0.0, strong_avg - weak_avg)
        normalized = min(1.0, gap / max(1.0, len(candidate.prompt)))
        return EvalScore(
            name=self.name,
            score=normalized,
            rationale=f"Computed normalized length gap: {normalized:.3f}",
        )

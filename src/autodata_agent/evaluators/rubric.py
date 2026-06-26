from autodata_agent.evaluators.base import Evaluator
from autodata_agent.schemas import CandidateExample, EvalScore, SolverRollout


class RubricJudgeEvaluator(Evaluator):
    """Simple rubric proxy; swap with a real LLM judge in production."""

    @property
    def name(self) -> str:
        return "rubric_judge"

    def score(
        self,
        candidate: CandidateExample,
        weak_rollouts: list[SolverRollout],
        strong_rollouts: list[SolverRollout],
    ) -> EvalScore:
        del weak_rollouts
        richness = sum(len(r.parsed_output) for r in strong_rollouts) / max(1, len(strong_rollouts))
        score = min(1.0, 0.5 + 0.1 * richness)
        rationale = (
            f"Rubric proxy richness score={score:.3f} "
            f"for prompt size={len(candidate.prompt)}"
        )
        return EvalScore(
            name=self.name,
            score=score,
            rationale=rationale,
        )

import time

from autodata_agent.agents.base import SolverAgent
from autodata_agent.schemas import CandidateExample, SolverRollout


class TemplateSolverAgent(SolverAgent):
    def __init__(self, name: str, capability_hint: float) -> None:
        self._name = name
        self._capability_hint = capability_hint

    @property
    def name(self) -> str:
        return self._name

    def solve(self, candidate: CandidateExample) -> SolverRollout:
        start = time.perf_counter()
        answer_text = f"{self._name} response for: {candidate.prompt}"
        parsed_output = {
            "answer": answer_text,
            "capability_hint": self._capability_hint,
        }
        latency_ms = int((time.perf_counter() - start) * 1000)
        return SolverRollout(
            solver_name=self._name,
            output_text=answer_text,
            parsed_output=parsed_output,
            latency_ms=latency_ms,
            tokens_used=max(1, len(candidate.prompt) // 4),
        )

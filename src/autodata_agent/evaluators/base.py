from abc import ABC, abstractmethod

from autodata_agent.schemas import CandidateExample, EvalScore, SolverRollout


class Evaluator(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def score(
        self,
        candidate: CandidateExample,
        weak_rollouts: list[SolverRollout],
        strong_rollouts: list[SolverRollout],
    ) -> EvalScore:
        raise NotImplementedError

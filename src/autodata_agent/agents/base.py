from abc import ABC, abstractmethod

from autodata_agent.schemas import CandidateExample, SolverRollout


class ChallengerAgent(ABC):
    @abstractmethod
    def propose(self, feedback: str | None = None) -> CandidateExample:
        raise NotImplementedError


class SolverAgent(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def solve(self, candidate: CandidateExample) -> SolverRollout:
        raise NotImplementedError

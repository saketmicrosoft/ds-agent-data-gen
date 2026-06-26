import re

from autodata_agent.schemas import CandidateExample


class QualityValidator:
    def __init__(self) -> None:
        self._seen_prompts: set[str] = set()

    def validate(self, candidate: CandidateExample) -> tuple[float, list[str]]:
        reasons: list[str] = []
        quality = 1.0

        if len(candidate.prompt.strip()) < 20:
            reasons.append("prompt_too_short")
            quality -= 0.3

        if self._looks_leaky(candidate.prompt):
            reasons.append("potential_leakage")
            quality -= 0.4

        if candidate.prompt in self._seen_prompts:
            reasons.append("duplicate_prompt")
            quality -= 0.4

        self._seen_prompts.add(candidate.prompt)
        return max(0.0, quality), reasons

    def _looks_leaky(self, text: str) -> bool:
        leakage_patterns = [r"\banswer is\b", r"\bground truth\b", r"\bsolution:\b"]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in leakage_patterns)

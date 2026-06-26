from autodata_agent.quality.validators import QualityValidator
from autodata_agent.schemas import CandidateExample


def test_quality_validator_detects_short_prompt() -> None:
    validator = QualityValidator()
    score, reasons = validator.validate(CandidateExample(prompt="short"))
    assert score < 1.0
    assert "prompt_too_short" in reasons

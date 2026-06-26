from autodata_agent.agents.model_agent import TemplateSolverAgent
from autodata_agent.cli import TemplateChallenger
from autodata_agent.config import Settings
from autodata_agent.evaluators.rubric import RubricJudgeEvaluator
from autodata_agent.evaluators.verifiable import CapabilityGapEvaluator
from autodata_agent.loops.inner_loop import InnerLoopRunner
from autodata_agent.storage.repository import ArtifactRepository


def test_inner_loop_runs(tmp_path) -> None:
    settings = Settings(
        trace_store_dir=str(tmp_path / "traces"),
        dataset_store_dir=str(tmp_path / "datasets"),
        weak_rollouts=1,
        strong_rollouts=1,
        acceptance_gap=0.0,
        min_quality_score=0.0,
    )
    runner = InnerLoopRunner(
        settings=settings,
        challenger=TemplateChallenger(),
        weak_solver=TemplateSolverAgent("weak", 0.3),
        strong_solver=TemplateSolverAgent("strong", 0.9),
        evaluators=[CapabilityGapEvaluator(), RubricJudgeEvaluator()],
        repository=ArtifactRepository(settings),
    )
    result = runner.run(2)
    assert result.accepted + result.rejected == 2

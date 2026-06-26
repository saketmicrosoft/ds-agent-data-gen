import random

import typer
from rich import print

from autodata_agent.agents.base import ChallengerAgent
from autodata_agent.agents.model_agent import TemplateSolverAgent
from autodata_agent.config import Settings
from autodata_agent.evaluators.rubric import RubricJudgeEvaluator
from autodata_agent.evaluators.verifiable import CapabilityGapEvaluator
from autodata_agent.loops.inner_loop import InnerLoopRunner
from autodata_agent.loops.meta_optimizer import PromptMetaOptimizer
from autodata_agent.schemas import CandidateExample
from autodata_agent.storage.repository import ArtifactRepository

app = typer.Typer(help="Autodata synthetic data agent harness")


class TemplateChallenger(ChallengerAgent):
    def propose(self, feedback: str | None = None) -> CandidateExample:
        base = "Create a hard, verifiable question requiring multi-step reasoning."
        if feedback:
            base += f" Feedback: {feedback}"
        return CandidateExample(
            prompt=base + f" VariantSeed={random.randint(1000, 9999)}",
            expected_schema={"answer": "string"},
            metadata={"domain": "general"},
        )


@app.command("run-inner-loop")
def run_inner_loop(budget: int = typer.Option(5, min=1, max=500)) -> None:
    settings = Settings()
    repository = ArtifactRepository(settings)
    runner = InnerLoopRunner(
        settings=settings,
        challenger=TemplateChallenger(),
        weak_solver=TemplateSolverAgent(name="weak-solver", capability_hint=0.4),
        strong_solver=TemplateSolverAgent(name="strong-solver", capability_hint=0.8),
        evaluators=[CapabilityGapEvaluator(), RubricJudgeEvaluator()],
        repository=repository,
    )
    result = runner.run(budget_steps=budget)
    print({"accepted": result.accepted, "rejected": result.rejected})


@app.command("meta-opt")
def meta_opt() -> None:
    optimizer = PromptMetaOptimizer(seed_prompt="Generate challenging synthetic examples")
    result = optimizer.run()
    print({"best_variant": result.best_variant.model_dump()})


if __name__ == "__main__":
    app()

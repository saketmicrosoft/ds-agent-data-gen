from dataclasses import dataclass

from autodata_agent.schemas import PromptVariant


@dataclass
class MetaOptimizeResult:
    best_variant: PromptVariant
    history: list[PromptVariant]


class PromptMetaOptimizer:
    def __init__(self, seed_prompt: str) -> None:
        self.population: list[PromptVariant] = [
            PromptVariant(variant_id="seed", prompt_template=seed_prompt, fitness=0.5, generation=0)
        ]

    def mutate(self, parent: PromptVariant, generation: int, idx: int) -> PromptVariant:
        mutated = (
            parent.prompt_template
            + "\nConstraint: maximize novelty while preserving verifiability."
        )
        return PromptVariant(
            variant_id=f"g{generation}_v{idx}",
            prompt_template=mutated,
            parent_id=parent.variant_id,
            fitness=max(0.0, min(1.0, parent.fitness + 0.05)),
            generation=generation,
        )

    def run(self, generations: int = 3, width: int = 2) -> MetaOptimizeResult:
        history: list[PromptVariant] = [self.population[0]]
        current_best = self.population[0]

        for generation in range(1, generations + 1):
            candidates = [self.mutate(current_best, generation, idx) for idx in range(width)]
            current_best = max(candidates, key=lambda c: c.fitness)
            history.extend(candidates)

        return MetaOptimizeResult(best_variant=current_best, history=history)

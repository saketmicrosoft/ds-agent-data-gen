from autodata_agent.loops.meta_optimizer import PromptMetaOptimizer


def test_meta_optimizer_returns_history() -> None:
    optimizer = PromptMetaOptimizer(seed_prompt="seed")
    result = optimizer.run(generations=2, width=2)
    assert result.best_variant.variant_id
    assert len(result.history) == 1 + (2 * 2)

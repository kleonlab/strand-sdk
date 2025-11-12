"""Example: Variable-Length Sequence Optimization with CMA-ES.

Demonstrates optimizing sequences with variable length using the new
CMAESVarLenStrategy. This is more realistic for biological sequences.
"""

from __future__ import annotations

from strand.core.sequence import Sequence
from strand.engine import Engine, EngineConfig, default_score
from strand.engine.executors.local import LocalExecutor
from strand.engine.strategies import strategy_from_name
from strand.engine.types import Metrics
from strand.evaluators.reward_aggregator import RewardAggregator
from strand.rewards import RewardBlock


def main() -> None:
    """Run variable-length CMA-ES optimization."""

    # Create rewards
    rewards = [
        RewardBlock.stability(weight=1.0),
        RewardBlock.gc_content(target=0.5, tolerance=0.1, weight=0.5),
    ]

    # Create evaluator
    evaluator = RewardAggregator(reward_blocks=rewards)

    # Create executor (sequential for simplicity)
    executor = LocalExecutor(evaluator=evaluator)

    # Create variable-length CMA-ES strategy
    strategy = strategy_from_name(
        "cmaes-varlen",
        alphabet="ACDEFGHIKLMNPQRSTVWY",
        min_len=8,  # Shorter sequences are allowed
        max_len=25,  # Longer sequences are allowed
        seed=42,
        sigma0=0.3,
    )

    # Configure engine
    config = EngineConfig(
        iterations=8,
        population_size=32,
        seed=42,
        method="cmaes-varlen",
    )

    # Create and run engine
    engine = Engine(
        config=config,
        strategy=strategy,
        evaluator=evaluator,
        executor=executor,
        score_fn=default_score,
    )

    print("🧬 Variable-Length CMA-ES Optimization")
    print("=" * 60)
    print(f"Alphabet: {strategy.alphabet}")
    print(f"Length range: [{strategy.min_len}, {strategy.max_len}]")
    print(f"Population: {config.population_size}")
    print(f"Iterations: {config.iterations}")
    print("=" * 60)

    results = engine.run()

    print(f"\n✅ Optimization complete!")
    print(f"Total iterations: {len(results.history)}")
    print(f"Total evaluations: {results.summary.get('total_evals')}")

    if results.best:
        best_seq, best_score = results.best
        print(f"\nBest score: {best_score:.4f}")
        print(f"Best sequence: {best_seq.tokens}")
        print(f"Length: {len(best_seq.tokens)}")

    # Show convergence
    print("\n📈 Convergence (best score per iteration):")
    for i, stats in enumerate(results.history):
        print(f"  Iteration {i}: best={stats.best:.4f}, mean={stats.mean:.4f}")


if __name__ == "__main__":
    main()


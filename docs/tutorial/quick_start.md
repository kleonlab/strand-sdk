# Quick Start

Get up and running with Strand SDK in 5 minutes.

## Installation

```bash
pip install strand-sdk
```

Or install from source:

```bash
git clone https://github.com/sethmorton/strand-sdk.git
cd strand-sdk
pip install -e .
```

## Your First Optimization

Run a simple sequence optimization with built-in reward blocks:

```python
from strand.core.optimizer import Optimizer
from strand.rewards import RewardBlock

# Define reward blocks
rewards = [
    RewardBlock.stability(weight=1.0),
    RewardBlock.novelty(baseline=["MKTAYIAKQRQISFVKSHFSRQ"], weight=0.5, metric="hamming"),
]

# Create and run optimizer
optimizer = Optimizer(
    sequences=["MKTAYIAKQRQISFVKSHFSRQ"],
    reward_blocks=rewards,
    method="cem",
    iterations=25,
    population_size=50,
)

results = optimizer.run()

# Examine results
print("Top 5 sequences:")
for i, seq in enumerate(results.top(5)):
    print(f"  {i+1}. {seq}")

print(f"\nTop score: {results.scores[0]:.4f}")
```

## Next Steps

- 📖 [Core Concepts](./core_concepts.md) — Understand the architecture
- 🎓 [Tutorials](../index.md#tutorials) — Learn by example
- 🔧 [API Reference](../api_reference.md) — Explore the full API
- 💾 [Examples](../../examples/) — Real-world use cases

## Troubleshooting

### Import Errors

```python
ModuleNotFoundError: No module named 'strand'
```

**Solution**: Install in development mode from the repo root:
```bash
pip install -e .
```

### Out of Memory

For large populations, consider:
```python
optimizer = Optimizer(
    sequences=sequences,
    reward_blocks=rewards,
    method="cem",
    iterations=50,
    population_size=32,  # Reduce from default
    batch_size=4,  # Process in batches
)
```

### Slow Performance

- Use `method="random"` for quick iteration during development
- Simplify reward functions
- Reduce population size

For more help, check the [FAQ](../faq.md).


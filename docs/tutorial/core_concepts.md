# Core Concepts

## Overview

Strand SDK is built around a few core concepts that enable flexible, reproducible sequence optimization:

### 1. **Sequence**

A `Sequence` is the fundamental unit — a string of amino acids (proteins), nucleotides (DNA/RNA), or other biological polymers.

```python
from strand.core.sequence import Sequence

seq = Sequence("MKTAYIAKQRQISFVKSHFSRQ")
print(len(seq))  # 23
print(seq.to_string())  # "MKTAYIAKQRQISFVKSHFSRQ"
```

### 2. **Reward Blocks**

`RewardBlock`s are composable, reusable units that score sequences. They can be:
- **Pre-built**: Stability, solubility, novelty, length penalty
- **Custom**: Your domain-specific scoring logic

```python
from strand.rewards import RewardBlock

# Combine multiple rewards using composition
rewards = (
    RewardBlock.stability(weight=1.0) +
    RewardBlock.novelty(baseline=["MKTAYIAKQRQISFVKSHFSRQ"], weight=0.5, metric="hamming") +
    RewardBlock.length_penalty(target_length=23, weight=0.2)
)
```

### 3. **Optimizer**

An `Optimizer` runs a search algorithm (CEM, CMA-ES, genetic algorithm) to find sequences that maximize combined reward scores.

```python
from strand.core.optimizer import Optimizer

optimizer = Optimizer(
    sequences=["MKT..."],
    reward_blocks=[reward],
    method="cem",
    iterations=50,
    population_size=100,
)

results = optimizer.run()
```

### 4. **Results**

`Results` objects capture all optimization outputs:
- Top scoring sequences
- Iteration history
- Reward breakdowns
- Reproducible manifest

```python
print(results.top(5))  # Top 5 sequences by score
print(results.scores)  # All scores
print(results.manifest)  # Reproducibility metadata
```

### 5. **Manifests**

`Manifest`s capture complete experiment provenance: inputs, hyperparameters, environment, and outputs. They enable reproducibility and sharing.

```python
manifest = results.manifest
manifest.save("experiment_2025_01.json")

# Load and reproduce later
from strand.manifests import Manifest
loaded = Manifest.load("experiment_2025_01.json")
```

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│         Optimizer (Algorithm)           │
│  ┌──────────────┬──────────────┐        │
│  │  CEM  │ CMA-ES │ Genetic │  │        │
│  └──────────────┴──────────────┘        │
└──────────────┬──────────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │   RewardBlock Chain   │
    │ ┌──────────┬────────┐ │
    │ │Stability │Novelty│…│ │
    │ └──────────┴────────┘ │
    └──────────────────────┘
               │
               ▼
        ┌────────────────┐
        │  Sequences     │
        │ (Population)   │
        └────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Results + Manifest   │
    │ (Provenance Trail)    │
    └──────────────────────┘
```

## Workflow

1. **Define** sequences, rewards, and algorithm parameters
2. **Optimize** using your chosen method
3. **Analyze** results and top sequences
4. **Manifest** captures everything for reproducibility
5. **Share** or archive experiments with confidence

## Next Steps

- [Quick Start](./quick_start.md) — Run your first optimization
- [API Reference](../api_reference.md) — Detailed API docs
- [Examples](../../examples/) — Real-world use cases


# Strand SDK

> **⚠️ Status: Work In Progress (WIP)**
>
> Strand is under active development. The API is **not stable** and will change significantly before v1.0.0. Use at your own risk for production workloads.

Strand is a Python toolkit for optimizing biological sequences (proteins, DNA, RNA, antibodies) with composable reward blocks and interchangeable optimization backends. The SDK provides production-ready tools for sequence design and optimization with comprehensive provenance tracking.

## Status

- **Current Phase**: Core API development and stabilization
- **Focus**: Establish core API primitives, reward block architecture, provenance manifests, and developer tooling
- **Stability**: Experimental — breaking changes may occur in minor versions
- **Next Milestones**: 
  - v0.2.0: Production-grade optimizers (CEM, CMA-ES)
  - v0.3.0: Protein structure prediction integration
  - v1.0.0: Stable API and comprehensive documentation

## Features (Planned)

1. Modular optimization strategies (CEM, CMA-ES, Genetic Algorithm, Random search baseline)
2. Built-in reward blocks for stability, solubility, novelty, and length preference
3. Provenance manifests capturing every experiment input, configuration, and result
4. Composable CLI, docs, tests, and benchmarks for reproducible research

## Quick Start (Draft)

```bash
# from strand-sdk root
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
```

```python
from strand.core.optimizer import Optimizer
from strand.rewards import RewardBlock

optimizer = Optimizer(
    sequences=["MKT..."] ,
    reward_blocks=[
        RewardBlock.stability(weight=1.0),
        RewardBlock.novelty(baseline=["MKP..."], metric="hamming", weight=0.5),
    ],
    method="cem",
    iterations=25,
)

results = optimizer.run()
print(results.top(5))
```

## Repo Layout

See `GITHUB_REPO_STRUCTURE.md` in the design workspace for the authoritative target layout. All directories listed there are present here with placeholder implementations, docs, examples, tests, and benchmarks so contributors can iterate per vertical slice.

## Contributing

Please review `CONTRIBUTING.md` for coding standards (Google TS/py style analog), testing expectations, and the dual-license policy.

## License

MIT OR Apache-2.0 (TBD). Placeholder text lives in `LICENSE` until legal review completes.

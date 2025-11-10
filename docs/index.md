# Strand SDK Documentation

Welcome to the **Strand SDK** documentation. Strand is a production-ready Python toolkit for optimizing biological sequences with composable reward blocks and interchangeable optimization backends.

## Getting Started

- [Installation](./getting_started.md) — Set up Strand SDK in your environment
- [Quick Start](./tutorial/quick_start.md) — Run your first optimization
- [Core Concepts](./tutorial/core_concepts.md) — Understand Strand's architecture

## Tutorials

- [Basic Optimization](./tutorial/basic_optimization.md) — Simple example with built-in reward blocks
- [Custom Reward Functions](./tutorial/custom_rewards.md) — Create domain-specific reward logic
- [Multi-Objective Optimization](./tutorial/multi_objective.md) — Balance multiple objectives
- [Protein Stability & Novelty](./tutorial/protein_stability_novelty.md) — Real-world example

## API Reference

- [Core API](./api_reference.md) — `Optimizer`, `Sequence`, `Results`
- [Reward Blocks](./reward_blocks.md) — Built-in and custom rewards
- [Optimization Methods](./optimization_methods.md) — CEM, CMA-ES, Genetic Algorithm
- [Manifests](./manifests.md) — Experiment provenance and reproducibility

## Advanced Topics

- [Export & Reproducibility](./advanced/export_reproducibility.md) — Save and share experiments
- [Performance Tuning](./advanced/performance.md) — Optimize for speed and accuracy
- [Cloud Integration](./advanced/cloud_api.md) — Use Strand with cloud APIs
- [Contributing](../CONTRIBUTING.md) — Help improve Strand

## FAQ

See [Frequently Asked Questions](./faq.md) for common questions and troubleshooting.

## Examples Repository

Complete examples are available in the [`examples/`](../examples/) directory:

- `basic_optimization.py` — Minimal working example
- `custom_reward_function.py` — Domain-specific rewards
- `dna_multi_objective.py` — Multi-objective DNA optimization
- `protein_stability_novelty.py` — Protein design with stability and novelty
- `export_and_reproducibility.py` — Manifest and reproducibility
- `cloud_api_integration.py` — Integration with cloud services

## Need Help?

- 📖 Check the [FAQ](./faq.md)
- 🐛 [Report a bug](https://github.com/sethmorton/strand-sdk/issues)
- 💡 [Request a feature](https://github.com/sethmorton/strand-sdk/issues)
- 💬 [Start a discussion](https://github.com/sethmorton/strand-sdk/discussions)

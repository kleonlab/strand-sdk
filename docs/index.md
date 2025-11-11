# Strand SDK Documentation

Strand is a pre-alpha Python SDK that sits between generative biology models and wet-lab programs. The toolkit focuses on search, reward composition, and manifest logging so that model proposals can be steered toward lab-ready sequences while keeping every run reproducible.

## Purpose

- **Bridge models to experiments**: plug in raw sequence proposals, define objectives, and let Strand’s search stack explore sequence space under those constraints.
- **Capture provenance by default**: manifests record model versions, reward blocks, and optimizer settings for every run.
- **Stay modular**: adapters, optimizers, and reward blocks are meant to be swapped per vertical slice without prop drilling state across features.

## What You Can Do Today

1. Install the SDK locally and experiment with the toy optimizers in `examples/`.
2. Extend reward blocks with project-specific scoring logic.
3. Inspect the manifest structure to see how optimization runs are traced.
4. Plan adapter layers for your own generative models ahead of the design-partner release.

## Roadmap Snapshot

- **Mid December 2025** – close the loop with the first design-partner optimization runs heading into wet-lab validation.
- **Q1 2026** – tag the first open-source release of the optimization engine + manifest tooling.
- **Q2 2026** – layer in managed cloud/on-prem packages for regulated teams.

## Getting Around

- [Installation + environment setup](./getting_started.md)
- [Quick Start](./tutorial/quick_start.md) for a minimal optimization run
- [Core Concepts](./tutorial/core_concepts.md) for the main abstractions
- [API Reference](./api_reference.md) for module-level details
- [Reward Blocks](./reward_blocks.md) and [Optimization Methods](./optimization_methods.md) for scoring and search internals

## Need Help?

- Consult the [FAQ](./faq.md)
- Open an issue or discussion on GitHub if something is missing or unclear

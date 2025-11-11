# Getting Started (Pre-Alpha)

Strand is still in the design-partner phase, so the steps below are geared toward contributors and early adopters who want to study the SDK locally.

1. **Create an isolated Python 3.11+ environment.**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install the SDK and tooling.**
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```
3. **Run the smoke tests.** `pytest` is wired for the current scaffolding so you can verify the optimizer + manifest stubs still execute.
4. **Explore the examples.** Start with `examples/basic_optimization.py`, then swap in your own generative model outputs or reward blocks.
5. **Map your workflow.** Use the manifest schema (`strand/manifests/`) to plan how your lab or model metadata will be recorded once the design-partner release lands in December 2025.

When in doubt, read through `docs/tutorial/quick_start.md` for a minimal optimization loop and the FAQ for timeline updates.

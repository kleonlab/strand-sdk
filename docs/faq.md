# FAQ

### What stage is Strand in right now?
Pre-alpha. We are still building the optimization engine and tracing layer with a small set of design partners. Expect breaking API changes while we tighten up the manifest format and optimizer interfaces.

### When can I run real optimization jobs that feed a wet lab?
The first closed-loop experiments with design partners are planned for **mid December 2025**. After those runs land, we plan to cut a tagged open-source release in **Q1 2026** so anyone can reproduce the workflow on their own infrastructure.

### Which Python versions are supported?
Python 3.11+ during the design-partner phase. Broader version coverage will follow once the API settles.

### How will the open-source SDK and managed offering relate?
The core optimization engine, reward blocks, and manifest schema live in this repository and will remain open-source. Managed cloud and on-prem deployments will layer on authentication, workload orchestration, and compliance features for teams that need them.

### What makes Strand different from other sequence-design tools?
Strand treats optimization + tracing as the neutral layer between many generative models and the wet lab. You plug in whatever model generated your sequences, define constraints via reward blocks, and Strand searches sequence space while generating a provenance trail you can hand to regulators or collaborators.

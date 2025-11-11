#!/usr/bin/env python3
"""
Example pipeline demonstrating the Strand SDK for biological sequence optimization.

This example shows:
1. Creating reward blocks (stability, solubility, novelty, custom)
2. Running optimization with different methods
3. Accessing results and exporting data
4. Saving the full provenance manifest
"""

from strand import Optimizer, RewardBlock
from strand.core.sequence import Sequence
from strand.rewards.base import RewardContext


def custom_scorer(sequence: Sequence, context: RewardContext) -> float:
    """Custom scoring function: reward sequences starting with 'M' and 'K'."""
    if sequence.tokens.startswith("MK"):
        return 1.0
    return 0.5


def main() -> None:
    """Run the example optimization pipeline."""
    print("🧬 Strand SDK Example Pipeline\n")
    print("=" * 60)

    # 1. Define candidate sequences
    print("\n1️⃣  Defining candidate sequences...")
    candidates = [
        "MKTAYIAKQRQISFVKSHFSRQDILDLQY",
        "MKPAYIAKQRQISFVKSHFSRQDILDVQY",
        "MKTAYIAKQRQISFVKSHFSRQDILDLQT",
        "MKPAVVAVQRQISFVKSHFSRQDILDLQY",
        "MKTAYIAKQRQISFVKSHFSRQDILDLQW",
    ]
    print(f"   Loaded {len(candidates)} sequences")
    for i, seq in enumerate(candidates, 1):
        print(f"   {i}. {seq}")

    # 2. Define reward blocks
    print("\n2️⃣  Defining reward blocks...")
    baseline_sequences = [candidates[0], candidates[1]]

    reward_blocks = [
        RewardBlock.stability(model="esmfold", threshold=0.8, weight=1.0),
        RewardBlock.solubility(model="protbert", weight=0.5),
        RewardBlock.novelty(baseline=baseline_sequences, metric="hamming", weight=0.3),
        RewardBlock.custom(fn=custom_scorer, weight=0.2),
    ]

    print(f"   Loaded {len(reward_blocks)} reward blocks:")
    for block in reward_blocks:
        print(f"   - {block.name} (weight: {block.weight})")

    # 3. Test different optimization methods
    methods = ["random", "cem", "ga"]
    all_results = {}

    for method in methods:
        print(f"\n3️⃣  Running optimization with method: {method.upper()}")
        print("-" * 60)

        optimizer = Optimizer(
            sequences=candidates,
            reward_blocks=reward_blocks,
            method=method,
            iterations=5,
            population_size=10,
            seed=42,
            experiment=f"example_{method}",
        )

        results = optimizer.run()
        all_results[method] = results

        # Display top results
        print(f"\n   Top 3 sequences (method={method}):")
        for rank, (seq, score) in enumerate(results.top(3), 1):
            print(f"   {rank}. {seq.tokens}")
            print(f"      Score: {score:.4f}")

        # Export results
        json_path = f"results_{method}.json"
        csv_path = f"results_{method}.csv"
        results.export_json(json_path)
        results.export_csv(csv_path)
        print(f"\n   📊 Exported results:")
        print(f"      - JSON: {json_path}")
        print(f"      - CSV: {csv_path}")

        # Save manifest
        manifest = results.to_manifest()
        if manifest:
            manifest_path = f"manifest_{method}.json"
            manifest.save(manifest_path)
            print(f"      - Manifest: {manifest_path}")

    # 4. Compare results
    print("\n4️⃣  Comparing Results Across Methods")
    print("=" * 60)
    print(f"{'Method':<12} {'Top Score':<12} {'Mean Score':<12}")
    print("-" * 60)

    for method in methods:
        results = all_results[method]
        top_score = results.scores[0] if results.scores else 0
        mean_score = sum(results.scores) / len(results.scores) if results.scores else 0
        print(f"{method:<12} {top_score:>10.4f}  {mean_score:>10.4f}")

    print("\n" + "=" * 60)
    print("✅ Pipeline complete!")
    print("\nGenerated files:")
    print("  - results_*.json/.csv: Ranked sequences and scores")
    print("  - manifest_*.json: Full provenance and metadata")


if __name__ == "__main__":
    main()

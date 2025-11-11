"""Export manifest and CSV example."""

from pathlib import Path

from strand.core.optimizer import Optimizer
from strand.rewards import RewardBlock

if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    optimizer = Optimizer(
        sequences=["ACDEFG"],
        reward_blocks=[RewardBlock.stability(), RewardBlock.solubility()],
        iterations=2,
    )
    results = optimizer.run()
    results.export_csv(output_dir / "results.csv")
    manifest = results.to_manifest()
    if manifest:
        manifest.save(output_dir / "manifest.json")

"""Cloud API integration placeholder."""

import json
from collections.abc import Mapping
from pathlib import Path

from strand.core.optimizer import Optimizer
from strand.rewards import RewardBlock


def push_results(payload: Mapping[str, object]) -> None:
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "cloud_payload.json"
    output_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":
    optimizer = Optimizer(
        sequences=["ACDE"],
        reward_blocks=[RewardBlock.stability(), RewardBlock.solubility()],
        method="cem",
    )
    payload = {
        "experiment": "cloud-prototype",
        "results": [
            {"id": seq.id, "score": score}
            for seq, score in optimizer.run().top()
        ],
    }
    push_results(payload)

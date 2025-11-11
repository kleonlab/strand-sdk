"""Command-line entry point placeholder."""

from __future__ import annotations

import argparse
import json

from strand.core.optimizer import Optimizer
from strand.rewards import RewardBlock
from strand.utils import get_logger

_logger = get_logger("cli")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a Strand optimization experiment")
    parser.add_argument("sequence", help="Primary input sequence")
    parser.add_argument("--baseline", nargs="*", default=[], help="Baseline sequences for novelty")
    parser.add_argument("--method", default="cem", help="Optimization method")
    parser.add_argument("--iterations", type=int, default=10, help="Number of iterations")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    reward_blocks = [RewardBlock.stability(), RewardBlock.solubility()]
    if args.baseline:
        reward_blocks.append(RewardBlock.novelty(baseline=list(args.baseline)))

    optimizer = Optimizer(
        sequences=[args.sequence],
        reward_blocks=reward_blocks,
        method=args.method,
        iterations=args.iterations,
    )
    results = optimizer.run()
    top_results = {"top": [(seq.id, score) for seq, score in results.top(3)]}
    _logger.info("Optimization completed. Results: %s", json.dumps(top_results, indent=2))
    print(json.dumps(top_results, indent=2))  # noqa: T201  # CLI output is expected
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

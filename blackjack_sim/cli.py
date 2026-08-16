import argparse

from .analysis import summarise_simulation
from .rules import GameRules
from .simulation import run_simulation
from .strategies import (
    BasicStrategy,
    DealerLikeStrategy,
    NaiveStrategy,
)


def create_strategy(name):
    strategy_classes = {
        "naive": NaiveStrategy,
        "dealer-like": DealerLikeStrategy,
        "basic": BasicStrategy,
    }

    if name not in strategy_classes:
        raise ValueError(f"Unknown strategy: {name}")

    return strategy_classes[name]()


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Run a single-deck Blackjack Monte Carlo "
            "simulation."
        )
    )

    parser.add_argument(
        "--strategy",
        choices=("naive", "dealer-like", "basic"),
        default="basic",
        help="Player strategy to simulate.",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=10_000,
        help="Number of rounds to simulate.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=25203038,
        help="Random seed used for reproducibility.",
    )
    parser.add_argument(
        "--hit-soft-17",
        action="store_true",
        help="Make the dealer hit instead of stand on soft 17.",
    )
    parser.add_argument(
        "--blackjack-payout",
        type=float,
        default=1.5,
        help="Net payout for a natural Blackjack.",
    )

    return parser


def format_summary(summary):
    strategy_name = summary.strategy_name.replace(
        "_",
        " ",
    )

    return "\n".join(
        [
            "Blackjack Monte Carlo Simulation",
            f"Strategy: {strategy_name}",
            f"Rounds: {summary.number_of_rounds:,}",
            f"Win rate: {summary.win_rate:.2%}",
            f"Loss rate: {summary.loss_rate:.2%}",
            f"Push rate: {summary.push_rate:.2%}",
            (
                "Expected value: "
                f"{summary.expected_value:+.5f} units per hand"
            ),
            f"House edge: {summary.house_edge:.3%}",
            (
                "95% confidence interval: "
                f"[{summary.confidence_interval_low:+.5f}, "
                f"{summary.confidence_interval_high:+.5f}]"
            ),
            (
                "Standard error: "
                f"{summary.standard_error:.5f}"
            ),
            (
                "Natural Blackjack rate: "
                f"{summary.blackjack_rate:.2%}"
            ),
            f"Player bust rate: {summary.bust_rate:.2%}",
        ]
    )


def main(arguments=None):
    parser = build_parser()
    args = parser.parse_args(arguments)

    strategy = create_strategy(args.strategy)
    rules = GameRules(
        dealer_hits_soft_17=args.hit_soft_17,
        blackjack_payout=args.blackjack_payout,
    )

    result = run_simulation(
        strategy=strategy,
        number_of_rounds=args.rounds,
        seed=args.seed,
        rules=rules,
    )
    summary = summarise_simulation(result)

    print(format_summary(summary))


if __name__ == "__main__":
    main()
import argparse

from blackjack_sim.experiments import (
    compare_strategies,
    save_strategy_comparison,
)


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Compare Blackjack strategies and "
            "save the results."
        )
    )

    parser.add_argument(
        "--rounds",
        type=int,
        default=10_000,
        help="Rounds simulated for each strategy.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=25203038,
        help="Random seed used for each strategy.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory used for CSV and plot files.",
    )

    return parser


def main(arguments=None):
    args = build_parser().parse_args(arguments)

    summaries = compare_strategies(
        number_of_rounds=args.rounds,
        seed=args.seed,
    )

    csv_path, plot_path = save_strategy_comparison(
        summaries,
        args.output_dir,
    )

    print(f"Saved table: {csv_path}")
    print(f"Saved plot: {plot_path}")


if __name__ == "__main__":
    main()
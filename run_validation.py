import argparse

from blackjack_sim.validation import (
    calculate_convergence,
    save_validation_outputs,
    validate_natural_blackjack_rate,
)


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Validate the Blackjack simulation "
            "and measure convergence."
        )
    )

    parser.add_argument(
        "--natural-rounds",
        type=int,
        default=100_000,
        help="Rounds used for the natural Blackjack check.",
    )
    parser.add_argument(
        "--sample-sizes",
        nargs="+",
        type=int,
        default=[1_000, 5_000, 10_000, 50_000],
        help="Sample sizes used for convergence.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=25203038,
        help="Random seed used for validation.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory used for validation files.",
    )

    return parser


def main(arguments=None):
    args = build_parser().parse_args(arguments)

    natural_validation = (
        validate_natural_blackjack_rate(
            number_of_rounds=args.natural_rounds,
            seed=args.seed,
        )
    )

    convergence_data = calculate_convergence(
        sample_sizes=args.sample_sizes,
        seed=args.seed,
    )

    paths = save_validation_outputs(
        natural_validation,
        convergence_data,
        args.output_dir,
    )

    status = (
        "PASS"
        if natural_validation.passed
        else "REVIEW"
    )

    print(
        "Expected natural rate: "
        f"{natural_validation.expected_rate:.4%}"
    )
    print(
        "Observed natural rate: "
        f"{natural_validation.observed_rate:.4%}"
    )
    print(f"Validation result: {status}")

    for path in paths:
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
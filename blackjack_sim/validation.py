from dataclasses import asdict, dataclass
from math import sqrt
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from .analysis import summarise_simulation
from .simulation import run_simulation
from .strategies import BasicStrategy, NaiveStrategy


EXPECTED_NATURAL_BLACKJACK_RATE = 128 / 2652


@dataclass(frozen=True)
class NaturalBlackjackValidation:
    number_of_rounds: int
    expected_rate: float
    observed_rate: float
    standard_error: float
    difference: float
    tolerance: float
    passed: bool


def validate_natural_blackjack_rate(
    number_of_rounds,
    seed=25203038,
):
    if number_of_rounds <= 0:
        raise ValueError(
            "Number of rounds must be greater than zero."
        )

    result = run_simulation(
        strategy=NaiveStrategy(),
        number_of_rounds=number_of_rounds,
        seed=seed,
    )

    expected_rate = (
        EXPECTED_NATURAL_BLACKJACK_RATE
    )

    observed_rate = (
        result.player_blackjacks
        / number_of_rounds
    )

    standard_error = sqrt(
        expected_rate
        * (1 - expected_rate)
        / number_of_rounds
    )

    difference = abs(
        observed_rate - expected_rate
    )

    tolerance = 3 * standard_error

    return NaturalBlackjackValidation(
        number_of_rounds=number_of_rounds,
        expected_rate=expected_rate,
        observed_rate=observed_rate,
        standard_error=standard_error,
        difference=difference,
        tolerance=tolerance,
        passed=difference <= tolerance,
    )


def calculate_convergence(
    sample_sizes,
    seed=25203038,
):
    sample_sizes = list(sample_sizes)

    if not sample_sizes:
        raise ValueError(
            "At least one sample size is required."
        )

    if any(size <= 0 for size in sample_sizes):
        raise ValueError(
            "Sample sizes must be greater than zero."
        )

    rows = []

    for number_of_rounds in sample_sizes:
        result = run_simulation(
            strategy=BasicStrategy(),
            number_of_rounds=number_of_rounds,
            seed=seed,
        )

        summary = summarise_simulation(result)

        rows.append(
            {
                "rounds": number_of_rounds,
                "expected_value": (
                    summary.expected_value
                ),
                "standard_error": (
                    summary.standard_error
                ),
                "ci_low": (
                    summary.confidence_interval_low
                ),
                "ci_high": (
                    summary.confidence_interval_high
                ),
                "ci_width": (
                    summary.confidence_interval_high
                    - summary.confidence_interval_low
                ),
            }
        )

    dataframe = pd.DataFrame(rows)

    return dataframe.sort_values(
        "rounds"
    ).reset_index(drop=True)


def save_validation_outputs(
    natural_validation,
    convergence_data,
    output_directory,
):
    output_directory = Path(output_directory)
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    natural_csv_path = (
        output_directory
        / "natural_blackjack_validation.csv"
    )
    convergence_csv_path = (
        output_directory
        / "convergence.csv"
    )
    convergence_plot_path = (
        output_directory
        / "convergence_standard_error.png"
    )

    pd.DataFrame(
        [asdict(natural_validation)]
    ).to_csv(
        natural_csv_path,
        index=False,
    )

    convergence_data.to_csv(
        convergence_csv_path,
        index=False,
    )

    figure, axis = plt.subplots(
        figsize=(8, 5)
    )

    axis.plot(
        convergence_data["rounds"],
        convergence_data["standard_error"],
        marker="o",
        color="darkgreen",
    )

    axis.set_xscale("log")
    axis.set_title(
        "Monte Carlo Precision by Sample Size"
    )
    axis.set_xlabel("Number of simulated rounds")
    axis.set_ylabel(
        "Standard error of expected value"
    )
    axis.grid(
        True,
        which="both",
        alpha=0.3,
    )

    figure.tight_layout()
    figure.savefig(
        convergence_plot_path,
        dpi=160,
    )
    plt.close(figure)

    return (
        natural_csv_path,
        convergence_csv_path,
        convergence_plot_path,
    )
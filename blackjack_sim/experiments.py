from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from .analysis import summarise_simulation
from .rules import GameRules
from .simulation import run_simulation
from .strategies import (
    BasicStrategy,
    DealerLikeStrategy,
    NaiveStrategy,
)


def compare_strategies(
    number_of_rounds,
    seed=25203038,
    rules=None,
):
    if rules is None:
        rules = GameRules()

    strategy_classes = (
        NaiveStrategy,
        DealerLikeStrategy,
        BasicStrategy,
    )

    summaries = []

    for strategy_class in strategy_classes:
        strategy = strategy_class()

        result = run_simulation(
            strategy=strategy,
            number_of_rounds=number_of_rounds,
            seed=seed,
            rules=rules,
        )

        summaries.append(
            summarise_simulation(result)
        )

    return summaries


def summaries_to_dataframe(summaries):
    rows = []

    for summary in summaries:
        rows.append(
            {
                "strategy": summary.strategy_name,
                "rounds": summary.number_of_rounds,
                "win_rate": summary.win_rate,
                "loss_rate": summary.loss_rate,
                "push_rate": summary.push_rate,
                "expected_value": summary.expected_value,
                "house_edge": summary.house_edge,
                "standard_error": summary.standard_error,
                "ci_low": (
                    summary.confidence_interval_low
                ),
                "ci_high": (
                    summary.confidence_interval_high
                ),
                "blackjack_rate": (
                    summary.blackjack_rate
                ),
                "bust_rate": summary.bust_rate,
            }
        )

    return pd.DataFrame(rows)


def save_strategy_comparison(
    summaries,
    output_directory,
):
    output_directory = Path(output_directory)
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe = summaries_to_dataframe(summaries)

    csv_path = (
        output_directory
        / "strategy_comparison.csv"
    )
    plot_path = (
        output_directory
        / "strategy_expected_value.png"
    )

    dataframe.to_csv(csv_path, index=False)

    strategy_labels = [
        name.replace("_", " ").title()
        for name in dataframe["strategy"]
    ]

    expected_values = dataframe[
        "expected_value"
    ].to_numpy()

    lower_errors = (
        dataframe["expected_value"]
        - dataframe["ci_low"]
    ).to_numpy()

    upper_errors = (
        dataframe["ci_high"]
        - dataframe["expected_value"]
    ).to_numpy()

    figure, axis = plt.subplots(
        figsize=(8, 5)
    )

    axis.errorbar(
        strategy_labels,
        expected_values,
        yerr=[lower_errors, upper_errors],
        fmt="o",
        markersize=8,
        capsize=6,
        color="navy",
    )

    axis.axhline(
        0,
        color="black",
        linewidth=1,
        linestyle="--",
    )

    axis.set_title(
        "Expected Value by Blackjack Strategy"
    )
    axis.set_xlabel("Strategy")
    axis.set_ylabel(
        "Expected value per hand (units)"
    )
    axis.grid(
        axis="y",
        alpha=0.3,
    )

    figure.tight_layout()
    figure.savefig(
        plot_path,
        dpi=160,
    )
    plt.close(figure)

    return csv_path, plot_path
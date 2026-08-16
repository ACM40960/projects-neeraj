from pathlib import Path

import pandas as pd
import pytest

from blackjack_sim.experiments import (
    compare_strategies,
    save_strategy_comparison,
    summaries_to_dataframe,
)


@pytest.fixture(scope="module")
def comparison_summaries():
    return compare_strategies(
        number_of_rounds=30,
        seed=1234,
    )


def test_all_strategies_are_compared(
    comparison_summaries,
):
    strategy_names = [
        summary.strategy_name
        for summary in comparison_summaries
    ]

    assert strategy_names == [
        "naive",
        "dealer_like",
        "basic",
    ]

    assert all(
        summary.number_of_rounds == 30
        for summary in comparison_summaries
    )


def test_summaries_are_converted_to_table(
    comparison_summaries,
):
    dataframe = summaries_to_dataframe(
        comparison_summaries
    )

    assert len(dataframe) == 3
    assert set(dataframe.columns) == {
        "strategy",
        "rounds",
        "win_rate",
        "loss_rate",
        "push_rate",
        "expected_value",
        "house_edge",
        "standard_error",
        "ci_low",
        "ci_high",
        "blackjack_rate",
        "bust_rate",
    }


def test_csv_and_plot_are_saved(
    comparison_summaries,
    tmp_path,
):
    csv_path, plot_path = save_strategy_comparison(
        comparison_summaries,
        tmp_path,
    )

    assert csv_path.exists()
    assert plot_path.exists()
    assert csv_path.stat().st_size > 0
    assert plot_path.stat().st_size > 0

    saved_data = pd.read_csv(csv_path)

    assert len(saved_data) == 3
    assert Path(plot_path).suffix == ".png"
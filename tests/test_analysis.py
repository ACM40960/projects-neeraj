from math import sqrt
from statistics import stdev

import pytest

from blackjack_sim.analysis import summarise_simulation
from blackjack_sim.simulation import SimulationResult


def make_sample_result():
    return SimulationResult(
        strategy_name="sample",
        number_of_rounds=4,
        wins=2,
        losses=1,
        pushes=1,
        player_blackjacks=1,
        player_busts=1,
        payoffs=[1.5, 1.0, -1.0, 0.0],
    )


def test_summary_calculates_rates_and_expected_value():
    summary = summarise_simulation(
        make_sample_result()
    )

    assert summary.strategy_name == "sample"
    assert summary.number_of_rounds == 4
    assert summary.win_rate == 0.5
    assert summary.loss_rate == 0.25
    assert summary.push_rate == 0.25
    assert summary.expected_value == 0.375
    assert summary.house_edge == -0.375
    assert summary.blackjack_rate == 0.25
    assert summary.bust_rate == 0.25


def test_summary_calculates_uncertainty():
    result = make_sample_result()
    summary = summarise_simulation(result)

    expected_deviation = stdev(result.payoffs)
    expected_error = expected_deviation / sqrt(4)
    expected_margin = 1.96 * expected_error

    assert summary.standard_deviation == pytest.approx(
        expected_deviation
    )
    assert summary.standard_error == pytest.approx(
        expected_error
    )
    assert summary.confidence_interval_low == pytest.approx(
        summary.expected_value - expected_margin
    )
    assert summary.confidence_interval_high == pytest.approx(
        summary.expected_value + expected_margin
    )


def test_single_round_has_zero_standard_error():
    result = SimulationResult(
        strategy_name="single",
        number_of_rounds=1,
        wins=1,
        losses=0,
        pushes=0,
        player_blackjacks=0,
        player_busts=0,
        payoffs=[1.0],
    )

    summary = summarise_simulation(result)

    assert summary.standard_deviation == 0.0
    assert summary.standard_error == 0.0
    assert summary.confidence_interval_low == 1.0
    assert summary.confidence_interval_high == 1.0


def test_payoff_count_must_match_round_count():
    result = make_sample_result()
    result.payoffs.pop()

    with pytest.raises(
        ValueError,
        match="Payoff count",
    ):
        summarise_simulation(result)


def test_outcome_counts_must_match_round_count():
    result = make_sample_result()
    result.wins = 1

    with pytest.raises(
        ValueError,
        match="Outcome counts",
    ):
        summarise_simulation(result)
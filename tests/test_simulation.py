import pytest

from blackjack_sim.simulation import run_simulation
from blackjack_sim.strategies import (
    BasicStrategy,
    NaiveStrategy,
)


def test_simulation_counts_every_round():
    result = run_simulation(
        NaiveStrategy(),
        number_of_rounds=200,
        seed=25203038,
    )

    total_outcomes = (
        result.wins
        + result.losses
        + result.pushes
    )

    assert result.number_of_rounds == 200
    assert total_outcomes == 200
    assert len(result.payoffs) == 200
    assert 0 <= result.player_blackjacks <= 200
    assert 0 <= result.player_busts <= 200


def test_same_seed_reproduces_results():
    first_result = run_simulation(
        NaiveStrategy(),
        number_of_rounds=100,
        seed=1234,
    )
    second_result = run_simulation(
        NaiveStrategy(),
        number_of_rounds=100,
        seed=1234,
    )

    assert first_result == second_result


def test_payoffs_use_expected_units():
    result = run_simulation(
        NaiveStrategy(),
        number_of_rounds=200,
        seed=5678,
    )

    allowed_payoffs = {-1.0, 0.0, 1.0, 1.5}

    assert set(result.payoffs).issubset(allowed_payoffs)


def test_strategy_name_is_recorded():
    result = run_simulation(
        BasicStrategy(),
        number_of_rounds=50,
        seed=42,
    )

    assert result.strategy_name == "basic"


@pytest.mark.parametrize(
    "number_of_rounds",
    [0, -10],
)
def test_number_of_rounds_must_be_positive(
    number_of_rounds,
):
    with pytest.raises(ValueError):
        run_simulation(
            NaiveStrategy(),
            number_of_rounds,
        )
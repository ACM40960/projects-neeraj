from dataclasses import dataclass
from math import sqrt
from statistics import mean, stdev

from .simulation import SimulationResult


@dataclass(frozen=True)
class SimulationSummary:
    strategy_name: str
    number_of_rounds: int
    win_rate: float
    loss_rate: float
    push_rate: float
    expected_value: float
    house_edge: float
    standard_deviation: float
    standard_error: float
    confidence_interval_low: float
    confidence_interval_high: float
    blackjack_rate: float
    bust_rate: float


def summarise_simulation(
    result: SimulationResult,
) -> SimulationSummary:
    number_of_rounds = result.number_of_rounds
    number_of_outcomes = (
        result.wins
        + result.losses
        + result.pushes
    )

    if number_of_rounds <= 0:
        raise ValueError(
            "Simulation must contain at least one round."
        )

    if len(result.payoffs) != number_of_rounds:
        raise ValueError(
            "Payoff count does not match number of rounds."
        )

    if number_of_outcomes != number_of_rounds:
        raise ValueError(
            "Outcome counts do not match number of rounds."
        )

    expected_value = mean(result.payoffs)

    if number_of_rounds > 1:
        standard_deviation = stdev(result.payoffs)
    else:
        standard_deviation = 0.0

    standard_error = (
        standard_deviation
        / sqrt(number_of_rounds)
    )

    margin_of_error = 1.96 * standard_error

    return SimulationSummary(
        strategy_name=result.strategy_name,
        number_of_rounds=number_of_rounds,
        win_rate=result.wins / number_of_rounds,
        loss_rate=result.losses / number_of_rounds,
        push_rate=result.pushes / number_of_rounds,
        expected_value=expected_value,
        house_edge=-expected_value,
        standard_deviation=standard_deviation,
        standard_error=standard_error,
        confidence_interval_low=(
            expected_value - margin_of_error
        ),
        confidence_interval_high=(
            expected_value + margin_of_error
        ),
        blackjack_rate=(
            result.player_blackjacks
            / number_of_rounds
        ),
        bust_rate=(
            result.player_busts
            / number_of_rounds
        ),
    )
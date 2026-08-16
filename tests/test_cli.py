import pytest

from blackjack_sim.analysis import summarise_simulation
from blackjack_sim.cli import (
    build_parser,
    create_strategy,
    format_summary,
    main,
)
from blackjack_sim.simulation import run_simulation
from blackjack_sim.strategies import (
    BasicStrategy,
    DealerLikeStrategy,
    NaiveStrategy,
)


@pytest.mark.parametrize(
    "name,expected_type",
    [
        ("naive", NaiveStrategy),
        ("dealer-like", DealerLikeStrategy),
        ("basic", BasicStrategy),
    ],
)
def test_create_strategy(name, expected_type):
    strategy = create_strategy(name)

    assert isinstance(strategy, expected_type)


def test_unknown_strategy_raises_error():
    with pytest.raises(
        ValueError,
        match="Unknown strategy",
    ):
        create_strategy("random")


def test_default_arguments():
    args = build_parser().parse_args([])

    assert args.strategy == "basic"
    assert args.rounds == 10_000
    assert args.seed == 25203038
    assert not args.hit_soft_17
    assert args.blackjack_payout == 1.5


def test_summary_is_formatted_for_terminal():
    result = run_simulation(
        NaiveStrategy(),
        number_of_rounds=25,
        seed=123,
    )
    summary = summarise_simulation(result)

    text = format_summary(summary)

    assert "Blackjack Monte Carlo Simulation" in text
    assert "Strategy: naive" in text
    assert "Rounds: 25" in text
    assert "Expected value:" in text
    assert "95% confidence interval:" in text


def test_cli_runs_simulation(capsys):
    main(
        [
            "--strategy",
            "basic",
            "--rounds",
            "20",
            "--seed",
            "123",
        ]
    )

    output = capsys.readouterr().out

    assert "Strategy: basic" in output
    assert "Rounds: 20" in output
    assert "House edge:" in output
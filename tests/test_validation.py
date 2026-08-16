import pytest

from blackjack_sim.validation import (
    EXPECTED_NATURAL_BLACKJACK_RATE,
    calculate_convergence,
    save_validation_outputs,
    validate_natural_blackjack_rate,
)


def test_exact_natural_blackjack_probability():
    assert (
        EXPECTED_NATURAL_BLACKJACK_RATE
        == pytest.approx(128 / 2652)
    )
    assert (
        EXPECTED_NATURAL_BLACKJACK_RATE
        == pytest.approx(0.04826546)
    )


def test_natural_blackjack_validation():
    validation = validate_natural_blackjack_rate(
        number_of_rounds=2_000,
        seed=25203038,
    )

    assert validation.number_of_rounds == 2_000
    assert 0 <= validation.observed_rate <= 1
    assert validation.standard_error > 0
    assert validation.tolerance > 0
    assert validation.difference == pytest.approx(
        abs(
            validation.observed_rate
            - validation.expected_rate
        )
    )
    assert isinstance(validation.passed, bool)


@pytest.mark.parametrize(
    "number_of_rounds",
    [0, -1],
)
def test_validation_requires_positive_round_count(
    number_of_rounds,
):
    with pytest.raises(ValueError):
        validate_natural_blackjack_rate(
            number_of_rounds
        )


def test_convergence_table():
    dataframe = calculate_convergence(
        sample_sizes=[500, 2_000],
        seed=25203038,
    )

    assert list(dataframe["rounds"]) == [
        500,
        2_000,
    ]

    assert set(dataframe.columns) == {
        "rounds",
        "expected_value",
        "standard_error",
        "ci_low",
        "ci_high",
        "ci_width",
    }

    assert (
        dataframe["ci_low"]
        <= dataframe["expected_value"]
    ).all()

    assert (
        dataframe["ci_high"]
        >= dataframe["expected_value"]
    ).all()

    assert (
        dataframe.iloc[-1]["ci_width"]
        < dataframe.iloc[0]["ci_width"]
    )


@pytest.mark.parametrize(
    "sample_sizes",
    [
        [],
        [100, 0],
    ],
)
def test_convergence_requires_valid_sizes(
    sample_sizes,
):
    with pytest.raises(ValueError):
        calculate_convergence(sample_sizes)


def test_validation_outputs_are_saved(tmp_path):
    validation = validate_natural_blackjack_rate(
        number_of_rounds=200,
        seed=1234,
    )

    convergence = calculate_convergence(
        sample_sizes=[50, 100],
        seed=1234,
    )

    paths = save_validation_outputs(
        validation,
        convergence,
        tmp_path,
    )

    assert len(paths) == 3
    assert all(path.exists() for path in paths)
    assert all(path.stat().st_size > 0 for path in paths)
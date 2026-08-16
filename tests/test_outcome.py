from blackjack_sim.card import Card
from blackjack_sim.hand import Hand
from blackjack_sim.outcome import Outcome, settle_round
from blackjack_sim.rules import GameRules


def make_hand(*ranks):
    suits = ("Hearts", "Diamonds", "Clubs", "Spades")
    cards = [
        Card(rank, suits[index % len(suits)])
        for index, rank in enumerate(ranks)
    ]
    return Hand(cards)


def test_player_bust_is_loss():
    result = settle_round(
        make_hand("K", "Q", "2"),
        make_hand("10", "7"),
        GameRules(),
    )

    assert result.outcome == Outcome.LOSS
    assert result.payoff == -1.0


def test_both_blackjacks_push():
    result = settle_round(
        make_hand("A", "K"),
        make_hand("A", "Q"),
        GameRules(),
    )

    assert result.outcome == Outcome.PUSH
    assert result.payoff == 0.0


def test_player_blackjack_uses_rule_payout():
    rules = GameRules(blackjack_payout=1.2)
    result = settle_round(
        make_hand("A", "K"),
        make_hand("10", "9"),
        rules,
    )

    assert result.outcome == Outcome.WIN
    assert result.payoff == 1.2


def test_dealer_blackjack_is_loss():
    result = settle_round(
        make_hand("10", "9"),
        make_hand("A", "K"),
        GameRules(),
    )

    assert result.outcome == Outcome.LOSS
    assert result.payoff == -1.0


def test_dealer_bust_is_win():
    result = settle_round(
        make_hand("10", "7"),
        make_hand("K", "Q", "2"),
        GameRules(),
    )

    assert result.outcome == Outcome.WIN
    assert result.payoff == 1.0


def test_higher_player_total_wins():
    result = settle_round(
        make_hand("10", "9"),
        make_hand("10", "8"),
        GameRules(),
    )

    assert result.outcome == Outcome.WIN


def test_lower_player_total_loses():
    result = settle_round(
        make_hand("10", "7"),
        make_hand("10", "8"),
        GameRules(),
    )

    assert result.outcome == Outcome.LOSS


def test_equal_totals_push():
    result = settle_round(
        make_hand("10", "8"),
        make_hand("K", "8"),
        GameRules(),
    )

    assert result.outcome == Outcome.PUSH
    assert result.payoff == 0.0
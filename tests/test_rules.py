import pytest

from blackjack_sim.rules import GameRules


def test_default_rules_match_project_scope():
    rules = GameRules()

    assert not rules.dealer_hits_soft_17
    assert rules.blackjack_payout == 1.5


def test_dealer_can_be_set_to_hit_soft_17():
    rules = GameRules(dealer_hits_soft_17=True)

    assert rules.dealer_hits_soft_17


def test_blackjack_payout_can_be_changed():
    rules = GameRules(blackjack_payout=1.2)

    assert rules.blackjack_payout == 1.2


def test_blackjack_payout_must_be_positive():
    with pytest.raises(ValueError):
        GameRules(blackjack_payout=0)
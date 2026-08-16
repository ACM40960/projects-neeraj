import pytest

from blackjack_sim.card import Card
from blackjack_sim.hand import Hand
from blackjack_sim.strategies import BasicStrategy


def make_hand(*ranks):
    suits = ("Hearts", "Diamonds", "Clubs", "Spades")
    cards = [
        Card(rank, suits[index % len(suits)])
        for index, rank in enumerate(ranks)
    ]
    return Hand(cards)


def dealer_card(rank):
    return Card(rank, "Hearts")


@pytest.mark.parametrize(
    "player_ranks,dealer_rank,should_hit",
    [
        (("2", "9"), "A", True),
        (("10", "2"), "3", True),
        (("10", "2"), "4", False),
        (("10", "2"), "6", False),
        (("10", "2"), "7", True),
        (("10", "3"), "2", False),
        (("10", "6"), "6", False),
        (("10", "6"), "7", True),
        (("10", "7"), "A", False),
    ],
)
def test_hard_total_decisions(
    player_ranks,
    dealer_rank,
    should_hit,
):
    strategy = BasicStrategy()
    hand = make_hand(*player_ranks)

    decision = strategy.should_hit(
        hand,
        dealer_card(dealer_rank),
    )

    assert decision is should_hit


@pytest.mark.parametrize(
    "player_ranks,dealer_rank,should_hit",
    [
        (("A", "5"), "6", True),
        (("A", "6"), "6", True),
        (("A", "7"), "8", False),
        (("A", "7"), "9", True),
        (("A", "7"), "10", True),
        (("A", "7"), "A", True),
        (("A", "8"), "10", False),
    ],
)
def test_soft_total_decisions(
    player_ranks,
    dealer_rank,
    should_hit,
):
    strategy = BasicStrategy()
    hand = make_hand(*player_ranks)

    decision = strategy.should_hit(
        hand,
        dealer_card(dealer_rank),
    )

    assert decision is should_hit


def test_strategy_name():
    assert BasicStrategy.name == "basic"
    
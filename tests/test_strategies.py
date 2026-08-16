from blackjack_sim.card import Card
from blackjack_sim.hand import Hand
from blackjack_sim.player import play_player
from blackjack_sim.strategies import (
    DealerLikeStrategy,
    NaiveStrategy,
)


def make_hand(*ranks):
    suits = ("Hearts", "Diamonds", "Clubs", "Spades")
    cards = [
        Card(rank, suits[index % len(suits)])
        for index, rank in enumerate(ranks)
    ]
    return Hand(cards)


class FixedDeck:
    def __init__(self, *ranks):
        self.cards = [
            Card(rank, "Clubs")
            for rank in reversed(ranks)
        ]

    def draw(self):
        return self.cards.pop()


DEALER_UPCARD = Card("10", "Hearts")


def test_naive_strategy_hits_below_seventeen():
    strategy = NaiveStrategy()
    hand = make_hand("10", "6")

    assert strategy.should_hit(hand, DEALER_UPCARD)


def test_naive_strategy_stands_on_seventeen():
    strategy = NaiveStrategy()
    hand = make_hand("10", "7")

    assert not strategy.should_hit(hand, DEALER_UPCARD)


def test_dealer_like_strategy_hits_soft_seventeen():
    strategy = DealerLikeStrategy()
    hand = make_hand("A", "6")

    assert hand.is_soft
    assert strategy.should_hit(hand, DEALER_UPCARD)


def test_dealer_like_strategy_stands_on_hard_seventeen():
    strategy = DealerLikeStrategy()
    hand = make_hand("10", "7")

    assert not strategy.should_hit(hand, DEALER_UPCARD)


def test_player_draws_until_strategy_stands():
    hand = make_hand("10", "2")
    deck = FixedDeck("5", "K")

    play_player(
        hand,
        deck,
        NaiveStrategy(),
        DEALER_UPCARD,
    )

    assert hand.value == 17
    assert len(hand) == 3
    assert len(deck.cards) == 1


def test_dealer_like_player_hits_soft_seventeen():
    hand = make_hand("A", "6")
    deck = FixedDeck("2")

    play_player(
        hand,
        deck,
        DealerLikeStrategy(),
        DEALER_UPCARD,
    )

    assert hand.value == 19
    assert len(hand) == 3


def test_player_does_not_draw_on_twenty_one():
    hand = make_hand("A", "K")
    deck = FixedDeck("5")

    play_player(
        hand,
        deck,
        NaiveStrategy(),
        DEALER_UPCARD,
    )

    assert hand.value == 21
    assert len(deck.cards) == 1
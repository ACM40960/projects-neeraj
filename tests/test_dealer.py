from blackjack_sim.card import Card
from blackjack_sim.dealer import play_dealer, should_dealer_hit
from blackjack_sim.hand import Hand
from blackjack_sim.rules import GameRules


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


def test_dealer_hits_below_seventeen():
    hand = make_hand("10", "6")

    assert should_dealer_hit(hand, GameRules())


def test_dealer_stands_on_hard_seventeen():
    hand = make_hand("10", "7")

    assert not should_dealer_hit(hand, GameRules())


def test_dealer_stands_on_soft_seventeen_by_default():
    hand = make_hand("A", "6")

    assert hand.is_soft
    assert not should_dealer_hit(hand, GameRules())


def test_dealer_can_hit_soft_seventeen():
    hand = make_hand("A", "6")
    rules = GameRules(dealer_hits_soft_17=True)

    assert should_dealer_hit(hand, rules)


def test_dealer_draws_until_seventeen():
    hand = make_hand("10", "2")
    deck = FixedDeck("5", "K")

    play_dealer(hand, deck, GameRules())

    assert hand.value == 17
    assert len(hand) == 3
    assert len(deck.cards) == 1


def test_dealer_stops_after_busting():
    hand = make_hand("10", "6")
    deck = FixedDeck("K", "5")

    play_dealer(hand, deck, GameRules())

    assert hand.value == 26
    assert hand.is_bust
    assert len(deck.cards) == 1
    
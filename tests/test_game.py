from blackjack_sim.card import Card
from blackjack_sim.game import deal_initial_hands, play_round
from blackjack_sim.outcome import Outcome
from blackjack_sim.strategies import NaiveStrategy


class FixedDeck:
    def __init__(self, *ranks):
        suits = ("Hearts", "Diamonds", "Clubs", "Spades")
        ordered_cards = [
            Card(rank, suits[index % len(suits)])
            for index, rank in enumerate(ranks)
        ]
        self.cards = list(reversed(ordered_cards))

    def draw(self):
        return self.cards.pop()


def test_initial_cards_are_dealt_in_correct_order():
    deck = FixedDeck("10", "9", "7", "8")

    player_hand, dealer_hand = deal_initial_hands(deck)

    assert [card.rank for card in player_hand.cards] == ["10", "7"]
    assert [card.rank for card in dealer_hand.cards] == ["9", "8"]


def test_player_can_win_round():
    deck = FixedDeck("10", "10", "9", "8")

    played_round = play_round(
        deck,
        NaiveStrategy(),
    )

    assert played_round.player_hand.value == 19
    assert played_round.dealer_hand.value == 18
    assert played_round.result.outcome == Outcome.WIN
    assert played_round.result.payoff == 1.0


def test_player_bust_ends_round_before_dealer_plays():
    deck = FixedDeck(
        "10", "10", "6", "7", "K", "5"
    )

    played_round = play_round(
        deck,
        NaiveStrategy(),
    )

    assert played_round.player_hand.is_bust
    assert len(played_round.dealer_hand) == 2
    assert played_round.result.outcome == Outcome.LOSS
    assert len(deck.cards) == 1


def test_dealer_bust_gives_player_win():
    deck = FixedDeck(
        "10", "10", "7", "6", "K", "5"
    )

    played_round = play_round(
        deck,
        NaiveStrategy(),
    )

    assert played_round.player_hand.value == 17
    assert played_round.dealer_hand.is_bust
    assert played_round.result.outcome == Outcome.WIN
    assert len(deck.cards) == 1


def test_player_blackjack_is_paid_immediately():
    deck = FixedDeck(
        "A", "9", "K", "7", "5"
    )

    played_round = play_round(
        deck,
        NaiveStrategy(),
    )

    assert played_round.player_hand.is_blackjack
    assert len(played_round.dealer_hand) == 2
    assert played_round.result.outcome == Outcome.WIN
    assert played_round.result.payoff == 1.5
    assert len(deck.cards) == 1


def test_dealer_blackjack_loses_immediately():
    deck = FixedDeck(
        "10", "A", "9", "K", "5"
    )

    played_round = play_round(
        deck,
        NaiveStrategy(),
    )

    assert played_round.dealer_hand.is_blackjack
    assert len(played_round.player_hand) == 2
    assert played_round.result.outcome == Outcome.LOSS
    assert played_round.result.payoff == -1.0
    assert len(deck.cards) == 1
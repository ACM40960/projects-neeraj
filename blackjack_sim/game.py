from dataclasses import dataclass

from .dealer import play_dealer
from .hand import Hand
from .outcome import RoundResult, settle_round
from .player import play_player
from .rules import GameRules


@dataclass
class PlayedRound:
    player_hand: Hand
    dealer_hand: Hand
    result: RoundResult


def deal_initial_hands(deck):
    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(deck.draw())
    dealer_hand.add_card(deck.draw())
    player_hand.add_card(deck.draw())
    dealer_hand.add_card(deck.draw())

    return player_hand, dealer_hand


def play_round(deck, strategy, rules=None):
    if rules is None:
        rules = GameRules()

    player_hand, dealer_hand = deal_initial_hands(deck)

    if player_hand.is_blackjack or dealer_hand.is_blackjack:
        result = settle_round(player_hand, dealer_hand, rules)
        return PlayedRound(player_hand, dealer_hand, result)

    dealer_upcard = dealer_hand.cards[0]

    play_player(
        player_hand,
        deck,
        strategy,
        dealer_upcard,
    )

    if not player_hand.is_bust:
        play_dealer(dealer_hand, deck, rules)

    result = settle_round(player_hand, dealer_hand, rules)

    return PlayedRound(
        player_hand,
        dealer_hand,
        result,
    )
    
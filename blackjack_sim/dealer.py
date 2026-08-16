from .hand import Hand
from .rules import GameRules


def should_dealer_hit(hand: Hand, rules: GameRules):
    if hand.value < 17:
        return True

    if (
        hand.value == 17
        and hand.is_soft
        and rules.dealer_hits_soft_17
    ):
        return True

    return False


def play_dealer(hand: Hand, deck, rules: GameRules):
    while should_dealer_hit(hand, rules):
        hand.add_card(deck.draw())

    return hand
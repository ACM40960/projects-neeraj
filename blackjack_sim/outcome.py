from dataclasses import dataclass
from enum import Enum

from .hand import Hand
from .rules import GameRules


class Outcome(Enum):
    WIN = "win"
    LOSS = "loss"
    PUSH = "push"


@dataclass(frozen=True)
class RoundResult:
    outcome: Outcome
    payoff: float


def settle_round(
    player_hand: Hand,
    dealer_hand: Hand,
    rules: GameRules,
):
    if player_hand.is_bust:
        return RoundResult(Outcome.LOSS, -1.0)

    if player_hand.is_blackjack and dealer_hand.is_blackjack:
        return RoundResult(Outcome.PUSH, 0.0)

    if player_hand.is_blackjack:
        return RoundResult(Outcome.WIN, rules.blackjack_payout)

    if dealer_hand.is_blackjack:
        return RoundResult(Outcome.LOSS, -1.0)

    if dealer_hand.is_bust:
        return RoundResult(Outcome.WIN, 1.0)

    if player_hand.value > dealer_hand.value:
        return RoundResult(Outcome.WIN, 1.0)

    if player_hand.value < dealer_hand.value:
        return RoundResult(Outcome.LOSS, -1.0)

    return RoundResult(Outcome.PUSH, 0.0)
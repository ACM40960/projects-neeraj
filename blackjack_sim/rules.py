from dataclasses import dataclass


@dataclass(frozen=True)
class GameRules:
    dealer_hits_soft_17: bool = False
    blackjack_payout: float = 1.5

    def __post_init__(self):
        if self.blackjack_payout <= 0:
            raise ValueError("Blackjack payout must be greater than zero.")
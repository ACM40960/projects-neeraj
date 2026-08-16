from dataclasses import dataclass


SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")

RANKS = (
    "A", "2", "3", "4", "5", "6", "7",
    "8", "9", "10", "J", "Q", "K"
)

CARD_VALUES = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def __post_init__(self):
        if self.rank not in RANKS:
            raise ValueError(f"Unknown card rank: {self.rank}")

        if self.suit not in SUITS:
            raise ValueError(f"Unknown card suit: {self.suit}")

    @property
    def value(self):
        return CARD_VALUES[self.rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"
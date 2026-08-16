import random

from .card import Card, RANKS, SUITS


class Deck:
    def __init__(self, seed=None):
        self.random = random.Random(seed)
        self.cards = [
            Card(rank, suit)
            for suit in SUITS
            for rank in RANKS
        ]
        self.shuffle()

    def shuffle(self):
        self.random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            raise IndexError("Cannot draw from an empty deck.")

        return self.cards.pop()

    @property
    def remaining(self):
        return len(self.cards)

    def __len__(self):
        return len(self.cards)
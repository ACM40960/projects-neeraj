class Hand:
    def __init__(self, cards=None):
        self.cards = list(cards) if cards else []

    def add_card(self, card):
        self.cards.append(card)

    @property
    def value(self):
        total = sum(card.value for card in self.cards)
        has_ace = any(card.rank == "A" for card in self.cards)

        if has_ace and total + 10 <= 21:
            total += 10

        return total

    @property
    def is_soft(self):
        total = sum(card.value for card in self.cards)
        has_ace = any(card.rank == "A" for card in self.cards)

        return has_ace and total + 10 <= 21

    @property
    def is_bust(self):
        return self.value > 21

    @property
    def is_blackjack(self):
        return len(self.cards) == 2 and self.value == 21

    def __len__(self):
        return len(self.cards)
class NaiveStrategy:
    name = "naive"

    def should_hit(self, hand, dealer_upcard):
        return hand.value < 17


class DealerLikeStrategy:
    name = "dealer_like"

    def should_hit(self, hand, dealer_upcard):
        if hand.value < 17:
            return True

        return hand.value == 17 and hand.is_soft
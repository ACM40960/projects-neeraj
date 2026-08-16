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

class BasicStrategy:
    name = "basic"

    def should_hit(self, hand, dealer_upcard):
        player_total = hand.value
        dealer_value = (
            11
            if dealer_upcard.rank == "A"
            else dealer_upcard.value
        )

        if hand.is_soft:
            if player_total <= 17:
                return True

            if player_total == 18:
                return dealer_value in (9, 10, 11)

            return False

        if player_total <= 11:
            return True

        if player_total == 12:
            return dealer_value not in (4, 5, 6)

        if 13 <= player_total <= 16:
            return dealer_value not in (2, 3, 4, 5, 6)

        return False
        
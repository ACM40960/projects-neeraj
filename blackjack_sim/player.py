from .hand import Hand


def play_player(
    hand: Hand,
    deck,
    strategy,
    dealer_upcard,
):
    while (
        hand.value < 21
        and strategy.should_hit(hand, dealer_upcard)
    ):
        hand.add_card(deck.draw())

    return hand
    
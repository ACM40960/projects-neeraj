from blackjack_sim.card import Card
from blackjack_sim.hand import Hand


def make_card(rank):
    return Card(rank, "Spades")


def test_empty_hand_has_value_zero():
    hand = Hand()
    assert hand.value == 0


def test_card_can_be_added():
    hand = Hand()
    hand.add_card(make_card("5"))

    assert len(hand) == 1
    assert hand.value == 5


def test_hard_hand_value():
    hand = Hand([make_card("10"), make_card("7")])

    assert hand.value == 17
    assert not hand.is_soft


def test_ace_counts_as_eleven_when_possible():
    hand = Hand([make_card("A"), make_card("6")])

    assert hand.value == 17
    assert hand.is_soft


def test_ace_changes_to_one_to_avoid_bust():
    hand = Hand([
        make_card("A"),
        make_card("6"),
        make_card("10"),
    ])

    assert hand.value == 17
    assert not hand.is_soft
    assert not hand.is_bust


def test_multiple_aces_are_counted_correctly():
    hand = Hand([
        make_card("A"),
        make_card("A"),
        make_card("9"),
    ])

    assert hand.value == 21
    assert hand.is_soft


def test_bust_hand():
    hand = Hand([
        make_card("K"),
        make_card("Q"),
        make_card("2"),
    ])

    assert hand.value == 22
    assert hand.is_bust


def test_two_card_twenty_one_is_blackjack():
    hand = Hand([make_card("A"), make_card("K")])

    assert hand.is_blackjack


def test_three_card_twenty_one_is_not_blackjack():
    hand = Hand([
        make_card("7"),
        make_card("7"),
        make_card("7"),
    ])

    assert hand.value == 21
    assert not hand.is_blackjack
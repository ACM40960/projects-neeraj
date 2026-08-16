import pytest

from blackjack_sim.card import Card


def test_number_card_value():
    card = Card("7", "Hearts")
    assert card.value == 7


def test_face_cards_are_worth_ten():
    for rank in ("10", "J", "Q", "K"):
        assert Card(rank, "Spades").value == 10


def test_ace_starts_as_one():
    card = Card("A", "Diamonds")
    assert card.value == 1


def test_card_text():
    card = Card("K", "Clubs")
    assert str(card) == "K of Clubs"


def test_invalid_rank():
    with pytest.raises(ValueError):
        Card("15", "Hearts")


def test_invalid_suit():
    with pytest.raises(ValueError):
        Card("5", "Stars")
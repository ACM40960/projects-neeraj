from collections import Counter

import pytest

from blackjack_sim.deck import Deck


def test_new_deck_has_52_cards():
    deck = Deck()
    assert len(deck) == 52


def test_deck_has_four_cards_of_each_rank():
    deck = Deck()
    rank_counts = Counter(card.rank for card in deck.cards)

    assert all(count == 4 for count in rank_counts.values())
    assert len(rank_counts) == 13


def test_all_cards_are_unique():
    deck = Deck()
    assert len(set(deck.cards)) == 52


def test_draw_removes_one_card():
    deck = Deck()
    drawn_card = deck.draw()

    assert deck.remaining == 51
    assert drawn_card not in deck.cards


def test_same_seed_produces_same_draws():
    first_deck = Deck(seed=25203038)
    second_deck = Deck(seed=25203038)

    first_draws = [first_deck.draw() for _ in range(5)]
    second_draws = [second_deck.draw() for _ in range(5)]

    assert first_draws == second_draws


def test_drawing_from_empty_deck_raises_error():
    deck = Deck()

    for _ in range(52):
        deck.draw()

    with pytest.raises(IndexError):
        deck.draw()
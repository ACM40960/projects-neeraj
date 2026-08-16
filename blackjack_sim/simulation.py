from dataclasses import dataclass
import random

from .deck import Deck
from .game import play_round
from .outcome import Outcome
from .rules import GameRules


@dataclass
class SimulationResult:
    strategy_name: str
    number_of_rounds: int
    wins: int
    losses: int
    pushes: int
    player_blackjacks: int
    player_busts: int
    payoffs: list[float]


def run_simulation(
    strategy,
    number_of_rounds,
    seed=25203038,
    rules=None,
):
    if number_of_rounds <= 0:
        raise ValueError(
            "Number of rounds must be greater than zero."
        )

    if rules is None:
        rules = GameRules()

    random_source = random.Random(seed)

    wins = 0
    losses = 0
    pushes = 0
    player_blackjacks = 0
    player_busts = 0
    payoffs = []

    for _ in range(number_of_rounds):
        round_seed = random_source.randrange(2**32)
        deck = Deck(seed=round_seed)

        played_round = play_round(
            deck,
            strategy,
            rules,
        )

        outcome = played_round.result.outcome
        payoff = played_round.result.payoff

        if outcome is Outcome.WIN:
            wins += 1
        elif outcome is Outcome.LOSS:
            losses += 1
        else:
            pushes += 1

        if played_round.player_hand.is_blackjack:
            player_blackjacks += 1

        if played_round.player_hand.is_bust:
            player_busts += 1

        payoffs.append(payoff)

    return SimulationResult(
        strategy_name=strategy.name,
        number_of_rounds=number_of_rounds,
        wins=wins,
        losses=losses,
        pushes=pushes,
        player_blackjacks=player_blackjacks,
        player_busts=player_busts,
        payoffs=payoffs,
    )
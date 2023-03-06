# Author: Jesse Rheal
# Programming Assignment Exploding Kittens
# Purpose: Separates deck data from game logic

from prog1_card import Card
from random import shuffle

class Deck:
    def __init__(self):
        self._deck = []

    def create_deck(self, num_players):
        self._deck =      [Card.ATTACK]          * 4
        self._deck.extend([Card.FAVOR]           * 4)
        self._deck.extend([Card.NOPE]            * 5)
        self._deck.extend([Card.SHUFFLE]         * 4)
        self._deck.extend([Card.SKIP]            * 4)
        self._deck.extend([Card.SEE_THE_FUTURE]  * 5)
        self._deck.extend([Card.TENACIOUS_TABBY] * 4)
        self._deck.extend([Card.SILLY_SIAMESE]   * 4)
        self._deck.extend([Card.PUFFY_PERSIAN]   * 4)
        self._deck.extend([Card.ROWDY_RAGDOLL]   * 4)
        self._deck.extend([Card.NYAN_CAT]        * 4)
        self._deck.extend([Card.DEFUSE]          * (6 - num_players))

    def get_size(self) -> int:
        return len(self._deck)

    def add_card(self, card: Card, index = -1):
        self._deck.insert(index, card)

    def deal_card(self) -> Card:
        card = self._deck[-1]
        self._deck.pop()
        return card

    def shuffle(self):
        shuffle(self._deck)

    def get_top_cards(self, count=1):
        if len(self._deck) > count:
            return self._deck[-count:]
        return self._deck
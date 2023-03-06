from card import Card
from random import shuffle

class Deck:
    def __init__(self):
        self._deck = []

    def create_deck(self, num_players):
        self._deck = [Card.ATTACK for i in range(4)]
        self._deck.extend([Card.FAVOR for i in range(4)])
        self._deck.extend([Card.NOPE for i in range(5)])
        self._deck.extend([Card.SHUFFLE for i in range(4)])
        self._deck.extend([Card.SKIP for i in range(4)])
        self._deck.extend([Card.SEE_THE_FUTURE for i in range(5)])
        self._deck.extend([Card.TENACIOUS_TABBY for i in range(4)])
        self._deck.extend([Card.SILLY_SIAMESE for i in range(4)])
        self._deck.extend([Card.PUFFY_PERSIAN for i in range(4)])
        self._deck.extend([Card.ROWDY_RAGDOLL for i in range(4)])
        self._deck.extend([Card.NYAN_CAT for i in range(4)])
        self._deck.extend([Card.DEFUSE for i in range(6 - num_players)])
        self.shuffle()

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
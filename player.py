from card import Card

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def query_card(self) -> bool:
        if len(self.hand) == 0:
            return False
        
        print("-----Would you like to play a card?-----")
        return self._get_yes_or_no()

    def print_hand(self):
        for i, card in enumerate(self.hand):
            print(f"{i + 1}: {card.name}")

    def choose_card(self) -> Card:
        print("-----Pick a card-----")
        self.print_hand()
        
        return self.hand[self._get_num_input(1, len(self.hand)) - 1]
    
    def is_playable_card(self, card: Card) -> bool:
        if card.value < 3:
            return False
        elif card.value > 7 and len([c for c in self.hand if c == card]) < 2:
            return False
        return True

    def query_nope(self) -> bool:
        if Card.NOPE not in self.hand:
            return False

        print("-----Would you like to play a nope card? (y/n)-----")
        return self._get_yes_or_no()

    def target_player(self, targets):
        print("-----Target a player-----")
        for i, player in enumerate(targets):
            print(f"{i + 1}: {player.name}")
        
        return targets[self._get_num_input(1, len(targets)) - 1]

    def choose_card_placement(self, deck_size) -> int:
        print(f"-----Choose a spot in the deck-----")
        print(f"0: Bottom of deck")
        print(f"{deck_size}: Top of deck")

        return self._get_num_input(0, deck_size)

    def see_cards(self, cards):
        for i, card in enumerate(cards):
            print(f"{i}: {card.name}" + (" (Top of deck)" if i == len(cards)-1 else ""))

    def _get_num_input(self, min: int, max: int) -> int:
        while True:
            i = input()
            try:
                i_int = int(i)
                if i_int < min or i_int > max:
                    print("Input out of bounds")
                    continue
                return i_int
            except:
                print("Invalid input.. please enter a digit value")
    
    def _get_yes_or_no(self) -> bool:
        i = ""
        while i != "y" and i != "n":
            i = input().lower()
        
        if i == "y":
            return True
        return False
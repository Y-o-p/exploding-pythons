from player import Player
from card import Card
from deck import Deck
from random import randint

class Game:
    def __init__(self, human_players):
        self._players = [Player(f"Player {i + 1}") for i in range(0, human_players)]

        self._deck = Deck()
        self._current_player = 0
        self._extra_turns = 0
        self._previous_card = None

        self._deck.create_deck(len(self._players))
        self._deck.shuffle()
        for player in self._players:
            player.hand.append(Card.DEFUSE)
        for i in range(7):
            for player in self._players:
                player.hand.append(self._deck.deal_card())
        
        for i in range(len(self._players)):
            self._deck.add_card(Card.EXPLODING_KITTEN)
        
        self._deck.shuffle()

    def _query_nopes(self, start) -> bool:
        nope_counter = 0
        rotate = lambda s, i : (s + i) % len(self._players)
        final_player = rotate(start, -1)
        while start != final_player:
            start = rotate(start, 1)
            nope = self._players[start].query_nope()
            if nope:
                nope_counter += 1
                final_player = rotate(start, -1)

        if nope_counter % 2 == 0:
            return False
        return True

    def _draw_card(self, player: Player):
        card = self._deck.deal_card()
        if card != Card.EXPLODING_KITTEN:
            player.hand.append(card)
        else:
            # If the player has a defuse card, use it
            # Otherwise, there will be a ValueError and that player loses
            try:
                defuse = player.hand.index(Card.DEFUSE)
                print(f"{player.name} drew an exploding kitten, but it was defused!")
                self._activate_card(player, Card.DEFUSE)
                player.hand.remove(player.hand[defuse])
            except ValueError:
                print(f"{player.name} drew an exploding kitten and is out of the game!")
                self._activate_card(player, Card.EXPLODING_KITTEN)
    
    def _activate_card(self, owner: Player, card: Card):
        skip_turn = False
        attack = False

        if card == Card.EXPLODING_KITTEN:
            self._players.remove(owner)
        elif card == Card.DEFUSE:
            index = owner.choose_card_placement(self._deck.get_size())
            self._deck.add_card(Card.EXPLODING_KITTEN, index)
        elif card == Card.ATTACK:
            if self._extra_turns == 0:
                self._extra_turns += 1
            else:
                self._extra_turns += 2
            skip_turn = True
            attack = True
        elif card == Card.FAVOR:
            philanthropist = owner.target_player([player for player in self._players if player is not owner])
            donation = philanthropist.choose_card()
            owner.hand.append(donation)
            philanthropist.hand.remove(donation)
        elif card == Card.SHUFFLE:
            self._deck.shuffle()
        elif card == Card.SKIP:
            skip_turn = True
        elif card == Card.SEE_THE_FUTURE:
            owner.see_cards(self._deck.get_top_cards(3))
        elif card == Card.NOPE:
            pass
        else:
            # Cat card
            philanthropist = owner.target_player([player for player in self._players if player is not owner])
            donation = philanthropist.hand[randint(0, len(philanthropist.hand) - 1)]
            owner.hand.append(donation)
            philanthropist.hand.remove(donation)

        return (skip_turn, attack)

    def _take_player_turn(self, player: Player) -> bool:
        skip_turn = False
        attack = False
        while True:
            if not player.query_card():
                break
            card = None
            while card is None:
                chosen_card = player.choose_card()
                if player.is_playable_card(chosen_card):
                    card = chosen_card
                else:
                    print("Not a playable card.. please try again")
            print(f"{player.name} played {card.name}")
            player.hand.remove(card)
            if card.value > 7:
                player.hand.remove(card)
            noped = self._query_nopes(self._players.index(player))
            if not noped:
                (skip_turn, attack) = self._activate_card(player, card)
                if skip_turn:
                    break
        
        if not skip_turn:
            self._draw_card(player)
        return attack

    def loop(self):
        while len(self._players) > 1:
            for player in self._players:
                while True:
                    print(f"##########################")
                    print(f"It is {player.name}'s turn")
                    print(f"##########################")
                    print(f"Extra turns to take: {self._extra_turns}")
                    player.print_hand()
                    attack = self._take_player_turn(player)
                    if self._extra_turns == 0 or attack:
                        break
                    self._extra_turns -= 1
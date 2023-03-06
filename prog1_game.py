# Author: Jesse Rheal
# Programming Assignment Exploding Kittens
# Purpose: Houses the game logic for Exploding Kittens

from prog1_player import Player
from prog1_card import Card
from prog1_deck import Deck
from random import randint

class Game:
    def __init__(self, human_players):
        self._players = [Player(f"Player {i + 1}") for i in range(0, human_players)]
        self._current_player = 0
        self._extra_turns = 0
        self._previous_card = None

        self._deck = Deck()
        self._deck.create_deck(len(self._players))
        self._deck.shuffle()

        for player in self._players:
            player.hand.append(Card.DEFUSE)
        
        for i in range(7):
            for player in self._players:
                player.hand.append(self._deck.deal_card())
        
        for i in range(len(self._players) - 1):
            self._deck.add_card(Card.EXPLODING_KITTEN)
        
        self._deck.shuffle()

    def _rotate(self, s, i):
        # Returns an index to rotate around players
        return (s + i) % len(self._players)

    def _query_nopes(self, start) -> bool:
        # Go around each player asking if they want to play a nope
        # For example: if Player 2 plays a nope, Player 1 becomes the new final player
        #              because Player 2 is the new start player. Player 2 essentially
        #              starts a new query.
        nope_counter = 0
        final_player = self._rotate(start, -1)
        while start != final_player:
            start = self._rotate(start, 1)
            player = self._players[start]
            nope = player.query_nope()
            if nope:
                player.hand.remove(Card.NOPE)
                print(f"{player.name} played {Card.NOPE.name}")
                nope_counter += 1
                final_player = self._rotate(start, -1)

        return nope_counter % 2 == 1

    def _draw_card(self, player: Player):
        # Gives a card to a player and handles exploding kitten/ defuse card logic
        card = self._deck.deal_card()
        if card != Card.EXPLODING_KITTEN:
            player.add_card(card)
        else:
            # If the player has a defuse card, use it
            # Otherwise, there will be a ValueError and that player loses
            try:
                defuse = player.hand.index(Card.DEFUSE)
                print(f"{player.name} drew an exploding kitten, but it was defused!")
                self._activate_card(player, Card.DEFUSE)
                player.remove_card(player.hand[defuse])
            except ValueError:
                print(f"{player.name} drew an exploding kitten and is out of the game!")
                self._activate_card(player, Card.EXPLODING_KITTEN)
    
    def _activate_card(self, owner: Player, card: Card):
        # Implements all card logic besides nope card
        skip_turn = False
        attack = False

        if card == Card.EXPLODING_KITTEN:
            owner.dead = True
        elif card == Card.DEFUSE:
            index = owner.choose_card_placement(self._deck.get_size())
            self._deck.add_card(Card.EXPLODING_KITTEN, index)
        elif card == Card.ATTACK:
            self._extra_turns += 1 if self._extra_turns == 0 else 2
            skip_turn = True
            attack = True
        elif card == Card.SHUFFLE:
            self._deck.shuffle()
        elif card == Card.SKIP:
            skip_turn = True
        elif card == Card.SEE_THE_FUTURE:
            owner.see_cards(self._deck.get_top_cards(3))
        elif card == Card.NOPE:
            # See Game._query_nopes() and Player.query_nope()
            pass
        else:
            # Cat card or favor card
            philanthropist = owner.target_player([player for player in self._players if player is not owner])
            donation = philanthropist.choose_card() if card == Card.FAVOR else philanthropist.hand[randint(0, len(philanthropist.hand) - 1)]
            owner.add_card(donation)
            philanthropist.remove_card(donation)

        return (skip_turn, attack)

    def _take_player_turn(self, player: Player) -> bool:
        # Queries player input and acts on the input

        skip_turn = False
        attack = False
        while True:
            # If the player doesn't want to play a card then break
            if not player.query_card():
                break
            # Get a playable card
            card = None
            while card is None:
                chosen_card = player.choose_card()
                if player.is_playable_card(chosen_card):
                    card = chosen_card
                else:
                    print("Not a playable card.. please try again")
            player.hand.remove(card)
            print(f"{player.name} played {card.name}")
            # If it's a cat card then remove the other twin
            if card.value > 7:
                player.remove_card(card)
            # See if anyone wants to nope the card
            noped = self._query_nopes(self._players.index(player))
            if not noped:
                (skip_turn, attack) = self._activate_card(player, card)
                if skip_turn:
                    break
        
        if not skip_turn:
            self._draw_card(player)
        return attack

    def loop(self):
        # Main game loop
        get_alive_players = lambda : [player for player in self._players if not player.dead]
        p_index = 0
        while len(get_alive_players()) > 1:
            print(self._deck._deck)
            player = self._players[p_index]
            while not player.dead:
                print(f"##########################")
                print(f"It is {player.name}'s turn")
                print(f"##########################")
                print(f"Extra turns to take: {self._extra_turns}")
                player.print_hand()
                attack = self._take_player_turn(player)
                if self._extra_turns == 0 or attack or len(get_alive_players()) == 1:
                    break
                self._extra_turns -= 1
            p_index = self._rotate(p_index, 1)
        
        alive_players = get_alive_players()
        print(f"{alive_players[0].name} wins!!!")
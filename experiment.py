# we have four objects Deck, Pile, Player, and Card
import random


class UnoCard:
    def __init__(self, number, color):
        self.num = number
        self.color = color

    def __str__(self):
        if self.color == '': return self.num
        return self.color + " " + str(self.num)

    def is_match(self, card2):
        if isinstance(card2, UnoActionCard):
            if card2.action == 'wild' or card2.action == 'wild draw four':
                if card2.color == '#':
                    return True
            return self.color == card2.color
        return card2.color == self.color or card2.num == self.num


class UnoDeck:
    # '''represents a deck of Uno cards
    # attribute:
    #   deck: list of UnoCards'''

    def __init__(self):
        # '''UnoDeck() -> UnoDeck
        # creates a new full Uno deck'''
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard(0, color))  # one 0 of each color
            self.deck.append(UnoActionCard(4))   # creating 4 wild cards
            self.deck.append(UnoActionCard(5))   # creating 4 wild cards with +4 cards
            for i in range(2):
                # for n in range(1, 10):  # two of each of 1-9 of each color
                #     self.deck.append(UnoCard(n, color))
                for j in range(1, 4):
                    self.deck.append(UnoActionCard(j, color))
        random.shuffle(self.deck)

    def __str__(self):
        '''str(Unodeck) -> str'''
        return 'An Uno deck with ' + str(len(self.deck)) + ' cards remaining.'

    def is_empty(self):
        # '''UnoDeck.is_empty() -> boolean
        # returns True if the deck is empty, False otherwise'''
        return len(self.deck) == 0

    def deal_card(self):
        # '''UnoDeck.deal_card() -> UnoCard
        # deals a card from the deck and returns it
        # (the dealt card is removed from the deck)'''
        return self.deck.pop()

    def reset_deck(self,pile):
        # '''UnoDeck.reset_deck(pile)
        # resets the deck from the pile'''
        self.deck = pile.reset_pile()
        random.shuffle(self.deck)


class UnoPile:
    '''represents the discard pile in Uno
    attribute:
      pile: list of UnoCards'''

    def __init__(self, deck):
        '''UnoPile(deck) -> UnoPile
        creates a new pile by drawing a card from the deck'''
        while True:
            card = deck.deal_card()
            self.pile = [card]
            if isinstance(card, UnoActionCard):
                deck.deck.append(card)
                self.pile = []
                random.shuffle(deck.deck)
            else:
                break

    def __str__(self):
        '''str(UnoPile) -> str'''
        return 'The pile has ' + str(self.pile[-1]) + ' on top.'

    def top_card(self):
        '''UnoPile.top_card() -> UnoCard
        returns the top card in the pile'''
        return self.pile[-1]

    def add_card(self, card):
        '''UnoPile.add_card(card)
        adds the card to the top of the pile'''
        self.pile.append(card)

    def reset_pile(self):
        '''UnoPile.reset_pile() -> list
        removes all but the top card from the pile and
          returns the rest of the cards as a list of UnoCards'''
        new_deck = self.pile[:-1]
        self.pile = [self.pile[-1]]
        return new_deck


class UnoPlayer:
    def __init__(self, name, deck):
        '''UnoPlayer(name,deck) -> UnoPlayer
        creates a new player with a new 7-card hand'''
        self.name = name
        self.hand = [deck.deal_card() for i in range(7)]

    def __str__(self):
        '''str(UnoPlayer) -> UnoPlayer'''
        return str(self.name) + ' has ' + str(len(self.hand)) + ' cards.'

    def get_name(self):
        # '''UnoPlayer.get_name() -> str
        # returns the player's name'''
        return self.name

    def get_hand(self):
        hand = ""
        for i in range(len(self.hand)):
            hand += str(self.hand[i]) + ', '
        return hand[:-2] + '.'

    def has_won(self):
        return len(self.hand) == 0

    def draw_card(self, deck):
        '''UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn'''
        card = deck.deal_card()  # get card from the deck
        self.hand.append(card)  # add this card to the hand
        return card

    def play_card(self, card, pile):
        '''UnoPlayer.play_card(card,pile)
                plays a card from the player's hand to the pile
                CAUTION: does not check if the play is legal!'''
        self.hand.remove(card)
        pile.add_card(card)

    def take_turn(self, deck, pile):
        """UnoPlayer.take_turn(deck,pile)
        takes the player's turn in the game
        deck is an UnoDeck representing the current deck
        pile is an UnoPile representing the discard pile"""
        # print player info
        print(self.name + ", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        # get a list of cards that can be played
        top_card = pile.top_card()
        matches = [card for card in self.hand if card.is_match(top_card)]

        wild_four_count = 0
        wild_four_idxs = []
        same_color_count = 0
        for i in range(len(matches)):
            if matches[i].color == top_card.color:
                same_color_count += 1
            if isinstance(matches[i], UnoActionCard):
                if matches[i].action == 'wild draw four':
                    wild_four_count += 1
                    wild_four_idxs.append(i)

        if same_color_count > 0:
            for i in range(wild_four_count):
                matches.pop(wild_four_idxs[i] - i)

        if len(matches) > 0:  # can play
            print("These cards can be played:")
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index + 1) + ": " + str(matches[index]))
            # get player's choice of which card to play
            choice = 0
            while choice < 1 or choice > len(matches):
                choice_str = input("Which do you want to play? ")
                if choice_str.isdigit():
                    choice = int(choice_str)

            if isinstance(matches[choice - 1], UnoActionCard):
                # This means we have found an action card and we must do something to
                # the next player
                if matches[choice - 1].action == 'wild' or matches[choice - 1].action == 'wild draw four':
                    color = '#'
                    while True:
                        if color not in ['red', 'yellow', 'green', 'blue']:
                            color = input("What color would you like to change the pile to? ")
                        break
                    matches[choice - 1].color = color

                self.play_card(matches[choice - 1], pile)
                return matches[choice - 1]
            self.play_card(matches[choice - 1], pile)
            return 1
        else:  # can't play
            print("You can't play, so you have to draw.")
            input("Press enter to draw.")
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
                # draw a new card from the deck
            new_card = self.draw_card(deck)
            print("You drew: " + str(new_card))
            if new_card.is_match(top_card):  # can be played
                print("Good -- you can play that!")
                if isinstance(new_card, UnoActionCard):
                    # This means we have found an action card and we must do something to
                    # the next player
                    if new_card.action == 'wild' or new_card.action == 'wild draw four':
                        color = '#'
                        while True:
                            if color not in ['red', 'yellow', 'green', 'blue']:
                                color = input("What color would you like to change the pile to? ")
                            break

                        new_card.color = color
                    self.play_card(new_card, pile)
                    return new_card
                self.play_card(new_card, pile)
                return 1
            else:  # still can't play
                print("Sorry, you still can't play.")
                return 1


# we create a completely different class computer player that
# completes the same actions as a player except automatically
# and you can see the computer's hand
class UnoComputerPlayer:
    """
    we create a completely different class computer player that
    completes the same actions as a player except automatically
    and you can't see the computer's hand
    """
    def __init__(self, computer_number, deck):
        self.comp_num = computer_number
        self.hand = [deck.deal_card() for i in range(7)]

    def __str__(self):
        '''str(UnoPlayer) -> UnoPlayer'''
        return str(self.comp_num) + ' has ' + str(len(self.hand)) + ' cards.'

    def get_name(self):
        # '''UnoPlayer.get_name() -> str
        # returns the player's name'''
        return self.comp_num

    def has_won(self):
        return len(self.hand) == 0

    def draw_card(self, deck):
        '''UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn'''
        card = deck.deal_card()  # get card from the deck
        self.hand.append(card)  # add this card to the hand
        return card

    def play_card(self, card, pile):
        '''UnoPlayer.play_card(card,pile)
                plays a card from the player's hand to the pile
                CAUTION: does not check if the play is legal!'''
        self.hand.remove(card)
        pile.add_card(card)

    def take_turn(self, deck, pile):
        """UnoPlayer.take_turn(deck,pile)
        takes the player's turn in the game
        deck is an UnoDeck representing the current deck
        pile is an UnoPile representing the discard pile"""
        # print player info
        # get a list of cards that can be played
        print("It's " + self.comp_num + "'s turn to play a card.")
        top_card = pile.top_card()
        matches = [card for card in self.hand if card.is_match(top_card)]

        wild_four_count = 0
        wild_four_idxs = []
        same_color_count = 0
        for i in range(len(matches)):
            if matches[i].color == top_card.color:
                same_color_count += 1
            if isinstance(matches[i], UnoActionCard):
                if matches[i].action == 'wild draw four':
                    wild_four_count += 1
                    wild_four_idxs.append(i)

        if same_color_count > 0:
            for i in range(wild_four_count):
                matches.pop(wild_four_idxs[i] - i)

        if len(matches) > 0:  # can play
            # we need the computer to play a random card from its hand and then print what card the
            # computer has just played
            # we randomly select a card using randrange()
            choice = random.randrange(0, len(matches))
            if isinstance(matches[choice - 1], UnoActionCard):
                # action card but for a computer this must happen automatically
                if matches[choice - 1].action == 'wild' or matches[choice - 1].action == 'wild draw four':
                    colors = ['red', 'blue', 'yellow', 'green']
                    color = random.randrange(0, 4)
                    matches[choice - 1].color = colors[color]

                self.play_card(matches[choice - 1], pile)
                print(self.comp_num + " has played a " + str(matches[choice - 1]) + ".")
                return matches[choice - 1]
            self.play_card(matches[choice - 1], pile)
            print(self.comp_num + " has played a " + str(matches[choice - 1]) + ".")
            return 1
        else:  # can't play
            # computer must automatically draw and play the card if it can be played
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
                # draw a new card from the deck
            new_card = self.draw_card(deck)
            if new_card.is_match(top_card):  # can be played
                choice = random.randrange(0, len(matches))
                if isinstance(matches[choice - 1], UnoActionCard):
                    # action card "wild" color choosing
                    # but for a computer this must happen automatically
                    if matches[choice - 1].action == 'wild' or matches[choice - 1].action == 'wild draw four':
                        colors = ['red', 'blue', 'yellow', 'green']
                        color = random.randrange(0, 4)
                        matches[choice - 1].color = colors[color]

                    self.play_card(matches[choice - 1], pile)
                    print(self.comp_num + " has played a " + str(matches[choice - 1]) + ".")
                    return matches[choice - 1]
                self.play_card(matches[choice - 1], pile)
                print(self.comp_num + " has played a " + str(matches[choice - 1]) + ".")
                return 1
            else:  # still can't play
                print(self.comp_num + " cannot play a card.")
                return 1


class UnoActionCard:
    def __init__(self, action_type, color='#'):
        """
        :param action_type:
        action type is a value from 1 -> 5 that will say if its a:
        1: Skip
        2: Reverse
        3: Draw Two
        4: Wild Card
        5: Wild Draw Four

        :param color:
        indicates the color of the card
        """
        # we figure out which action type the card is specifically
        actions = ['skip', 'reverse', 'draw two', 'wild', 'wild draw four']
        self.action = actions[action_type - 1]
        self.color = color

    def __str__(self):
        if self.action == 'wild':
            if self.color == '#':
                return 'wild card'
            return self.color + ' wild card'
        if self.action == 'wild draw four':
            if self.color == '#':
                return self.action + ' card'
            return self.color + ' draw four'
        return self.color + ' ' + self.action

    def is_match(self, top_card):
        if self.action == 'wild' or self.action == 'wild draw four':
            return True
        if isinstance(top_card, UnoActionCard):
            return (self.color == top_card.color) or (self.action == top_card.action)
        return self.color == top_card.color


def play_uno(num_players):
    # set up full deck and initial discard pile
    print("If you would like computer players then for their name please type "
          "the string: computer")
    deck = UnoDeck()
    pile = UnoPile(deck)
    # set up the players
    player_list = []
    comp_count = 1
    for n in range(num_players):
        # get each player's name, then create an UnoPlayer
        name = input('Player #' + str(n + 1) + ', enter your name: ')
        if name.lower() == 'computer':
            # we have a computer player
            player_list.append(UnoComputerPlayer("Computer #" + str(comp_count), deck))
            comp_count += 1
        else:
            player_list.append(UnoPlayer(name, deck))
    # randomly assign who goes first
    current_player_num = random.randrange(num_players)
    # play the game
    while True:
        # print the game status
        print('-------')
        for player in player_list:
            print(player)
        print('-------')
        # take a turn
        type_of_card_played = player_list[current_player_num].take_turn(deck, pile)
        # check for a winner
        if player_list[current_player_num].has_won():
            print(player_list[current_player_num].get_name() + " wins!")
            print("Thanks for playing!")
            break
        # go to the next player
        if isinstance(type_of_card_played, UnoActionCard):
            # we have a special action card
            action = type_of_card_played.action
            if action == 'skip':
                current_player_num = (current_player_num + 2) % num_players
            elif action == 'draw two':
                for i in range(2):
                    player_list[(current_player_num + 1) % num_players].draw_card(deck)
                current_player_num = (current_player_num + 2) % num_players
            elif action == 'reverse':
                # action where we reverse
                player_list.reverse()
                current_player_num = (num_players - current_player_num + 1) % num_players
                # we completely reverse our player list and continue from there
            elif action == 'wild draw four':
                for i in range(4):
                    player_list[(current_player_num + 1) % num_players].draw_card(deck)
                current_player_num = (current_player_num + 2) % num_players
            else:
                current_player_num = (current_player_num + 1) % num_players
        else:
            current_player_num = (current_player_num + 1) % num_players


player_count = int(input("How many player are playing? "))
play_uno(player_count)

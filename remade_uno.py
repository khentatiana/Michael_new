# uno game shortened and remade using inheritance
import random


class UnoCard:
    def __init__(self, number, color):
        self.number = number
        self.color = color

    def __str__(self): return self.color + " " + str(self.number)

    def is_match(self, card2):
        if isinstance(card2, UnoActionCard):
            if card2.number in ['wild', 'wild draw four']:
                if card2.color == '': return True
        return self.color == card2.color or self.number == card2.number


class UnoActionCard(UnoCard):
    def __init__(self, color='#', number='action'): self.card = UnoCard.__init__(self, number, color)


class UnoDeck:
    def __init__(self):
        self.deck = []
        for color in ['red', 'yellow', 'green', 'blue']:
            for action in ['wild', 'wild draw four']: self.deck.append(UnoActionCard('', action))
            self.deck.append(UnoCard(0, color))
            for card in range(2):
                # for card_number in range(1, 10): self.deck.append(UnoCard(card_number, color))
                for action in ['reverse', 'skip', 'draw two']: self.deck.append(UnoActionCard(color, action))
        random.shuffle(self.deck)

    def __str__(self): return 'An Uno deck with ' + str(len(self.deck)) + ' cards remaining.'
    
    def draw_card(self): return self.deck.pop()
    
    def is_empty(self): return len(self.deck) == 0

    def reset_deck(self, pile):
        pile.reset_pile(self)
        random.shuffle(self.deck)


class UnoPile:
    def __init__(self, deck):
        while True:
            self.pile = [deck.draw_card()]
            if isinstance(self.pile[0], UnoActionCard):
                deck.deck.append(self.pile[0])
                random.shuffle(deck.deck)
            else: break

    def __str__(self): return 'The pile has ' + str(self.pile[-1]) + ' on top.'

    def top_card(self): return self.pile[-1]

    def add_card(self, card): self.pile.append(card)

    def reset_pile(self):
        deck = self.pile[:-1]
        self.pile = self.pile[-1]
        return deck


class UnoPlayer:
    def __init__(self, name, deck):
        self.name = name
        self.hand = [deck.draw_card() for i in range(7)]

    def __str__(self): return str(self.name) + ' has ' + str(len(self.hand)) + ' cards.'

    def get_name(self): return self.name

    def get_hand(self):
        new_hand = ''
        for card in self.hand: new_hand += str(card) + ', '
        return new_hand[:-2] + '.'

    def has_won(self): return len(self.hand) == 0

    def draw_card(self, deck): return str(self.hand.append(deck.draw_card())), self.hand[-1]

    def play_card(self, card, pile): self.hand.remove(card), pile.add_card(card)

    def find_matches(self, pile):
        if not isinstance(self, UnoComputerPlayer):
            print(self.name + " it's your turn.")
            print(pile)
            print("Your hand is: " + self.get_hand())
        else:
            print("It's " + self.name + "'s turn.")
            print(pile)

        top_card = pile.top_card()
        matches = [card for card in self.hand if card.is_match(top_card)]

        wild_four_count = 0
        wild_four_idxs = []
        same_color_count = 0
        for i in range(len(matches)):
            if matches[i].color == top_card.color:
                same_color_count += 1
            if isinstance(matches[i], UnoActionCard):
                if matches[i].number == 'wild draw four':
                    wild_four_count += 1
                    wild_four_idxs.append(i)

        if same_color_count > 0:
            for i in range(wild_four_count):
                matches.pop(wild_four_idxs[i] - i)

        return matches, top_card

    def choose_color(self, card):
        color = '#'
        while True:
            if color not in ['red', 'yellow', 'green', 'blue']: color = input("What color would you like to change the pile to? ")
            else: break
        card.color = color

    def take_turn(self, deck, pile):
        vals = self.find_matches(pile)
        matches = vals[0]
        if len(matches) > 0:  # can play
            print("These cards can be played:")
            for index in range(len(matches)): print(str(index + 1) + ": " + str(matches[index]))

            choice = 0
            while choice < 1 or choice > len(matches):
                choice_str = input("Which do you want to play? ")
                if choice_str.isdigit(): choice = int(choice_str)

            if isinstance(matches[choice - 1], UnoActionCard):
                if matches[choice - 1].number == 'wild' or matches[choice - 1].number == 'wild draw four': self.choose_color(matches[choice - 1])
                self.play_card(matches[choice - 1], pile)
                return matches[choice - 1]
            self.play_card(matches[choice - 1], pile)
            return 1
        else:
            print("You can't play, so you have to draw.")
            _ = input("Press enter to draw.")
            if deck.is_empty(): deck.reset_deck(pile)
            new_card = self.draw_card(deck)[1]
            print("You drew: " + str(new_card))
            if new_card.is_match(vals[1]):
                print("Good -- you can play that!")
                if isinstance(new_card, UnoActionCard):
                    if new_card.number == 'wild' or new_card.number == 'wild draw four': self.choose_color(new_card)

                    self.play_card(new_card, pile)
                    return new_card
                self.play_card(new_card, pile)
                return 1
            else:
                print("Sorry, you still can't play.")
                return 1


class UnoComputerPlayer(UnoPlayer):
    def take_turn(self, deck, pile):
        vals = self.find_matches(pile)
        matches = vals[0]
        if len(matches) > 0:
            choice = random.randrange(0, len(matches))
            if isinstance(matches[choice], UnoActionCard):
                if matches[choice - 1].action == 'wild' or matches[choice].action == 'wild draw four': matches[choice].color = ['red', 'blue', 'yellow', 'green'][random.randrange(0, 4)]
                self.play_card(matches[choice - 1], pile)
                print(self.name + " has played a " + str(matches[choice]) + ".")
                return matches[choice]
            self.play_card(matches[choice], pile)
            print(self.name + " has played a " + str(matches[choice]) + ".")
            return 1
        else:
            if deck.is_empty(): deck.reset_deck(pile)
            new_card = self.draw_card(deck)[1]
            if new_card.is_match(vals[1]):  # can be played
                choice = random.randrange(0, len(matches))
                if isinstance(matches[choice], UnoActionCard):
                    if matches[choice].action == 'wild' or matches[choice].action == 'wild draw four': matches[choice].color = ['red', 'blue', 'yellow', 'green'][random.randrange(0, 4)]
                    self.play_card(matches[choice], pile)
                    print(self.name + " has played a " + str(matches[choice]) + ".")
                    return matches[choice]
                self.play_card(matches[choice], pile)
                print(self.name + " has played a " + str(matches[choice]) + ".")
                return 1
            else:  # still can't play
                print(self.name + " cannot play a card.")
                return 1


def play_uno(num_players):
    print("If you would like computer players then for their name please type the string: 'computer'")
    deck = UnoDeck()
    pile = UnoPile(deck)
    player_list = []
    comp_count = 1

    for n in range(num_players):
        name = input('Player #' + str(n + 1) + ', enter your name: ')
        if name.lower() == 'computer':
            player_list.append(UnoComputerPlayer("Computer #" + str(comp_count), deck))
            comp_count += 1
        else: player_list.append(UnoPlayer(name, deck))

    current_player_num = random.randrange(0, num_players)
    while True:
        print('-------')
        for player in player_list: print(player)
        print('-------')
        type_of_card_played = player_list[current_player_num].take_turn(deck, pile)

        if player_list[current_player_num].has_won():
            print(player_list[current_player_num].get_name() + " wins!")
            print("Thanks for playing!")
            break

        if isinstance(type_of_card_played, UnoActionCard):
            action = type_of_card_played.number
            if action == 'skip': current_player_num = (current_player_num + 2) % num_players
            elif action == 'draw two':
                for i in range(2):
                    player_list[(current_player_num + 1) % num_players].draw_card(deck)
                    player_list[(current_player_num + 1) % num_players].hand[-1] = player_list[(current_player_num + 1) % num_players][-1][1]
                current_player_num = (current_player_num + 2) % num_players
            elif action == 'reverse':
                # action where we reverse
                player_list.reverse()
                current_player_num = (num_players - current_player_num + 1) % num_players
                # we completely reverse our player list and continue from there
            elif action == 'wild draw four':
                for i in range(4):
                    player_list[(current_player_num + 1) % num_players].draw_card(deck)
                    player_list[(current_player_num + 1) % num_players].hand[-1] = player_list[(current_player_num + 1) % num_players][-1][1]
                current_player_num = (current_player_num + 2) % num_players
            else:
                current_player_num = (current_player_num + 1) % num_players
        else:
            current_player_num = (current_player_num + 1) % num_players


player_count = int(input("How many player are playing? "))
play_uno(player_count)

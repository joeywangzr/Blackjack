import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True
status = ''

# Classes ---------------------------------------------------------------------------------------

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total -= self.bet

def bet_chips(chips):
    while True:
        try:
            print('You have ' + str(chips.total) + ' chips you can bet.')
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError: 
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed", chips.total)
            else:
                break
    
def hit(deck,hand):
    hand.add_card(deck.deal())

def hit_or_stand(deck,hand):
    global playing
    
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        
        if x[0].lower() == 'h':
            print("Player hits.")
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break

def show_some(dealer,player):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(dealer,player):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

print('BLACKJACK by @joeywangzr. Get as close as you can until 21. Aces count as 1 or 11.')

while True:

    deck = Deck()
    deck.shuffle()

    player_chips = Chips()
    bet_chips(player_chips)

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    while playing:
        show_some(dealer_hand, player_hand)
        if player_hand.value > 21:
            if player_hand.aces > 0:
                player_hand.adjust_for_ace()
            else:
                status = 'player_bust'
                break
        else:
            hit_or_stand(deck, player_hand)

    while playing == False:
        if dealer_hand.value < 17:
            dealer_hand.add_card(deck.deal())
        elif dealer_hand.value > 21:
            if dealer_hand.aces > 0:
                dealer_hand.adjust_for_ace()
            else: 
                status = 'dealer_bust'
                break
        else:
            break

    show_all(dealer_hand,player_hand)

    # Test different winning scenarios
    if status == 'dealer_bust':
        print('Dealer Bust!')
        player_chips.win_bet()

    elif status == 'player_bust':
        print('Player Bust!')
        player_chips.lose_bet()

    elif dealer_hand.value > player_hand.value:
        print('Dealer wins.')
        player_chips.lose_bet()

    elif dealer_hand.value < player_hand.value:
        print('Player wins.')
        player_chips.win_bet()

    else:
        print('It\'s a tie!')

    print('You now have ' + str(player_chips.total) + ' chips.')

    while True:
        try:
            again = str(input('Play again? y/n: '))
        except ValueError: 
            print('Please input y or n!')
        else:
            if again.lower() == 'y':
                playing = True
                status = ''
                break
            elif again.lower() == 'n':
                print('Thanks for playing.')
                break
    if again == 'n':
        break

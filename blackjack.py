import simplegui
import random

# sprite - 949x392
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# some global variables
in_play = False
outcome = ""
choice = ""
score = 0

# globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []
        self.value = 0

    def __str__(self):
        # return a string representation of a hand
        s = []
        for i in range(len(self.hand)):
            s.append(str(self.hand[i]))
        return "Hand contains " + str(s)

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)
        return str(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        A = False
        self.value = 0
        for i in range(len(self.hand)):
            self.value += VALUES[self.hand[i].rank]
            if self.hand[i].rank == "A":
                A = True
        if A:
            if self.value + 10 <= 21:
                self.value += 10
        return self.value

    def draw(self, canvas, pos, dealer = False):
        # draw a hand on the canvas using the cards draw method
        if dealer == False or in_play == False:
            for i in range(len(self.hand)):
                self.hand[i].draw(canvas, [pos[0]+((CARD_SIZE[0]+5)*i), pos[1]])
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0]+36.5, pos[1]+49], CARD_BACK_SIZE)
            for i in range(1,len(self.hand)):
                self.hand[i].draw(canvas, [pos[0]+((CARD_SIZE[0]+5)*i), pos[1]])
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for x in SUITS:
            for y in RANKS:
                self.deck.append(Card(x,y))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
        
    
    def __str__(self):
        # return a string representing the deck 
        s = ""
        for i in range(len(self.deck)):
            s += str(self.deck[i]) + ' '
        return s

# event handlers for buttons
def deal():
    global outcome, choice, in_play, player, dealer, deck, score
    if in_play == False:
        choice = "Hit or Stand?"
        outcome = ""
        deck = Deck()
        player = Hand()
        dealer = Hand()
        random.shuffle(deck.deck)
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        in_play = True
        if player.get_value() == 21:
            outcome = "Blackjack! You win!"
            choice = "New deal?"
            score += 1
            in_play = False

def hit():
    # if busted, assign the message to outcome, update in_play and score
    global outcome, choice, in_play, score
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value() > 21:        
            outcome = "You went bust and lose."
            choice = "New deal?"
            score -= 1
            in_play = False           

def stand():
    # if hand is in play, dealer hits until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global outcome, choice, in_play, score
    if in_play :
        while (dealer.get_value() < 17):
            dealer.add_card(deck.deal_card())
        if (dealer.value > 21):
            outcome = "Dealer Busted. You win!"
            score += 1
        elif (player.value > dealer.get_value()):
            outcome = "You win!"
            score += 1
        else:
            outcome = "You lose!"
            score -= 1
        choice = "New deal?"
    in_play = False

# draw handler    
def draw(canvas):
    player.draw(canvas,[30,400])
    dealer.draw(canvas,[30,200], True)
    canvas.draw_text("Score: " + str(score), (400, 100), 30, 'Black')
    canvas.draw_text('Blackjack', (103, 103), 42, 'Black')
    canvas.draw_text('Blackjack', (100, 100), 42, 'Red')
    canvas.draw_text('Dealer', (100, 180), 30, 'Black')
    canvas.draw_text('Player', (100, 380), 30, 'Black')
    canvas.draw_text(outcome, (250, 180), 30, 'Black')
    canvas.draw_text(choice, (250, 380), 30, 'Black')

# frame initialization
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
label = frame.add_label('Values:')
label2 = frame.add_label('A = 1 or 11')
label3 = frame.add_label('2 to 10 = 2 to 10')
label4 = frame.add_label('images = 10')

# this get things rolling
deal()
frame.start()

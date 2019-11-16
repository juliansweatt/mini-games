import random
from functools import reduce
class poker:
    class card:
        def __init__(self, cardName=None, suit=None, randomCard=False, deck={}):
            if (randomCard):
                self.name, self.suit = randomCard(deck)
            else:
                self.name = cardName
                self.suit = suit
            self.image = 'cards\\' + cardName + "_of_" + suit + ".png"
        
    
        def randomCard(deck={}):
            number = random.randint(2,14)
            if (number == 11):
                number = "jack"
            elif(number == 12):
                number = "queen"
            elif (number == 13):
                number = "king"
            elif (number == 14):
                number = "ace"
            else:
                number = str(number)
            suit = random.randint(0, 3)
            if (suit == 0):
                suit = "clubs"
            elif (suit == 1):
                suit = "spades"
            elif(suit == 2):
                suit = "hearts"
            elif (suit == 3):
                suit = "diamonds"
            if (number in deck):
                if (deck[number] == suit):
                    randomCard(deck)
            return number, suit
        
        def getNumber(self):
            if (self.name == "jack"):
                return = 11
            elif(self.name == "queen"):
                return = 12
            elif (self.name == "king"):
                return = 13
            elif (self.name == "ace"):
                return = 14
            else:
                return = int(self.name)

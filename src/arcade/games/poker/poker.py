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

    class player:
        def __init__(self, playerName, hand=None, money=0, dealer=False):
            self.name = playerName
            if(hand):
                self.hand = hand
            else:
                self.hand = [self.card(randomCard=True), self.card(randomCard=True)]

            if(money):
                self.money = money
            self.handValue = 0
            self.highCardValue = 
            self.dealer = dealer
        def addCard(self, card=None, deck={}, randomCard=False,)
            if (randomCard):
                card = self.card(random=True, deck=deck)
            self.hand.append = card
            return card
        def hasStraightOrFlush(self):
            if(len(self.hand) < 5):
                return False
            flush = False
            straightFlush = False
            currentStraight = []
            numbers = [card.getNumber for card in self.hand]
            numbers.sort(reverse=True)
            while (len(numbers) >= 5 and len(currentStraight) < 5):
                for i in range(len(numbers)):
                    if (numbers[i] - numbers[i+1] != 1):
                        currentStraight = []
                        for delIndex in range(i, -1, -1):
                            del numbers[delIndex]
                        break
                    else:
                        if (i == 0):
                            currentStraight.append(numbers[i])
                        currentStraight.append(numbers[i+1])
                        if (len(currentStraight) >= 5):
                            self.highCardValue = currentStraight[0]
                            break
            suits = [card.suit for card in self.hand]
            if(suits.count("clubs") >= 5):
                flush = "clubs"
            elif(suits.count("spades") >= 5):
                flush = "spades"
            elif (suits.count("hearts") >= 5):
                flush = "hearts"
            elif (suits.count("diamonds") >= 5):
                flush = "diamonds"
            if(flush):
                self.highCardValue = 0
                for card in self.hand:
                    if (card.suit == flush and card.getNumber() > self.highCardValue):
                        self.highCardValue = card.getNumber()
                for num in currentStraight:
                    for card in self.hand:
                        if (card.getNumber() == num):
                            straightFlush = True
                            break
                        else:
                            straightFlush = False
                    if (not straightFlush):
                        break
            if (straightFlush and self.highCardValue == 14):
                return 10
            elif(straightFlush):
                return 9
            elif(flush):
                return 6
            elif(len(currentStraight) > 0):
                return 5
            else:
                return 0
            
            def getPairValue(self):
                pair = 0
                numbers = [card.getNumber for card in self.hand]
                uniqueNumbers = []
                for num in numbers:
                    if (num not in uniqueNumbers):
                        uniqueNumbers.append(num)
                uniqueNumbers.sort(reverse=True)
                for num in uniqueNumbers:
                    if (numbers.count(num) > 0 and pair == 0):
                        pair = numbers.count(num)
                        self.highCardValue = num
                    elif(numbers.count(num) == 2 and pair == 1):
                        pair = 2
                        self.highCardValue = num if num > self.highCardValue else self.highCardValue
                    elif (numbers.count(num) == 2 and pair == 3):
                        pair = 5
                    elif (numbers.count(num) == 3 and (pair == 1 or pair == 2)):
                        pair = 5
                        #ADD Full House Edge Cases (Adding decimal values?)
                        self.highCardValue = num
                if (pair == 1):
                    return 2
                elif (pair == 2):
                    return 3
                elif (pair == 3):
                    return 4
                elif (pair == 4):
                    return 8
                elif (pair == 5):
                    return 7
                else:
                    return 0
            
        def getHandValue(self):
            pairs = self.getPairs()
            self.handValue = self.hasStraightOrFlush()
            if(self.hasRoyalFlush()):
                self.handValue = 11
            if(self.hasStraightFlush()):
                self.handValue = 10
            if(paris == 4):
                self.handValue = 9
            if(self.hasFullHouse()):
                self.handValue = 8
            if(self.hasFlush()):
                self.handValue

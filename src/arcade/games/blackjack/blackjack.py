import pygame
import os
from arcade import plethoraAPI
from enum import IntFlag, auto, unique

from pygame.locals import (
    QUIT,
    K_SPACE,
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_q,
    KEYDOWN, KEYUP,
    MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN,
)

from typing import Tuple

@unique
class ArrowMask(IntFlag):
    """ Enum used to mask arrow keys (up, right, down, left) """
    up = auto()
    right = auto()
    down = auto()
    left = auto()

import random
class Game(plethoraAPI.Game):
    def __init__(self, humanPlayer=None, dealer=None, numGames=10):
        super().__init__(size=(800, 600), fps=12)  # call plethoraAPI.Game.__init__ to initialize :attr:`size` and :attr:`fps`
        self.arrows = 0b0000  # bitmask for arrow keys
        self.arrows_hidden = 0b0000  # bitmask for hiding opposite keys on key down while that key is down
        self.player = humanPlayer or self.playerOrDealer("Player", None, 500)
        self.playerBust = False
        self.dealer = dealer or self.playerOrDealer("Player", None, 0)
        self.dealerBust = False
        self.split = False
        self.canSplit = False
        self.minWager = 50
        self.totalWager = self.minWager
        self.deck={}
    
    def checkAceHand(self, hand):
        lowHand = [1 if card == 11 else card for card in hand]
        for i in lowHand:
            print()
        lastCount = sum(lowHand)
        if (lastCount < 21):
            for i in range(lowHand.count(1)):
                if(lastCount + (i*10) < 21):
                    lastCount += (i*10)
        else:
            lastCount = 0
        return lastCount



    def checkCardTotal(self, hand):
        aces = False
        checkHand = [card if type(card) == type(1) else card.getCardBlackjackValue() for card in hand]
        aces = 11 in checkHand
        if (len(checkHand) == 2):
            if (sum(checkHand) == 21):
                return "blackjack"
            if(checkHand[0] == checkHand[1]):
                self.canSplit = True
            return sum(checkHand)
        elif (sum(checkHand) > 21):
            if (aces):
                return self.checkAceHand(checkHand)
            else:
                return 0
        else:
            return sum(checkHand)
    def onevent(self, event: pygame.event):
        """ called from :func:`PlethoraAPI.mainloop` when there is an event while this game is running
        Args:
            event: a pygame.event fetched from :func:`pygame.event.get` in
                :func:`arcade.plethoraAPI.PlethoraAPI.mainloop`
        Returns:
            bool: True if onrender should be called on the next frame; False otherwise
        """
        if event.type == KEYDOWN:
            # if arrow keydown:
            #   1) add to key mask to `self.arrows`
            #   2) add opposite key mask to `self.arrows_hidden`
            #   3) remove key mask from `self.arrows_hidden`
            if event.key == pygame.K_UP:
                self.arrows |= ArrowMask.up
                self.arrows_hidden |= ArrowMask.down
                self.arrows_hidden &= ~ArrowMask.up
            elif event.key == pygame.K_RIGHT:
                self.arrows |= ArrowMask.right
                self.arrows_hidden |= ArrowMask.left
                self.arrows_hidden &= ~ArrowMask.right
            elif event.key == pygame.K_DOWN:
                self.arrows |= ArrowMask.down
                self.arrows_hidden |= ArrowMask.up
                self.arrows_hidden &= ~ArrowMask.down
            elif event.key == pygame.K_LEFT:
                self.arrows |= ArrowMask.left
                self.arrows_hidden |= ArrowMask.right
                self.arrows_hidden &= ~ArrowMask.left
            else:
                return False
            return True
        if event.type == KEYUP:
            # if arrow keyup:
            #   1) remove key mask from `self.arrows`
            #   2) remove both key and opposite key from `self.arrows_hidden`
            if event.key == pygame.K_UP:
                self.arrows &= ~ArrowMask.up
                self.arrows_hidden &= ~(ArrowMask.up | ArrowMask.down)
            elif event.key == pygame.K_RIGHT:
                self.arrows &= ~ArrowMask.right
                self.arrows_hidden &= ~(ArrowMask.left | ArrowMask.right)
            elif event.key == pygame.K_DOWN:
                self.arrows &= ~ArrowMask.down
                self.arrows_hidden &= ~(ArrowMask.up | ArrowMask.down)
            elif event.key == pygame.K_LEFT:
                self.arrows &= ~ArrowMask.left
                self.arrows_hidden &= ~(ArrowMask.left | ArrowMask.right)
            else:
                return False
            return True
        return False
    
    def onrender(self) -> bool:
        """ called from :func:`PlethoraAPI.mainloop` when game is dirty
        The game is dirty when:
            - The game is first loaded
            - True is returned from :func:`Game.onevent`
            - True is returned from :func:`Game.onrender`
        Returns:
            bool: True if onrender should be called again on the next frame - this is useful if a
                  key is down and re-rendering should occur; False otherwise
        """
        self.display.fill((50,205,50))
        pygame.draw.rect(self.display, (12, 10, 20),(self.rect.width-200,0,200,self.rect.height))


        arrows = self.arrows & ~self.arrows_hidden
        print(self.selected)
        return rerender

    class playerOrDealer:
        def __init__(self, playerName, hand=None, money=0, dealer=False):
            self.name = playerName
            if(hand and type(hand) == list):
                self.hand = hand
            else:
                self.hand = [self.card(randomCard=True), self.card(randomCard=True)]
            if(money):
                self.money = money
            self.blackjack = False
            self.dealer = dealer
        def addCard(self, card=None, deck={}, randomCard=False):
            if (randomCard):
                card = self.card(randomCard=True, deck=deck)
            self.hand.append(card)
            return card
        class card:
            def __init__(self, cardName=None, suit=None, randomCard=False, deck={}):
                if (randomCard):
                    self.name, self.suit = self.randomCard(deck)
                else:
                    self.name = cardName
                    self.suit = suit
                print(os.getcwd())
                self.image = pygame.image.load('cards\\' + self.name + "_of_" + self.suit + ".png")
                self.image = pygame.transform.scale(self.image, (160, 233))
        
    
            def randomCard(self, deck={}):
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
            

            def getCardBlackjackValue(self):
                if (self.name == "jack"):
                    number = 10
                elif(self.name == "queen"):
                    number = 10
                elif (self.name == "king"):
                    number = 10
                elif (self.name == "ace"):
                    number = 11
                else:
                    number = int(self.name)
                return number
        
    
    
        

        


            
        
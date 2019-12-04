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


IMAGES = plethoraAPI.ROOT/"games/images"


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
        self.numGames = numGames
        self.split = False
        self.canSplit = False
        self.canDoubleDown = True
        self.playerStayed = False
        self.doubleDown = False
        self.minWager = 50
        self.totalWager = self.minWager
        self.cardBack = pygame.image.load(str(IMAGES/'cards/back.png'))
        self.cardBack = pygame.transform.scale(self.cardBack, (160, 233))
        self.smallFont = pygame.font.SysFont('Arial', 25)
        self.biggerFont = pygame.font.SysFont('Arial', 30)
        self.select = [True, False, False, False]
        self.selected = 0
        self.deck={}
        self.topCardStart = (10, 10)
        self.bottomCardStart = (430, self.rect.height-243)
        self.gameEnd = False
        self.mouse_down_pos = None
        self.plusButton = pygame.Rect(self.rect.width-34,200,26,22)
        self.minusButton = pygame.Rect(self.rect.width-34,224,26,21)
        self.stayButton = pygame.Rect(self.rect.width-180,280,160,40)
        self.hitButton = pygame.Rect(self.rect.width-180,340,160,40)
        self.doubleDownButton = pygame.Rect(self.rect.width-180,400,160,40)
        self.splitButton = pygame.Rect(self.rect.width-180,460,160,40)
        self.exitWarningScreenBox = pygame.Rect(self.rect.width/2-250,200,300,200)
        self.exitWarningScreenBoxText = (self.rect.width/2-170,225)
        self.confirmExitButton = pygame.Rect(self.rect.width/2-200,325,80,40)
        self.rejectExitButton = pygame.Rect(self.rect.width/2-75,325,80,40)

        self.clicked = False
        self.exitWarningScreen = False
    
    def checkAceHand(self, hand):
        lowHand = [1 if card == 11 else card for card in hand]
        # for i in lowHand:
        #     print()
        lastCount = sum(lowHand)
        if (lastCount < 21):
            for i in range(lowHand.count(1)):
                if(lastCount + (i*10) < 21):
                    lastCount += (i*10)
        else:
            lastCount = 0
        return lastCount


    def getMenuBottonLocation(self):
        if (self.canSplit):
            return (self.rect.width-180,520,160,40)
        else:
            return (self.rect.width-180,460,160,40)
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
    
    def continueGame(self):
        continueGame = False
        print("PLayer Total:", self.checkCardTotal(self.player.hand))
        if (self.checkCardTotal(self.player.hand) != 0):
            self.playerBust = False
            if (self.checkCardTotal(self.player.hand) == 'blackjack' or self.checkCardTotal(self.player.hand) == 21):
                print('Player win')
                continueGame = False

            else:
                continueGame = True
        else:
            self.playerBust = True

        if (self.checkCardTotal(self.dealer.hand) != 0):
            self.dealerBust = False
            if (self.checkCardTotal(self.dealer.hand) == 'blackjack' or self.checkCardTotal(self.dealer.hand) == 21):
                print('Dealer win')
                continueGame = False
            else:
                continueGame = True
        else:
            self.dealerBust = True
        if (self.playerBust or self.dealerBust):
            print('Player Lost')
            return False
        else:
            return True
    
    def playerDoubleDown(self):
        self.totalWager *= 2
        self.canDoubleDown = False

    def playerSplit(self):
        self.totalWager *= 2
        self.player.splitHand = [self.player.hand[0], self.card(random=True, deck=self.deck)]
        self.player.hand = [self.player.hand[0], self.card(random=True, deck=self.deck)]
        self.player.canSplit = False
    
    def hit(self, hitPlayer=True):
        if (self.checkCardTotal(self.dealer.hand) == "blackjack"):
            return False
        if (self.checkCardTotal(self.dealer.hand) < 17 and self.checkCardTotal(self.dealer.hand) > 0):
            self.dealer.addCard(deck=self.deck, randomCard=True)
            self.dealerBust = not self.continueGame()
            if (self.dealerBust):
                return False
        else:
            if(self.playerStayed):
                return False
            
        if (hitPlayer):
            self.player.addCard(deck=self.deck, randomCard=True)
            if (self.split):
                self.player.splitHand.addCard(deck=self.deck, randomCard=True)
            self.playerBust = not self.continueGame()
            if (self.playerBust):
                return False
        return True

    def onGameEnd(self):
        if (self.checkCardTotal(self.player.hand) == 'blackjack'):
            self.player.money += self.totalWager*3
        elif (self.checkCardTotal(self.dealer.hand) == 'blackjack'):
            self.player.money -= self.totalWager
        elif (self.playerBust):
            self.player.money -= self.totalWager
        elif(self.dealerBust):
            self.player.money += self.totalWager
        elif (self.player.blackjack and not self.dealer.blackjack):
            self.player.money += self.totalWager * 2
        elif(self.dealer.blackjack and not self.player.blackjack):
            self.player.money -= self.totalWager
        elif (self.dealer.blackjack and self.player.blackjack):
            print('push')#ADD PUSH
        elif (self.checkCardTotal(self.player.hand) == self.checkCardTotal(self.dealer.hand)):
            self.player.money -= self.totalWager
        elif (self.checkCardTotal(self.player.hand) > self.checkCardTotal(self.dealer.hand)):
            self.player.money += self.totalWager
        else:
            self.player.money -= self.totalWager
        self.numGames -= 1
        self.gameEnd = True
    
    def newGame(self):
        self.player.newHand()
        self.dealer.newHand()
        self.playerBust = False
        self.dealerBust = False
        self.numGames -= 1
        self.split = False
        self.canSplit = False
        self.canDoubleDown = True
        self.doubleDown = False
        self.totalWager = 50
        self.gameEnd = False
        return



    def onevent(self, event: pygame.event):
        """ called from :func:`PlethoraAPI.mainloop` when there is an event while this game is running
        Args:
            event: a pygame.event fetched from :func:`pygame.event.get` in
                :func:`arcade.plethoraAPI.PlethoraAPI.mainloop`
        Returns:
            bool: True if onrender should be called on the next frame; False otherwise
        """
        if event.type == pygame.QUIT:
            self.onexit()
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down_pos = event.pos
                self.clicked = True
                return True
        elif event.type == KEYDOWN:
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
        arrows = self.arrows & ~self.arrows_hidden

        if arrows & ArrowMask.up:
            self.select[self.selected] = False
            self.selected -= 1 if self.selected > 0 else -3
            self.select[self.selected] = True
        if arrows & ArrowMask.right or self.clicked:
            if(self.gameEnd):
                self.newGame()
                return True
            self.clicked = False
            continueRound = True
            if (self.plusButton.collidepoint(self.mouse_down_pos) and self.totalWager < self.player.money):
                self.totalWager += 50
            elif (self.minusButton.collidepoint(self.mouse_down_pos)):
                self.totalWager -= 50
            elif (self.stayButton.collidepoint(self.mouse_down_pos)):
                self.playerStayed = True
                continueRound = self.hit(False)
            elif (self.hitButton.collidepoint(self.mouse_down_pos)):
                continueRound = self.hit()
            elif (self.doubleDownButton.collidepoint(self.mouse_down_pos)):
                self.playerDoubleDown()
                continueRound = self.hit()
            elif (self.splitButton.collidepoint(self.mouse_down_pos) and self.canSplit):
                self.playerDoubleDown()
                self.playerSplit()
                continueRound = self.hit()
            elif (pygame.Rect(self.getMenuBottonLocation()).collidepoint(self.mouse_down_pos)):
                    self.exitWarningScreen = True
            elif (self.confirmExitButton.collidepoint(self.mouse_down_pos)):
                    self.onexit()
            elif (self.rejectExitButton.collidepoint(self.mouse_down_pos)):
                    self.exitWarningScreen = False
            if(arrows & ArrowMask.right):
            #The dealer may take another card but won't if over 16
                if (self.select[0]):
                    self.playerStayed = True
                    continueRound = self.hit(False)
                elif (self.select[1]):
                    continueRound = self.hit()
                elif (self.select[2]):
                    self.playerDoubleDown()
                    continueRound = self.hit()
                elif (self.select[3]):
                    self.doubleDown()
                    self.split()
                    continueRound = self.hit()
            if (not continueRound):
                self.onGameEnd()
        if arrows & ArrowMask.down:
            self.select[self.selected] = False
            self.selected += 1 if self.selected < 3 else -3
            self.select[self.selected] = True
        if arrows & ArrowMask.left:
            self.onexit()



        

        pygame.draw.rect(self.display, (193, 193, 199),(self.rect.width-190,80,180,50))
        self.display.blit(self.biggerFont.render(('$'+str(self.player.money)), True, (0,0,0)), (self.rect.width-140, 90))
        pygame.draw.rect(self.display, (193, 193, 199),(self.rect.width-183,200,145,45))
        self.display.blit(self.smallFont.render(('$'+str(self.totalWager)), True, (255,0,0)), (self.rect.width-132, 210))
        pygame.draw.rect(self.display, (112, 61, 34),self.plusButton)
        self.display.blit(self.smallFont.render(('+'), True, (245, 245, 66)), (self.rect.width-28, 197))
        pygame.draw.rect(self.display, (112, 61, 34),(self.minusButton))
        self.display.blit(self.smallFont.render(('-'), True, (245, 245, 66)), (self.rect.width-25, 218))

        pygame.draw.rect(self.display, (205, 205, 210) if self.select[0] else (143, 143, 149), self.stayButton)
        self.display.blit(self.smallFont.render('Stay', True, (0,0,0)), (self.rect.width-126, 285))
        pygame.draw.rect(self.display, (205, 205, 210) if self.select[1] else (143, 143, 149), self.hitButton)
        self.display.blit(self.smallFont.render('Hit', True, (0,0,0)), (self.rect.width-115, 345))
        if (self.canDoubleDown):
            pygame.draw.rect(self.display, (205, 205, 210) if self.select[2] else (143, 143, 149),self.doubleDownButton)
            self.display.blit(self.smallFont.render('Double Down', True, (0,0,0)), (self.rect.width-176, 405))
        if (self.canSplit):
            pygame.draw.rect(self.display, (205, 205, 210) if self.select[3] else (143, 143, 149),self.splitButton)
            self.display.blit(self.smallFont.render('Split', True, (0,0,0)), (self.rect.width-127, 464))
        pygame.draw.rect(self.display, (205, 205, 210) if self.select[2] else (143, 143, 149),self.getMenuBottonLocation())
        self.display.blit(self.smallFont.render('Back to Menu', True, (0,0,0)), (self.rect.width-177, self.getMenuBottonLocation()[1]+5))
        
        rerender = False
        rerender = bool(arrows)  # return True if an arrow key is down; otherwise False
        for i in range(len(self.player.hand)):

            self.display.blit(self.player.hand[i].image, (self.bottomCardStart[0]-(i*110),self.rect.height-243))
            #self.display.blit(self.player.hand[i].image, (430+(i*110),self.rect.height-243))
        for i in range(len(self.dealer.hand)):
            if (i==0):
                self.display.blit(self.dealer.hand[i].image, self.topCardStart)
            else:
                self.display.blit(self.dealer.hand[i].image, (self.topCardStart[0]+(i*110), 10))
        if (self.gameEnd):
            displayName = "Dealer" if self.playerBust else "Player"
            pygame.draw.rect(self.display, (0, 0, 0),(self.rect.width/2 - 200,280,200,45))
            self.display.blit(self.smallFont.render((displayName+' Won'), True, (255,0,0)), (self.rect.width/2 - 169, 287))
        
        if(self.exitWarningScreen):
            pygame.draw.rect(self.display, (0,0,0),self.exitWarningScreenBox)
            self.display.blit(self.smallFont.render('Are you sure', True, (237,28,36)), (self.exitWarningScreenBoxText))
            self.display.blit(self.smallFont.render('you want to quit?', True, (237,28,36)), (self.exitWarningScreenBoxText[0]-20, self.exitWarningScreenBoxText[1]+30))
            pygame.draw.rect(self.display, (34,177,76),self.confirmExitButton)
            self.display.blit(self.smallFont.render('Yes', True, (255,255,255)), (self.confirmExitButton[0]+20, self.confirmExitButton[1]+5))
            pygame.draw.rect(self.display, (237,28,36),self.rejectExitButton)
            self.display.blit(self.smallFont.render('No', True, (255,255,255)), (self.rejectExitButton[0]+25, self.rejectExitButton[1]+5))

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
        def newHand(self, deck={}):
            self.hand = []
            self.addCard(deck=deck, randomCard=True)
            self.addCard(deck=deck, randomCard=True)
        class card:
            def __init__(self, cardName=None, suit=None, randomCard=False, deck={}):
                if (randomCard):
                    self.name, self.suit = self.randomCard(deck)
                else:
                    self.name = cardName
                    self.suit = suit
                # print(os.getcwd())
                self.image = pygame.image.load(str(IMAGES/f'cards/{self.name}_of_{self.suit}.png'))
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
                        self.randomCard(deck)
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
        
    
    
        

        


            
        

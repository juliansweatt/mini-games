import random

import pygame
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
class Game(plethoraAPI.Game):


    def __init__(self, humanPlayer=None, numNPC=3, numGames=10):
        super().__init__(size=(800, 600), fps=12)  # call plethoraAPI.Game.__init__ to initialize :attr:`size` and :attr:`fps`
        self.arrows = 0b0000  # bitmask for arrow keys
        self.arrows_hidden = 0b0000  # bitmask for hiding opposite keys on key down while that key is down
        self.player = humanPlayer or self.playerOrNpc("Player", None, 500)
        self.playerBust = False
        self.npc = []
        for i in range(numNPC):
            self.npc.append(self.playerOrNpc("NPC "+str(i), None, 500))
        self.cardBack = pygame.image.load('cards\\back.png')
        self.cardBack = pygame.transform.scale(self.cardBack, (86, 120))
        self.betBoxFont = pygame.font.SysFont('Arial', 18)
        self.smallFont = pygame.font.SysFont('Arial', 25)
        self.biggerFont = pygame.font.SysFont('Arial', 30)
        self.totalWager = 0
        self.pendingWager = 0
        self.currentWager = 0
        self.select = [True, False, False, False]
        self.selected = 0
        self.deck={}
        self.gameEnd = False
        self.canCall = True
        self.canCheck = True
        self.topCardStart = (10, 10)
        self.npcCardStart = [(10, 10), (10, self.rect.height-260), (430, 10)]
        self.bottomCardStart = (430, self.rect.height-260)
        self.shardCardStart = (108, 250)
        self.plusButton = pygame.Rect(self.rect.width-34,200,26,22)
        self.minusButton = pygame.Rect(self.rect.width-34,224,26,21)
        self.checkButton = pygame.Rect(self.rect.width-180,280,160,40)
        self.betButton = pygame.Rect(self.rect.width-180,340,160,40)
        self.foldButton = pygame.Rect(self.rect.width-180,400,160,40)
        self.clicked = False


        self.gamePhase = 0 #0 - Start #1 - Flop #2 - ??? #3 - ??? 
        self.dealer = self.playerOrNpc("Dealer", None, 0)
        








    def onevent(self, event: pygame.event):
        """ called from :func:`PlethoraAPI.mainloop` when there is an event while this game is running
        Args:
            event: a pygame.event fetched from :func:`pygame.event.get` in
                :func:`arcade.plethoraAPI.PlethoraAPI.mainloop`
        Returns:
            bool: True if onrender should be called on the next frame; False otherwise
        """
        
        """
        elif event.type == MOUSEMOTION:
            if self.mouse_down_pos:
                self.mouse_down_pos = event.pos
                return True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_down_pos = None
                return True
        """
        if event.type == MOUSEBUTTONUP:
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

    def newGame(self):
        self.currentWager = 0
        self.pendingWager = 0
        self.gamePhase = 0
        self.gameEnd = False
        self.dealer.newHand(self.deck)
        self.player.newHand(self.deck)
        for i in range(len(self.npc)):
            self.npc[i].newHand(self.deck)

    def npcsTurn(self):
        for i in range(len(self.npc)):
            self.bet(self.npc[i])
        
        #Next Game Phase
        self.gamePhase += 1
        if (self.gamePhase == 3):
            self.gameEnd = True
        self.dealer.addCard(randomCard=True)
        self.currentWager = 0

    def bet(self, player):
        player.money -= self.currentWager
        self.totalWager += self.currentWager
    
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
        if (self.gameEnd):
            self.newGame()

        
        arrows = self.arrows & ~self.arrows_hidden
        if (self.clicked):
            self.clicked = False
            if (self.plusButton.collidepoint(self.mouse_down_pos) and self.pendingWager < self.player.money):
                self.pendingWager += 50
            elif (self.minusButton.collidepoint(self.mouse_down_pos) and self.pendingWager > self.currentWager):
                self.pendingWager -= 50
            elif (self.checkButton.collidepoint(self.mouse_down_pos) and self.canCall):
                self.currentWager = 0
                self.pendingWager = 0
                self.player.lastWager = "Check"
                self.npcsTurn()
            elif (self.betButton.collidepoint(self.mouse_down_pos) and self.pendingWager >= self.currentWager):
                self.currentWager = self.pendingWager
                self.player.lastWager = str(self.currentWager)
                self.bet(self.player)
                self.npcsTurn()
            elif (self.foldButton.collidepoint(self.mouse_down_pos)):
                self.player.fold = True
        if arrows & ArrowMask.up:
            self.select[self.selected] = False
            self.selected -= 1 if self.selected > 0 else -3
            self.select[self.selected] = True
        if arrows & ArrowMask.right:
            if(self.gameEnd):
                self.newGame()
                return True
            #The dealer may take another card but won't if over 16
            if (self.select[0]):
                continueRound = self.hit(False)
            if (self.select[1]):
                continueRound = self.hit()
            if (self.select[2]):
                self.playerDoubleDown()
                continueRound = self.hit()
            if (self.select[3]):
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

        if (self.gameEnd):
            playerWin = False
            if (self.player.getHandValue(self.dealer.hand) > self.npc[0].getHandValue(self.dealer.hand)):
                playerWin = True
            elif (self.player.getHandValue(self.dealer.hand) < self.npc[0].getHandValue(self.dealer.hand)):
                playerWin = False
            elif (self.player.getHandValue(self.dealer.hand) == self.npc[0].getHandValue(self.dealer.hand)):
                if (self.player.highCardValue > self.npc[0].highCardValue):
                    playerWin = True
                elif (self.player.highCardValue < self.npc[0].highCardValue):
                    playerWin = False
                if (self.player.highCardValue == self.npc[0].highCardValue):
                    playerWin = True
            self.player.money += self.totalWager if playerWin else (self.totalWager*-1)
            print('Player Score:', self.player.getHandValue(self.dealer.hand))
            print('Npc Score:', self.npc[0].getHandValue(self.dealer.hand))
            



        #Create the UI on the right side of the screen
        pygame.draw.rect(self.display, (193, 193, 199),(self.rect.width-190,80,180,50))
        self.display.blit(self.biggerFont.render(('$'+str(self.player.money)), True, (0,0,0)), (self.rect.width-140, 90))
        pygame.draw.rect(self.display, (193, 193, 199),(self.rect.width-183,200,145,45))
        self.display.blit(self.smallFont.render(('$'+str(self.pendingWager)), True, (255,0,0)), (self.rect.width-132, 210))
        pygame.draw.rect(self.display, (112, 61, 34),self.plusButton)
        self.display.blit(self.smallFont.render(('+'), True, (245, 245, 66)), (self.rect.width-28, 197))
        pygame.draw.rect(self.display, (112, 61, 34),(self.minusButton))
        self.display.blit(self.smallFont.render(('-'), True, (245, 245, 66)), (self.rect.width-25, 218))

        pygame.draw.rect(self.display, (205, 205, 210) if self.select[0] else (143, 143, 149), (self.rect.width-365,380,130,80))
        self.display.blit(self.betBoxFont.render('Last Bet', True, (0,0,0)), (self.rect.width-335, 390))
        self.display.blit(self.betBoxFont.render('$'+self.player.lastWager, True, (0,0,0)), (self.rect.width-326, 415))

        pygame.draw.rect(self.display, (205, 205, 210) if self.select[0] else (143, 143, 149),(self.rect.width-180,280,160,40))
        self.display.blit(self.smallFont.render('Check', True, (0,0,0)), (self.rect.width-127, 285))
        pygame.draw.rect(self.display, (205, 205, 210) if self.select[1] else (143, 143, 149),(self.rect.width-180,340,160,40))
        self.display.blit(self.smallFont.render('Bet', True, (0,0,0)), (self.rect.width-127, 345))
        pygame.draw.rect(self.display, (205, 205, 210) if self.select[2] else (143, 143, 149),(self.rect.width-180,400,160,40))
        self.display.blit(self.smallFont.render('Fold', True, (0,0,0)), (self.rect.width-127, 405))
        
        rerender = False
        rerender = bool(arrows)  # return True if an arrow key is down; otherwise False
        
        self.display.blit(self.cardBack, (self.shardCardStart[0]-98, self.shardCardStart[1]))
        if (self.gamePhase > 0):
            for i in range(len(self.dealer.hand)):
                self.display.blit(self.dealer.hand[i].image, (self.shardCardStart[0]+(i*98), self.shardCardStart[1]))

        #Display the cards on the for the player
        for i in range(len(self.player.hand)):
            self.display.blit(self.player.hand[i].image, (self.bottomCardStart[0]+(i*50),self.rect.height-130))
            #self.display.blit(self.player.hand[i].image, (430+(i*110),self.rect.height-243))
        #Display the cards on the for the Dealer

        for num, npc in enumerate(self.npc):
            for i in range(len(npc.hand)):
                if (i==10):
                    self.display.blit(npc.hand[i].image, self.npcCardStart[num])
                else:
                    self.display.blit(npc.hand[i].image, (self.npcCardStart[num][0]+(i*60), 10))
        

        if (self.gameEnd):
            displayName = "Player" if playerWin else "NPC"
            pygame.draw.rect(self.display, (0, 0, 0),(self.rect.width/2 - 200,280,200,45))
            self.display.blit(self.smallFont.render((displayName+' Won'), True, (255,0,0)), (self.rect.width/2 - 169, 287))

        
        print(self.selected)
        return rerender



    class playerOrNpc:
        def __init__(self, playerName, hand=None, money=0, isNPC=False):
            self.name = playerName
            if(hand):
                self.hand = hand
            else:
                self.hand = [self.card(randomCards=True), self.card(randomCards=True)]

            if(money):
                self.money = money
            self.handValue = 0
            self.highCardValue = 0
            self.npc = isNPC
            self.canCheck = False
            self.lastWager = '0'
            self.fold = False
        def newHand(self, deck={}):
            self.hand = []
            self.addCard(deck=deck, randomCard=True)
            self.addCard(deck=deck, randomCard=True)

        def addCard(self, card=None, deck={}, randomCard=False):
            if (randomCard):
                card = self.card(randomCards=True, deck=deck)
            self.hand.append(card)
            return card
        def getStraightOrFlushValue(self, shardCards=[]):
            sharedHand = self.hand + shardCards
            if(len(sharedHand) < 5):
                return 0
            flush = False
            straightFlush = False
            currentStraight = []
            numbers = [card.getNumber() for card in sharedHand]
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
            suits = [card.suit for card in sharedHand]
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
                for card in sharedHand:
                    if (card.suit == flush and card.getNumber() > self.highCardValue):
                        self.highCardValue = card.getNumber()
                for num in currentStraight:
                    for card in sharedHand:
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
            
        def getPairValue(self, shardCards=[]):
            pair = 0
            sharedHand = self.hand + shardCards
            numbers = [card.getNumber() for card in sharedHand]
            uniqueNumbers = []
            for num in numbers:
                if (num not in uniqueNumbers):
                    uniqueNumbers.append(num)
            uniqueNumbers.sort(reverse=True)
            for num in uniqueNumbers:
                if (numbers.count(num) == 2 and pair == 0):
                    pair = 1
                    self.highCardValue = num
                elif(numbers.count(num) == 2 and pair == 1):
                    pair = 2
                    self.highCardValue = num if num > self.highCardValue else self.highCardValue
                elif(numbers.count(num) == 3 and pair == 0):
                    pair = 3
                    self.highCardValue = num if num > self.highCardValue else self.highCardValue
                elif (numbers.count(num) == 2 and pair == 3):
                    pair = 5
                elif (numbers.count(num) == 3 and (pair == 1 or pair == 2)):
                    pair = 5
                    #ADD Full House Edge Cases (Adding decimal values?)
                    self.highCardValue = num
                elif(numbers.count(num) == 4):
                    pair = 4
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
                self.highCardValue = max(numbers)
                return 0
            
        def getHandValue(self, sharedCards=[]):
            print(self.name+'PairValue:', self.getPairValue(sharedCards))
            print(self.name+'StraightorFlush:', self.getStraightOrFlushValue(sharedCards))
            return self.getPairValue(sharedCards) if self.getStraightOrFlushValue(sharedCards) < self.getPairValue(sharedCards) else self.getStraightOrFlushValue(sharedCards)

        class card:
            def __init__(self, cardName=None, suit=None, randomCards=False, deck={}):
                if (randomCards):
                    self.name, self.suit = self.randomCard(deck)
                else:
                    self.name = cardName
                    self.suit = suit
                self.image = pygame.image.load('cards\\' + self.name + "_of_" + self.suit + ".png")
                #self.image = pygame.transform.scale(self.image, (160, 233))
                self.image = pygame.transform.scale(self.image, (86, 120))
            
        
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
            
            def getNumber(self):
                if (self.name == "jack"):
                    return 11
                elif(self.name == "queen"):
                    return 12
                elif (self.name == "king"):
                    return 13
                elif (self.name == "ace"):
                    return 14
                else:
                    return int(self.name)
        


            
            
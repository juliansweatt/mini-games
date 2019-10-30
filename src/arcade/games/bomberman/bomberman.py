#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os.path
from arcade import plethoraAPI
from arcade.games.bomberman.spritesheet import SpriteSheet
from arcade.games.bomberman.spritesheet import SpriteResourceReference
from arcade.games.bomberman.spritesheet import SpriteBook

# Color Definitions
AVATAR_TRANSPARENT_GREEN = (64, 144, 56)
TILE_TRANSPARENT_YELLOW = (255, 255, 128)

class GameConfig():
    def __init__(self):
        self.gameHeight = 600
        self.gameWidth = 800
        self.gamePath = os.path.join('src', 'arcade', 'games','bomberman')
        self.assetPath = os.path.join(self.gamePath, 'assets')
        self.sprites = {
            "avatars.png": (
                SpriteResourceReference("bomber_w_neutral",71,45,17,26,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying1",29,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying2",48,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying3",65,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying4",82,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying5",99,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying6",117,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_turning_r_1",87,45,17,26,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_turning_r_2",105,46,17,26,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_turning_r_3",122,47,16,25,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_turning_r_4",138,48,17,25,AVATAR_TRANSPARENT_GREEN)
            ),
            "tiles.png": (
                SpriteResourceReference("bomb_s_inactive", 508,184,18,18, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("bomb_m_inactive", 525,184,18,18, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("bomb_l_inactive", 542,184,18,18, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("bomb_s_active", 406,116,18,18, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("bomb_m_active", 423,184,18,18, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("bomb_l_active", 440,184,18,18, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("grass", 474,14,18,18, TILE_TRANSPARENT_YELLOW),
            )
        }

class Bomberman(plethoraAPI.Game):
    def __init__(self) -> None:
        self.config = GameConfig()
        super().__init__(size=(self.config.gameWidth, self.config.gameHeight), fps=10)
        self.bomberSprites = pygame.sprite.Group()
        self.bombSprites = pygame.sprite.Group()
        self.spriteDict = SpriteBook(self.config.sprites, self.config.assetPath).getAllSprites()
        # --- Test Sprite Render --- #
        deathAnimation = list()
        deathAnimation.append(self.spriteDict["bomber_w_dying1"])
        deathAnimation.append(self.spriteDict["bomber_w_dying2"])
        deathAnimation.append(self.spriteDict["bomber_w_dying3"])
        deathAnimation.append(self.spriteDict["bomber_w_dying4"])
        deathAnimation.append(self.spriteDict["bomber_w_dying5"])
        deathAnimation.append(self.spriteDict["bomber_w_dying6"])
        self.p1 = Bomber(self.spriteDict["bomber_w_neutral"], deathAnimation = deathAnimation)
        self.bomberSprites.add(self.p1)


    def onevent(self, event: pygame.event) -> bool:
        if event.type == pygame.QUIT:
            self.onexit()
        if event.type == pygame.KEYDOWN:
            # --- Test Death Animation --- #
            self.p1.death()
            return True
        return False

    def onrender(self) -> bool:
        needsUpdate = False
        pygame.display.flip()
        self.bomberSprites.draw(self.display)
        self.bombSprites.draw(self.display)
        if self.p1.needsUpdate(): # TODO Update to check all characters update status
            needsUpdate = True
            self.bomberSprites.update()
        return needsUpdate

class Bomber(pygame.sprite.Sprite):
    def __init__(self, neutralImage, *, deathAnimation):
        super().__init__()
        # Load the image
        self.neutralImage = neutralImage
        self.image = self.neutralImage
        self.images = list()
        self.index = 0
        self.state = 'neutral'
        self.rect = self.image.get_rect()
        self.animations = dict()
        self.animations['death'] = deathAnimation
        self.animating = False
    
    def setState(self, state):
        self.index = 0
        if self.animations.get(state):
            self.images = self.animations[state]
        else:
            self.images = list()

    def death(self):
        self.setState('death')
        self.state = 'death'
        self.animating = True
    
    def needsUpdate(self):
        return self.animating

    def update(self):
        if self.state == 'death' and self.index == len(self.animations['death'])-1:
            # Stop Updating
            self.animating = False
            self.state = 'dead'
        else:
            if self.state != 'neutral' and type(self.images) == list:
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                
                if self.index < len(self.images):
                    self.image = self.images[self.index]

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        # Load the image
        self.image = image
        self.rect = self.image.get_rect()

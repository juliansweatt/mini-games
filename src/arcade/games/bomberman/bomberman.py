#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os.path
from arcade import plethoraAPI
from arcade.common.spritesheet import SpriteResourceReference, SpriteSheet, SpriteBook
from arcade.common.graphicsManager import AnimatedEntity, Graphic

# Color Definitions
AVATAR_TRANSPARENT_GREEN = (64, 144, 56)
TILE_TRANSPARENT_YELLOW = (255, 255, 128)

class GameConfig():
    def __init__(self):
        self.gameHeight = 800
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
                SpriteResourceReference("grass", 475,15,16,16, TILE_TRANSPARENT_YELLOW),
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
        self.p1.setScale((50,50))
        self.bomberSprites.add(self.p1)
        # --- Test Map --- #
        self.map = Map(self.spriteDict, self.config.gameWidth, self.config.gameHeight)

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
        self.map.update(self.display)
        self.bomberSprites.draw(self.display)
        self.bombSprites.draw(self.display)
        if self.p1.needsUpdate(): # TODO Update to check all characters update status
            needsUpdate = True
            self.bomberSprites.update()
        return needsUpdate

class Bomber(AnimatedEntity):
    def __init__(self, neutralImage, *, deathAnimation):
        AnimatedEntity.__init__(self, neutralImage, deathAnimation)

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        # Load the image
        self.image = image
        self.rect = self.image.get_rect()

class Tile(Graphic):
    def __init__(self, surfaceName=False, surfaceImage=False, scale=False, *, destructable=False):
        self.destructable = destructable
        self.surface = 'grass' # Example, fix, default background
        self.graphicsLive = False
        if surfaceName and surfaceImage:
            self.setSurface(surfaceName, surfaceImage)
            if scale:
                self.setScale(scale)

    def __setImage__(self, image):
        if not self.graphicsLive:
            Graphic.__init__(self, image)
            self.graphicsLive = True

    def setSurface(self, surface, image):
        self.surface = surface
        self.__setImage__(image)

    def setScale(self, scale):
        Graphic.setScale(self, scale)


class Map():
    def __init__(self, spriteDict, gameWidth, gameHeight):
        self.width = 10
        self.height = 10
        self.graphicsLibrary = spriteDict
        self.scaleWidth = int(gameWidth/10)
        self.scaleHeight = int(gameHeight/10)
        self.reset()
    
    def reset(self):
        self.map = []
        for col in range(self.width):
            self.map.append([])
            for cell in range(self.height):
                self.map[col].append(Tile('grass', self.graphicsLibrary.get('grass'), (self.scaleWidth,self.scaleHeight)))

    def update(self, display):
        for colNum, col in enumerate(self.map):
            for rowNum, tile in enumerate(col):
                if tile.graphicsLive:
                    display.blit(tile.image, (self.scaleWidth * colNum, self.scaleHeight * rowNum))
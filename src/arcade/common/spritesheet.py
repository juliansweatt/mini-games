#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os.path

class SpriteResourceReference():
    def __init__(self, spriteName: str, xCoordinate: int, yCoordinate: int, width: int, height: int, transparentColorRGB):
        self.name = spriteName
        self.x = xCoordinate
        self.y = yCoordinate
        self.width = width
        self.height = height
        self.transparent = transparentColorRGB

# Based On: http://programarcadegames.com/python_examples/en/sprite_sheets/
class SpriteSheet():
    def __init__(self, fileName):
        self.sprite_sheet = pygame.image.load(fileName).convert()
 
    def getSprite(self, sprite: SpriteResourceReference):
        image = pygame.Surface((sprite.width, sprite.height)).convert()
        image.blit(self.sprite_sheet, (0, 0), (sprite.x, sprite.y, sprite.width, sprite.height))
        image.set_colorkey(sprite.transparent)
        return image

    def getSprites(self, sprites: list):
        images = dict()
        for sprite in sprites:
            image = self.getSprite(sprite)
            images[sprite.name] = image
        return images

# Create a sprite book which will return all of the surfaces from all of the sprite sheets
class SpriteBook():
    def __init__(self, importConfig, assetPath):
        self.specs = importConfig
        self.assetPath = assetPath
    
    def getAllSprites(self):
        sprites = dict()
        for filePath, spriteList in self.specs.items():
            fullPath = os.path.join(self.assetPath, filePath)
            if type(spriteList) is SpriteResourceReference:
                sprites[spriteList.name] = SpriteSheet(fullPath).getSprite(spriteList)
            else:
                sprites.update(SpriteSheet(fullPath).getSprites(spriteList))
        return sprites

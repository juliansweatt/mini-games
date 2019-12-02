#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os.path
from typing import List, Dict

class SpriteResourceReference():
    """Specifications for an external sprite resource.

    """
    def __init__(self, resource_name:str, x: int, y: int, width: int, height: int, transparent_color_code:tuple):
        """Create a new Sprite Resource Reference

        :param str resource_name: Name or label of the resource.
        :param int x: Top-left x-coordinate of the resource on the sprite sheet.
        :param int y: Top-left y-coordinate of the resource on the sprite sheet.
        :param int width: Horizontal size of the sprite on the sprite sheet.
        :param int height: Vertical size of the sprite on the sprite sheet.
        :param tuple transparent_color_code: Color used as the transparent background on the sprite sheet (RGB Format).
        :return: Newly instantiated Sprite Resource Reference
        :rtype: SpriteResourceReference
        """
        self.name = resource_name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.transparent = transparent_color_code

# Based On: http://programarcadegames.com/python_examples/en/sprite_sheets/
class SpriteSheet():
    """Sprite sheet references for one sprite sheet document.

    """
    def __init__(self, file_name:str):
        """Create a new Sprite Sheet

        :param str file_name: File name of the sprite sheet document.
        :return: Newly instantiated Sprite Sheet
        :rtype: SpriteSheet
        """
        self.sprite_sheet = pygame.image.load(file_name).convert()
 
    def get_sprite(self, sprite: SpriteResourceReference) -> pygame.image:
        """Retrieve a single sprite from the Sprite Sheet.

        :param SpriteResourceReference sprite: Sprite to retrieve.
        :return: Retrieved sprite resource.
        :rtype: pygame.image
        """
        image = pygame.Surface((sprite.width, sprite.height)).convert()
        image.blit(self.sprite_sheet, (0, 0), (sprite.x, sprite.y, sprite.width, sprite.height))
        image.set_colorkey(sprite.transparent)
        return image

    def get_sprites(self, sprites: list) -> List[object]:
        """Get several sprites from the Sprite Sheet.

        :param list sprites: A list of SpriteResourceReferences to retrieve.
        :return: List of sprite resources.
        :rtype: List[pygame.image]:
        """
        images = dict()
        for sprite in sprites:
            image = self.get_sprite(sprite)
            images[sprite.name] = image
        return images

# Create a sprite book which will return all of the surfaces from all of the sprite sheets
class SpriteBook():
    """An accumulation of Sprite Sheets.

    """
    def __init__(self, import_config:dict, asset_path:str):
        """Create a SpriteBook.

        :param dict import_config: Import specification object. Key is the filename, value is a SpriteSheet.
        :param str asset_path: Path to the assets file.
        :return: Newly instantiated SpriteBook
        :rtype: SpriteBook
        """
        self.specs = import_config
        self.asset_path = asset_path
    
    def get_all_sprites(self) -> Dict[str, object]:
        """Get all sprite resources defined in a Sprite Book.

        :return: Dict of all images in the Sprite Book.
        :rtype: Dict[str, pygame.image]
        """
        sprites = dict()
        for file_path, sprite_list in self.specs.items():
            full_path = os.path.join(self.asset_path, file_path)
            if type(sprite_list) is SpriteResourceReference:
                sprites[sprite_list.name] = SpriteSheet(full_path).get_sprite(sprite_list)
            else:
                sprites.update(SpriteSheet(full_path).get_sprites(sprite_list))
        return sprites

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os.path
import random
from arcade import plethoraAPI
from arcade.common.spritesheet import SpriteResourceReference, SpriteSheet, SpriteBook
from arcade.common.graphicsManager import AnimatedEntity, Graphic, Animation, AnimationFrame

# Color Definitions
AVATAR_TRANSPARENT_GREEN = (64, 144, 56)
TILE_TRANSPARENT_YELLOW = (255, 255, 128)

class GameConfig():
    def __init__(self):
        self.gameHeight = 800
        self.gameWidth = 800
        self.gamePath = os.path.join('src', 'arcade', 'games','bomberman')
        self.assetPath = os.path.join(self.gamePath, 'assets')
        self.playableTilesX = 19
        self.playableTilesY = 17
        self.totalTilesX = self.playableTilesX + 2
        self.totalTilesY = self.playableTilesY + 4
        self.tileWidth = int(self.gameWidth/self.totalTilesX)
        self.tileHeight = int(self.gameWidth/self.totalTilesY)
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
                # SpriteResourceReference("bomb_s_inactive", 508,184,18,18, TILE_TRANSPARENT_YELLOW),
                # SpriteResourceReference("bomb_m_inactive", 525,184,18,18, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("bomb_l_inactive", 543,185,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("bomb_l_active", 441,117,16,16, TILE_TRANSPARENT_YELLOW),
                # SpriteResourceReference("bomb_s_active", 406,116,18,18, TILE_TRANSPARENT_YELLOW),
                # SpriteResourceReference("bomb_m_active", 423,184,18,18, TILE_TRANSPARENT_YELLOW),
                # SpriteResourceReference("bomb_l_active", 440,184,18,18, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("terrain", 475,15,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("destructable_new", 458,32,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("solid", 475,32,16,16, TILE_TRANSPARENT_YELLOW),
                # Wall Numbering is Left -> Right, Top -> Bottom on the Sprite Sheet
                SpriteResourceReference("wall_1", 407,15,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_2", 424,15,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_3", 441,15,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_4", 458,15,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_5", 407,32,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_6", 424,32,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_7", 424,49,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_8", 407,66,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_9", 424,66,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_10", 407,83,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_11", 424,83,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("wall_12", 441,83,16,16, TILE_TRANSPARENT_YELLOW)
            )
        }

class Bomberman(plethoraAPI.Game):
    def __init__(self) -> None:
        self.config = GameConfig()
        super().__init__(size=(self.config.gameWidth, self.config.gameHeight), fps=20)
        self.bomberSprites = pygame.sprite.Group()
        self.bombSprites = pygame.sprite.Group()
        self.spriteDict = SpriteBook(self.config.sprites, self.config.assetPath).getAllSprites()

        # --- Test Map --- #
        self.map = Map(self.spriteDict, self.config.totalTilesX, self.config.totalTilesY, self.config.tileWidth, self.config.tileHeight)
        # --- Test Sprite Render --- #
        death_animation = Animation()
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying1"]))
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying2"]))
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying3"]))
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying4"]))
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying5"]))
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying6"]))

        self.bomb_ticking_animation = Animation()
        self.bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_inactive"], 10))
        self.bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_active"], 10))
        self.bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_inactive"], 5))
        self.bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_active"], 5))
        self.bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_inactive"], 3))
        self.bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_active"], 3))
        self.bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_inactive"], 1))
        self.bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_active"], 1))

        self.p1 = Bomber(self.spriteDict["bomber_w_neutral"], deathAnimation = death_animation)
        p1_spawn_tile_xy = self.map.assign_spawn_point()
        p1_spawn_tile = self.map.map[p1_spawn_tile_xy[0]][p1_spawn_tile_xy[1]]
        self.p1.set_scale((self.config.tileWidth,self.config.tileHeight))
        self.p1.place_at(p1_spawn_tile.rect.center)
        self.bomberSprites.add(self.p1)

    def onevent(self, event: pygame.event) -> bool:
        if event.type == pygame.QUIT:
            self.onexit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return self.p1.toggle_movement('left')
            elif event.key == pygame.K_RIGHT:
                return self.p1.toggle_movement('right')
            elif event.key == pygame.K_UP:
                return self.p1.toggle_movement('up')
            elif event.key == pygame.K_DOWN:
                return self.p1.toggle_movement('down')
            elif event.key == pygame.K_SPACE:
                # Drop bomb (player 1)
                b = Bomb(self.spriteDict.get("bomb_l_inactive"), deathAnimation=self.bomb_ticking_animation.copy())
                b.drop_bomb(self.p1.rect.center,self.map)
                b.set_scale((self.config.tileWidth,self.config.tileHeight))
                self.bombSprites.add(b)
                return True
            # else:
            #     # --- Test Death Animation --- #
            #     self.p1.death()
            #     return True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                return self.p1.toggle_movement('none')
            elif event.key == pygame.K_RIGHT:
                return self.p1.toggle_movement('none')
            elif event.key == pygame.K_UP:
                return self.p1.toggle_movement('none')
            elif event.key == pygame.K_DOWN:
                return self.p1.toggle_movement('none')
        return False

    def onrender(self) -> bool:
        needsUpdate = False
        pygame.display.flip()
        self.map.update(self.display)
        self.bombSprites.draw(self.display)
        self.bomberSprites.draw(self.display)
        if self.p1.needsUpdate(): # TODO Update to check all characters update status
            needsUpdate = True
            self.bomberSprites.update()
        for bomb in self.bombSprites:
            if bomb.needsUpdate():
                needsUpdate = True
                bomb.update()
            elif not bomb.is_alive():
                # Bomb is done ticking
                # TODO Spawn an explosion in the surrounding tiles
                self.bombSprites.remove(bomb)
                needsUpdate = True
        return needsUpdate

class Bomber(AnimatedEntity):
    def __init__(self, neutralImage, *, deathAnimation):
        AnimatedEntity.__init__(self, neutralImage, deathAnimation)
    
    def place_at(self, center_coordinates):
        self.rect.center = center_coordinates

class Bomb(AnimatedEntity):
    def __init__(self, neutral_image, *, deathAnimation):
        AnimatedEntity.__init__(self, neutral_image, deathAnimation)

    def place_at(self, center_coordinates):
        self.rect.center = center_coordinates

    def drop_bomb(self, player_center, world_map):
        # Will drop bomb in the center of whatever tile the player is centered over
        tile_center = world_map.coordinates_to_tile(player_center).rect.center
        self.place_at(tile_center)
        self.death()

class Tile(Graphic):
    def __init__(self, surfaceName='terrain', surfaceImage=False, scale=False, imageRotation=0, *, destructable=False, flip_x=False, flip_y=False):
        self.destructable = destructable
        self.surface = surfaceName
        self.graphicsLive = False
        if surfaceName and surfaceImage:
            if imageRotation > 0:
                surfaceImage = pygame.transform.rotate(surfaceImage,imageRotation)
            if flip_y or flip_x:
                surfaceImage = pygame.transform.flip(surfaceImage,flip_x,flip_y)
            self.setSurface(surfaceName, surfaceImage)
            if scale:
                self.set_scale(scale)

    def __setImage__(self, image):
        if not self.graphicsLive:
            Graphic.__init__(self, image)
            self.graphicsLive = True

    def setSurface(self, surface, image):
        self.surface = surface
        self.__setImage__(image)

class Map():
    def __init__(self, spriteDict, numTilesX, numTilesY, tileWidth, tileHeight):
        self.width = numTilesX
        self.height = numTilesY
        self.graphicsLibrary = spriteDict
        self.scaleWidth = tileWidth
        self.scaleHeight = tileHeight

        self.active_spawns = 0
        self.spawn_points = [(2,1),(self.width-3, self.height-2),(self.width-3,1),(2, self.height-2)] # TODO Adjust to only buffer if the spawnpoint is active
        self.spawn_buffer = 3
        self.spawn_buffers = list()
        for spawn in self.spawn_points:
            for i in range(self.spawn_buffer):
                for j in range(self.spawn_buffer):
                    self.spawn_buffers.append((spawn[0]+i, spawn[1]+j))
                    self.spawn_buffers.append((spawn[0]-i, spawn[1]+j))
                    self.spawn_buffers.append((spawn[0]+i, spawn[1]-j))
                    self.spawn_buffers.append((spawn[0]-i, spawn[1]-j))

        self.reset()

    def assign_spawn_point(self):
        spawn_tile = self.spawn_points[self.active_spawns]
        self.active_spawns += 1
        return spawn_tile

    def reset(self):
        self.map = []
        for col in range(self.width):
            self.map.append([])
            for cell in range(self.height):
                if col > 1 and col < self.width - 2:
                    if cell == 0:
                        # World Barrier - Top Middle
                        self.map[col].append(Tile('wall_3', self.graphicsLibrary.get('wall_3'), (self.scaleWidth,self.scaleHeight)))
                    elif cell == self.height - 1:
                        # World Barrier - Bottom Middle
                        self.map[col].append(Tile('wall_12', self.graphicsLibrary.get('wall_12'), (self.scaleWidth,self.scaleHeight)))
                    else:
                        # Playable Map Area
                        if (col % 2) != 0 and (cell % 2) == 0:
                            # Hard-Barrier Generation
                            self.map[col].append(Tile('solid', self.graphicsLibrary.get('solid'), (self.scaleWidth,self.scaleHeight)))
                        elif (col,cell) in self.spawn_buffers:
                            # Preserve Potential Spawn Points
                            self.map[col].append(Tile('terrain', self.graphicsLibrary.get('terrain'), (self.scaleWidth,self.scaleHeight)))
                        elif random.randint(0, 2) == 0:
                            # Soft-Barrier Generation
                            self.map[col].append(Tile('destructable_new', self.graphicsLibrary.get('destructable_new'), (self.scaleWidth,self.scaleHeight), destructable="True"))
                        else:
                            # Fill Remaining Terrain
                            self.map[col].append(Tile('terrain', self.graphicsLibrary.get('terrain'), (self.scaleWidth,self.scaleHeight)))
                else:
                    # World Barrier - Side Sections
                    if col == 0 or col == self.width - 1:
                        # Roof
                        right_most_columns = False
                        if col == self.width - 1:
                            right_most_columns = True

                        if cell == self.height - 1:
                            self.map[col].append(Tile('wall_10', self.graphicsLibrary.get('wall_10'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns))
                        elif cell == self.height - 2:
                            self.map[col].append(Tile('wall_1', self.graphicsLibrary.get('wall_1'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns))
                        elif cell == 0:
                            self.map[col].append(Tile('wall_1', self.graphicsLibrary.get('wall_1'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns))
                        else:
                            self.map[col].append(Tile('wall_5', self.graphicsLibrary.get('wall_5'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns))
                    elif col == 1 or col == self.width - 2:
                        # Floor 
                        right_most_columns = False
                        if col == self.width - 2:
                            right_most_columns = True

                        if cell == self.height -1:
                            self.map[col].append(Tile('wall_11', self.graphicsLibrary.get('wall_11'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns))
                        elif cell == self.height - 2:
                            self.map[col].append(Tile('wall_9', self.graphicsLibrary.get('wall_9'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns))
                        elif cell == 0:
                            self.map[col].append(Tile('wall_2', self.graphicsLibrary.get('wall_2'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns))
                        elif cell == 1:
                            self.map[col].append(Tile('wall_6', self.graphicsLibrary.get('wall_6'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns))
                        else:
                            self.map[col].append(Tile('wall_7', self.graphicsLibrary.get('wall_7'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns))
                self.map[col][cell].placeAt(topleft=(self.scaleWidth * col, self.scaleHeight * cell))

    def update(self, display):
        for colNum, col in enumerate(self.map):
            for rowNum, tile in enumerate(col):
                if tile.graphicsLive:
                    display.blit(tile.image, tile.rect.topleft)

    def coordinates_to_tile(self, coordinates):
        for colNum, col in enumerate(self.map):
            for rowNum, tile in enumerate(col):
                if tile.rect.collidepoint(coordinates):
                    return tile
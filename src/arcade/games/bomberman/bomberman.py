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
                SpriteResourceReference("explosion_center_1", 475,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_center_2", 492,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_center_3", 509,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_center_4", 527,134,16,16, TILE_TRANSPARENT_YELLOW),
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
        # --- PyGame Core Inits --- #
        self.config = GameConfig()
        super().__init__(size=(self.config.gameWidth, self.config.gameHeight), fps=20)
        self.bomberSprites = pygame.sprite.Group()
        self.bombSprites = pygame.sprite.Group()
        self.deadlySprites = pygame.sprite.Group()

        # --- Sprite Load-In --- #
        self.spriteDict = SpriteBook(self.config.sprites, self.config.assetPath).getAllSprites()

        # --- Map Setup --- #
        self.map = Map(self.spriteDict, self.config.totalTilesX, self.config.totalTilesY, self.config.tileWidth, self.config.tileHeight)
        
        # --- Animations Setup --- #
        self.animations_library = self.generate_animations_library()

        # --- Player Initialization --- #
        self.p1 = Bomber(self.spriteDict["bomber_w_neutral"], deathAnimation=self.animations_library.get("bomber_w_death").copy(), movement_plane=self.map.map, barrier_sprites=self.bombSprites)
        p1_spawn_tile_xy = self.map.assign_spawn_point()
        p1_spawn_tile = self.map.map[p1_spawn_tile_xy[0]][p1_spawn_tile_xy[1]]
        self.p1.set_scale((int(self.config.tileWidth*.75),int(self.config.tileHeight*.75)))
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
                b = Bomb(self.spriteDict.get("bomb_l_inactive"), deathAnimation=self.animations_library.get("bomb_ticking").copy())
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
        # --- PyGame Draw Handling --- #
        needsUpdate = False
        pygame.display.flip()
        self.map.update(self.display)
        self.bombSprites.draw(self.display)
        self.deadlySprites.draw(self.display)
        self.bomberSprites.draw(self.display)

        # --- Player Updates --- #
        for player in self.bomberSprites:
            if player.needsUpdate():
                needsUpdate = True
                self.bomberSprites.update()

        # --- Bomb Updates --- #
        for bomb in self.bombSprites:
            if bomb.needsUpdate():
                needsUpdate = True
                bomb.update()
            elif not bomb.is_alive():
                explosion = Explosion(self.spriteDict.get("bomb_l_inactive"), deathAnimation=self.animations_library.get("explosion_center").copy())
                explosion.explode_at(bomb.rect.center)
                explosion.set_scale((self.config.tileWidth,self.config.tileHeight))
                self.deadlySprites.add(explosion)

                self.bombSprites.remove(bomb)
                needsUpdate = True

        # --- Explosion Updates --- #
        for deadly_sprite in self.deadlySprites:
            if deadly_sprite.needsUpdate():
                needsUpdate=True
                deadly_sprite.update()
            elif not deadly_sprite.is_alive():
                self.deadlySprites.remove(deadly_sprite)
                needsUpdate=True
        
        # --- Death Handling --- #
        kill_list = pygame.sprite.groupcollide(self.deadlySprites, self.bomberSprites, False, False)
        if len(kill_list) > 0:
            for bomber_collision_group in kill_list.values():
                for bomber in bomber_collision_group:
                    bomber.death()

        # --- End Game Handling --- #
        living_players = 0
        for bomber in self.bomberSprites:
            if bomber.is_alive():
                living_players += 1
        if living_players == 1:
            print("Game Over") # TODO 

        return needsUpdate

    def generate_animations_library(self):
        animation_library = dict()
        death_animation = Animation()
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying1"]))
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying2"]))
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying3"]))
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying4"]))
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying5"]))
        death_animation.add_frame(AnimationFrame(self.spriteDict["bomber_w_dying6"]))
        animation_library["bomber_w_death"] = death_animation

        bomb_ticking_animation = Animation()
        bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_inactive"], 10))
        bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_active"], 10))
        bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_inactive"], 5))
        bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_active"], 5))
        bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_inactive"], 3))
        bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_active"], 3))
        bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_inactive"], 1))
        bomb_ticking_animation.add_frame(AnimationFrame(self.spriteDict["bomb_l_active"], 1))
        animation_library["bomb_ticking"] = bomb_ticking_animation

        explosion_center_animation = Animation()
        explosion_center_animation.add_frame(AnimationFrame(self.spriteDict["explosion_center_1"], 4))
        explosion_center_animation.add_frame(AnimationFrame(self.spriteDict["explosion_center_2"], 4))
        explosion_center_animation.add_frame(AnimationFrame(self.spriteDict["explosion_center_3"], 4))
        explosion_center_animation.add_frame(AnimationFrame(self.spriteDict["explosion_center_4"], 4))
        animation_library["explosion_center"] = explosion_center_animation

        return animation_library

class Bomber(AnimatedEntity):
    def __init__(self, neutralImage, *, deathAnimation, movement_plane=False, barrier_sprites=False):
        AnimatedEntity.__init__(self, neutralImage, deathAnimation, movement_plane=movement_plane, barrier_sprites=barrier_sprites)
    
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

class Explosion(AnimatedEntity):
    def __init__(self, neutral_image, *, deathAnimation):
        AnimatedEntity.__init__(self, neutral_image, deathAnimation)

    def place_at(self, center_coordinates):
        self.rect.center = center_coordinates

    def explode_at(self, center_point):
        self.place_at(center_point)
        self.death()

class Tile(Graphic):
    def __init__(self, surfaceName='terrain', surfaceImage=False, scale=False, imageRotation=0, *, destructable=False, flip_x=False, flip_y=False, barrier=False):
        self.destructable = destructable
        self.surface = surfaceName
        self.graphicsLive = False
        self.barrier = barrier
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
                        self.map[col].append(Tile('wall_3', self.graphicsLibrary.get('wall_3'), (self.scaleWidth,self.scaleHeight), barrier=True))
                    elif cell == self.height - 1:
                        # World Barrier - Bottom Middle
                        self.map[col].append(Tile('wall_12', self.graphicsLibrary.get('wall_12'), (self.scaleWidth,self.scaleHeight), barrier=True))
                    else:
                        # Playable Map Area
                        if (col % 2) != 0 and (cell % 2) == 0:
                            # Hard-Barrier Generation
                            self.map[col].append(Tile('solid', self.graphicsLibrary.get('solid'), (self.scaleWidth,self.scaleHeight), barrier=True))
                        elif (col,cell) in self.spawn_buffers:
                            # Preserve Potential Spawn Points
                            self.map[col].append(Tile('terrain', self.graphicsLibrary.get('terrain'), (self.scaleWidth,self.scaleHeight), barrier=False))
                        elif random.randint(0, 2) == 0:
                            # Soft-Barrier Generation
                            self.map[col].append(Tile('destructable_new', self.graphicsLibrary.get('destructable_new'), (self.scaleWidth,self.scaleHeight), destructable="True", barrier=True))
                        else:
                            # Fill Remaining Terrain
                            self.map[col].append(Tile('terrain', self.graphicsLibrary.get('terrain'), (self.scaleWidth,self.scaleHeight), barrier=False))
                else:
                    # World Barrier - Side Sections
                    if col == 0 or col == self.width - 1:
                        # Roof
                        right_most_columns = False
                        if col == self.width - 1:
                            right_most_columns = True

                        if cell == self.height - 1:
                            self.map[col].append(Tile('wall_10', self.graphicsLibrary.get('wall_10'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        elif cell == self.height - 2:
                            self.map[col].append(Tile('wall_1', self.graphicsLibrary.get('wall_1'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        elif cell == 0:
                            self.map[col].append(Tile('wall_1', self.graphicsLibrary.get('wall_1'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        else:
                            self.map[col].append(Tile('wall_5', self.graphicsLibrary.get('wall_5'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                    elif col == 1 or col == self.width - 2:
                        # Floor 
                        right_most_columns = False
                        if col == self.width - 2:
                            right_most_columns = True

                        if cell == self.height -1:
                            self.map[col].append(Tile('wall_11', self.graphicsLibrary.get('wall_11'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        elif cell == self.height - 2:
                            self.map[col].append(Tile('wall_9', self.graphicsLibrary.get('wall_9'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        elif cell == 0:
                            self.map[col].append(Tile('wall_2', self.graphicsLibrary.get('wall_2'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        elif cell == 1:
                            self.map[col].append(Tile('wall_6', self.graphicsLibrary.get('wall_6'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        else:
                            self.map[col].append(Tile('wall_7', self.graphicsLibrary.get('wall_7'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
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
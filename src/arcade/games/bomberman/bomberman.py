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
        self.explosion_duration = 4
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
                SpriteResourceReference("bomb_l_inactive", 543,185,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("bomb_l_active", 441,117,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_center_1", 475,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_center_2", 492,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_center_3", 509,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_center_4", 527,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_center_5", 475,151,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_top_tip_1", 526,100,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_top_tip_2", 526,117,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_top_tip_3", 509,117,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_top_tip_4", 492,117,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_top_tip_5", 475,117,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_bottom_tip_1", 526,168,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_bottom_tip_2", 509,168,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_bottom_tip_3", 492,168,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_bottom_tip_4", 475,168,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_bottom_tip_5", 458,117,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_left_tip_1", 475,100,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_left_tip_2", 458,100,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_left_tip_3", 441,100,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_left_tip_4", 424,100,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_left_tip_5", 407,100,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_right_tip_1", 424,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_right_tip_2", 424,151,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_right_tip_3", 424,168,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_right_tip_4", 458,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_right_tip_5", 458,151,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_vertical_shaft_1", 492,151,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_vertical_shaft_2", 509,151,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_vertical_shaft_3", 526,151,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_vertical_shaft_4", 441,168,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_vertical_shaft_5", 458,168,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_horizontal_shaft_1", 407,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_horizontal_shaft_2", 407,151,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_horizontal_shaft_3", 407,168,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_horizontal_shaft_4", 441,134,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("explosion_horizontal_shaft_5", 441,151,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("aftermath", 507,202,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("terrain", 475,15,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("destructable_new", 458,32,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("destructable_death_1", 407,185,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("destructable_death_2", 424,185,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("destructable_death_3", 441,185,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("destructable_death_4", 458,185,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("destructable_death_5", 475,185,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("destructable_death_6", 492,185,16,16, TILE_TRANSPARENT_YELLOW),
                SpriteResourceReference("destructable_death_7", 475,15,16,16, TILE_TRANSPARENT_YELLOW),
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

        # --- Animations Setup --- #
        self.animations_library = self.generate_animations_library()

        # --- Map Setup --- #
        self.map = Map(self.spriteDict, self.animations_library, self.config.totalTilesX, self.config.totalTilesY, self.config.tileWidth, self.config.tileHeight)

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
                if self.p1.is_alive():
                    b = Bomb(self.spriteDict.get("bomb_l_inactive"), deathAnimation=self.animations_library.get("bomb_ticking").copy())
                    b.drop_bomb(self.p1,self.map)
                    b.set_scale((self.config.tileWidth,self.config.tileHeight))
                    self.bombSprites.add(b)
                    return True
                else:
                    return False
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
        self.deadlySprites.draw(self.display)
        self.bombSprites.draw(self.display)
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
                # --- Generate Explosion Area --- #
                explosion = Explosion(self.spriteDict.get("bomb_l_inactive"), deathAnimation=self.animations_library.get("explosion_center").copy())
                explosion.explode_at(bomb.rect.center)
                explosion.set_scale((self.config.tileWidth,self.config.tileHeight))
                self.deadlySprites.add(explosion)
                cluster = ExplosionCluster((self.config.tileWidth,self.config.tileHeight), bomb.rect.center,self.map, self.spriteDict.get("aftermath"), self.animations_library.get("explosion_center").copy(), self.animations_library.get("explosion_top_tip").copy(),
                    self.animations_library.get("explosion_bottom_tip").copy(), self.animations_library.get("explosion_right_tip").copy(), self.animations_library.get("explosion_left_tip").copy(), 
                    self.animations_library.get("explosion_horizontal_shaft").copy(), self.animations_library.get("explosion_vertical_shaft").copy())
                self.deadlySprites.add(cluster.get_explosions())

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

        # --- Map Animations --- #
        for col in self.map.map:
            for tile in col:
                if tile.needsUpdate():
                    needsUpdate = True

        # --- End Game Handling --- #
        living_players = 0
        for bomber in self.bomberSprites:
            if bomber.is_alive():
                living_players += 1
        if living_players == 1:
            self.game_over()

        return needsUpdate

    def game_over(self):
        # TODO - Implement game over handling with Dylan's UI tools
        # print("Game Over")
        return

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
        explosion_center_animation.add_frame(AnimationFrame(self.spriteDict["explosion_center_1"], self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.spriteDict["explosion_center_2"], self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.spriteDict["explosion_center_3"], self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.spriteDict["explosion_center_4"], self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.spriteDict["explosion_center_5"], self.config.explosion_duration))
        animation_library["explosion_center"] = explosion_center_animation

        explosion_top_tip_animation = Animation()
        explosion_top_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_top_tip_1"], self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_top_tip_2"], self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_top_tip_3"], self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_top_tip_4"], self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_top_tip_5"], self.config.explosion_duration))
        animation_library["explosion_top_tip"] = explosion_top_tip_animation

        explosion_bottom_tip_animation = Animation()
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_bottom_tip_1"], self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_bottom_tip_2"], self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_bottom_tip_3"], self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_bottom_tip_4"], self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_bottom_tip_5"], self.config.explosion_duration))
        animation_library["explosion_bottom_tip"] = explosion_bottom_tip_animation
        
        explosion_right_tip_animation = Animation()
        explosion_right_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_right_tip_1"], self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_right_tip_2"], self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_right_tip_3"], self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_right_tip_4"], self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_right_tip_5"], self.config.explosion_duration))
        animation_library["explosion_right_tip"] = explosion_right_tip_animation

        explosion_left_tip_animation = Animation()
        explosion_left_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_left_tip_1"], self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_left_tip_2"], self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_left_tip_3"], self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_left_tip_4"], self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.spriteDict["explosion_left_tip_5"], self.config.explosion_duration))
        animation_library["explosion_left_tip"] = explosion_left_tip_animation

        explosion_vertical_shaft_animation = Animation()
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.spriteDict["explosion_vertical_shaft_1"], self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.spriteDict["explosion_vertical_shaft_2"], self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.spriteDict["explosion_vertical_shaft_3"], self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.spriteDict["explosion_vertical_shaft_4"], self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.spriteDict["explosion_vertical_shaft_5"], self.config.explosion_duration))
        animation_library["explosion_vertical_shaft"] = explosion_vertical_shaft_animation

        explosion_horizontal_shaft_animation = Animation()
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.spriteDict["explosion_horizontal_shaft_1"], self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.spriteDict["explosion_horizontal_shaft_2"], self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.spriteDict["explosion_horizontal_shaft_3"], self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.spriteDict["explosion_horizontal_shaft_4"], self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.spriteDict["explosion_horizontal_shaft_5"], self.config.explosion_duration))
        animation_library["explosion_horizontal_shaft"] = explosion_horizontal_shaft_animation

        destructable_death = Animation()
        destructable_death.add_frame(AnimationFrame(self.spriteDict["destructable_death_1"], self.config.explosion_duration))
        destructable_death.add_frame(AnimationFrame(self.spriteDict["destructable_death_2"], self.config.explosion_duration))
        destructable_death.add_frame(AnimationFrame(self.spriteDict["destructable_death_3"], self.config.explosion_duration))
        destructable_death.add_frame(AnimationFrame(self.spriteDict["destructable_death_4"], self.config.explosion_duration))
        destructable_death.add_frame(AnimationFrame(self.spriteDict["destructable_death_5"], self.config.explosion_duration))
        destructable_death.add_frame(AnimationFrame(self.spriteDict["destructable_death_6"], self.config.explosion_duration))
        destructable_death.add_frame(AnimationFrame(self.spriteDict["destructable_death_7"], self.config.explosion_duration))
        animation_library["destructable_death"] = destructable_death

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

    def drop_bomb(self, player, world_map):
        if player.is_alive():
            # Will drop bomb in the center of whatever tile the player is centered over
            tile_center = world_map.coordinates_to_tile(player.rect.center).rect.center
            self.place_at(tile_center)
            self.death()

class ExplosionCluster():
    def __init__(self, tile_scale, epicenter_coordinates, world_map, neutral_image, center_animation, top_tip_animation, bottom_tip_animation, right_tip_animation, left_tip_animation, horizontal_shaft_animation, vertical_shaft_animation):
        central_tile = world_map.coordinates_to_tile(epicenter_coordinates)
        exploding_tiles, destructable_tiles = world_map.get_around(central_tile, distance=4) # TODO Differentiate which explosion texture to use and place on map
        self.explosions = list()
        for tile in exploding_tiles:
            if tile[1] == 'up':
                if tile[2]: 
                    self.explosions.append(Explosion(neutral_image, deathAnimation=top_tip_animation.copy(), explosion_coordinates=tile[0].rect.center, scale=tile_scale))
                else:
                    self.explosions.append(Explosion(neutral_image, deathAnimation=vertical_shaft_animation.copy(), explosion_coordinates=tile[0].rect.center, scale=tile_scale))
            elif tile[1] == 'down':
                if tile[2]: 
                    self.explosions.append(Explosion(neutral_image, deathAnimation=bottom_tip_animation.copy(), explosion_coordinates=tile[0].rect.center, scale=tile_scale))
                else:
                    self.explosions.append(Explosion(neutral_image, deathAnimation=vertical_shaft_animation.copy(), explosion_coordinates=tile[0].rect.center, scale=tile_scale))
            elif tile[1] == 'left':
                if tile[2]: 
                    self.explosions.append(Explosion(neutral_image, deathAnimation=left_tip_animation.copy(), explosion_coordinates=tile[0].rect.center, scale=tile_scale))
                else:
                    self.explosions.append(Explosion(neutral_image, deathAnimation=horizontal_shaft_animation.copy(), explosion_coordinates=tile[0].rect.center, scale=tile_scale))
            elif tile[1] == 'right':
                if tile[2]: 
                    self.explosions.append(Explosion(neutral_image, deathAnimation=right_tip_animation.copy(), explosion_coordinates=tile[0].rect.center, scale=tile_scale))
                else:
                    self.explosions.append(Explosion(neutral_image, deathAnimation=horizontal_shaft_animation.copy(), explosion_coordinates=tile[0].rect.center, scale=tile_scale))
        for destructable in destructable_tiles:
            destructable.death()

    def get_explosions(self):
        return self.explosions

class Explosion(AnimatedEntity):
    def __init__(self, neutral_image, *, deathAnimation, explosion_coordinates=False, scale=False):
        AnimatedEntity.__init__(self, neutral_image, deathAnimation)
        if explosion_coordinates:
            self.explode_at(explosion_coordinates)
            if scale:
                self.set_scale(scale)

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
        self.state = 'static'
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

    def update(self):
        pass
        
    def needsUpdate(self):
        return False

class AnimatedTile(AnimatedEntity): # TODO make a special destructable tile class for the trees
    def __init__(self, surfaceName='destructable_new', surfaceImage=False, scale=False, *, destructable=False, barrier=False, death_animation=False):
        AnimatedEntity.__init__(self, surfaceImage, death_animation)
        self.destructable = destructable
        self.surface = surfaceName
        self.graphicsLive = False
        self.barrier = barrier
        if scale:
            self.set_scale(scale)
        self.graphicsLive=True

class Map():
    def __init__(self, spriteDict, animation_dict, numTilesX, numTilesY, tileWidth, tileHeight):
        self.width = numTilesX
        self.height = numTilesY
        self.graphicsLibrary = spriteDict
        self.animations_library = animation_dict
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
                            self.map[col].append(AnimatedTile('destructable_new', self.graphicsLibrary.get('destructable_new'), (self.scaleWidth,self.scaleHeight), destructable="True", barrier=True, death_animation=self.animations_library.get('destructable_death').copy()))
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
                self.map[col][cell].place_at(topleft=(self.scaleWidth * col, self.scaleHeight * cell))

    def update(self, display):
        for colNum, col in enumerate(self.map):
            for rowNum, tile in enumerate(col):
                if tile.graphicsLive:
                    tile.update()
                    display.blit(tile.image, tile.rect.topleft)
                    if tile.state == 'dead':
                        self.map[colNum][rowNum] = Tile('terrain', self.graphicsLibrary.get('terrain'), (self.scaleWidth,self.scaleHeight), barrier=False)
                        self.map[colNum][rowNum].place_at(topleft=(self.scaleWidth * colNum, self.scaleHeight * rowNum))

    def coordinates_to_tile(self, coordinates):
        for colNum, col in enumerate(self.map):
            for rowNum, tile in enumerate(col):
                if tile.rect.collidepoint(coordinates):
                    return tile

    def __get_index_pair__(self, current_tile):
        for colNum, col in enumerate(self.map):
            for rowNum, tile in enumerate(col):
                if tile == current_tile:
                    return (colNum, rowNum)

    def get_around(self, current_tile, *, index_pair=False, distance=1):
        # Context Tiles = (tile:Tile, direction:string, is_tip:bool)
        tiles = list()
        destructables = list()
        if not index_pair:
            index_pair = self.__get_index_pair__(current_tile)
        if distance > 0:
            for i in range(1, distance):
                up = self.get_above(current_tile, index_pair, i)
                if not up or up.barrier:
                    if up.destructable:
                        destructables.append(up)
                    if i > 1:
                        previous_tile = tiles.pop()
                        tiles.append((previous_tile[0],previous_tile[1],True))
                    break
                else:
                    if i == distance - 1:
                        tiles.append((up, 'up', True))
                    else:
                        tiles.append((up, 'up', False))
            for i in range(1, distance):
                down = self.get_below(current_tile, index_pair, i)
                if not down or down.barrier:
                    if down.destructable:
                        destructables.append(down)
                    if i > 1:
                        previous_tile = tiles.pop()
                        tiles.append((previous_tile[0],previous_tile[1],True))
                    break
                else:
                    if i == distance - 1:
                        tiles.append((down, 'down', True))
                    else:
                        tiles.append((down, 'down', False))
            for i in range(1, distance):
                right = self.get_right(current_tile, index_pair, i)
                if not right or right.barrier:
                    if right.destructable:
                        destructables.append(right)
                    if i > 1:
                        previous_tile = tiles.pop()
                        tiles.append((previous_tile[0],previous_tile[1],True))
                    break
                else:
                    if i == distance - 1:
                        tiles.append((right, 'right', True))
                    else:
                        tiles.append((right, 'right', False))
            for i in range(1, distance):
                left = self.get_left(current_tile, index_pair, i)
                if not left or left.barrier:
                    if left.destructable:
                        destructables.append(left)
                    if i > 1:
                        previous_tile = tiles.pop()
                        tiles.append((previous_tile[0],previous_tile[1],True))
                    break
                else:
                    if i == distance - 1:
                        tiles.append((left, 'left', True))
                    else:
                        tiles.append((left, 'left', False))
        return tiles, destructables

    def get_above(self, current_tile, index_pair=False, distance=1):
        col = 0
        row = 0
        if index_pair:
            col, row = index_pair
        else: 
            col, row = self.__get_index_pair__(current_tile)

        if row - distance > -1:
            return self.map[col][row-distance]
        else:
            return False

    def get_below(self, current_tile, index_pair=False, distance=1):
        col = 0
        row = 0
        if index_pair:
            col, row = index_pair
        else: 
            col, row = self.__get_index_pair__(current_tile)
            
        if row + distance < self.height:
            return self.map[col][row+distance]
        else:
            return False

    def get_left(self, current_tile, index_pair=False, distance=1):
        col = 0
        row = 0
        if index_pair:
            col, row = index_pair
        else: 
            col, row = self.__get_index_pair__(current_tile)
            
        if col - distance > -1:
            return self.map[col-distance][row]
        else:
            return False

    def get_right(self, current_tile, index_pair=False, distance=1):
        col = 0
        row = 0
        if index_pair:
            col, row = index_pair
        else: 
            col, row = self.__get_index_pair__(current_tile)
            
        if col + distance < self.width:
            return self.map[col+distance][row]
        else:
            return False
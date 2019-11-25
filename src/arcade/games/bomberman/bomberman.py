#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
from arcade import plethoraAPI
from arcade.common.spritesheet import SpriteResourceReference, SpriteSheet, SpriteBook
from arcade.common.graphicsManager import AnimatedEntity, Graphic, Animation, AnimationFrame
from arcade.games.bomberman.bomberman_animations import BombermanAnimationLibrary
from arcade.games.bomberman.bomberman_config import GameConfig

class Bomberman(plethoraAPI.Game):
    def __init__(self) -> None:
        # --- PyGame Core Inits --- #
        self.config = GameConfig()
        super().__init__(size=(self.config.gameWidth, self.config.gameHeight), fps=20)
        self.bomber_sprites = pygame.sprite.Group()
        self.bomb_sprites = pygame.sprite.Group()
        self.deadly_sprites = pygame.sprite.Group()

        # --- Sprite Load-In --- #
        self.static_image_library = SpriteBook(self.config.sprites, self.config.assetPath).get_all_sprites()

        # --- Animations Setup --- #
        animations = BombermanAnimationLibrary(self.static_image_library, self.config)
        self.animations_library = animations.get_library()

        # --- Map Setup --- #
        self.map = Map(self.static_image_library, self.animations_library, self.config.totalTilesX, self.config.totalTilesY, self.config.tileWidth, self.config.tileHeight)

        # --- Player Initialization --- #
        self.p1 = Bomber(self.static_image_library["bomber_w_neutral"], deathAnimation=self.animations_library.get("bomber_w_death").copy(), movement_plane=self.map.map, barrier_sprites=self.bomb_sprites, world_map=self.map, config=self.config)
        self.bomber_sprites.add(self.p1)

        self.p2 = Bomber(self.static_image_library["bomber_b_neutral"], deathAnimation=self.animations_library.get("bomber_b_death").copy(), movement_plane=self.map.map, barrier_sprites=self.bomb_sprites, world_map=self.map, config=self.config)
        self.bomber_sprites.add(self.p2)

    def onevent(self, event: pygame.event) -> bool:
        if event.type == pygame.QUIT:
            self.onexit()
        if event.type == pygame.KEYDOWN:
            # Player 1 Controls
            if event.key == pygame.K_LEFT:
                return self.p1.toggle_movement('left')
            elif event.key == pygame.K_RIGHT:
                return self.p1.toggle_movement('right')
            elif event.key == pygame.K_UP:
                return self.p1.toggle_movement('up')
            elif event.key == pygame.K_DOWN:
                return self.p1.toggle_movement('down')
            elif event.key == pygame.K_SPACE:
                # Drop bomb
                if self.p1.is_alive():
                    b = Bomb(self.static_image_library.get("bomb_l_inactive"), deathAnimation=self.animations_library.get("bomb_ticking").copy())
                    b.drop_bomb(self.p1,self.map)
                    b.set_scale((self.config.tileWidth,self.config.tileHeight))
                    self.bomb_sprites.add(b)
                    return True
                else:
                    return False
            # Player 2 Controls
            elif event.key == pygame.K_a:
                return self.p2.toggle_movement('left')
            elif event.key == pygame.K_d:
                return self.p2.toggle_movement('right')
            elif event.key == pygame.K_w:
                return self.p2.toggle_movement('up')
            elif event.key == pygame.K_s:
                return self.p2.toggle_movement('down')
            elif event.key == pygame.K_q:
                # Drop bomb
                if self.p2.is_alive():
                    b = Bomb(self.static_image_library.get("bomb_l_inactive"), deathAnimation=self.animations_library.get("bomb_ticking").copy())
                    b.drop_bomb(self.p2,self.map)
                    b.set_scale((self.config.tileWidth,self.config.tileHeight))
                    self.bomb_sprites.add(b)
                    return True
                else:
                    return False
        if event.type == pygame.KEYUP:
            # Player 1 Controls
            if event.key == pygame.K_LEFT:
                return self.p1.toggle_movement('none')
            elif event.key == pygame.K_RIGHT:
                return self.p1.toggle_movement('none')
            elif event.key == pygame.K_UP:
                return self.p1.toggle_movement('none')
            elif event.key == pygame.K_DOWN:
                return self.p1.toggle_movement('none')
            # Player 2 Controls 
            elif event.key == pygame.K_a:
                return self.p2.toggle_movement('none')
            elif event.key == pygame.K_d:
                return self.p2.toggle_movement('none')
            elif event.key == pygame.K_w:
                return self.p2.toggle_movement('none')
            elif event.key == pygame.K_s:
                return self.p2.toggle_movement('none')
        return False

    def onrender(self) -> bool:
        # --- PyGame Draw Handling --- #
        needs_update = False
        pygame.display.flip()
        self.map.update(self.display)
        self.deadly_sprites.draw(self.display)
        self.bomb_sprites.draw(self.display)
        self.bomber_sprites.draw(self.display)

        # --- Player Updates --- #
        for player in self.bomber_sprites:
            if player.needs_update():
                needs_update = True
                self.bomber_sprites.update()

        # --- Bomb Updates --- #
        for bomb in self.bomb_sprites:
            if bomb.needs_update():
                needs_update = True
                bomb.update()
            elif not bomb.is_alive():
                # --- Generate Explosion Area --- #
                explosion = Explosion(self.static_image_library.get("bomb_l_inactive"), deathAnimation=self.animations_library.get("explosion_center").copy())
                explosion.explode_at(bomb.rect.center)
                explosion.set_scale((self.config.tileWidth,self.config.tileHeight))
                self.deadly_sprites.add(explosion)
                cluster = ExplosionCluster((self.config.tileWidth,self.config.tileHeight), bomb.rect.center,self.map, self.static_image_library.get("aftermath"), self.animations_library.get("explosion_center").copy(), self.animations_library.get("explosion_top_tip").copy(),
                    self.animations_library.get("explosion_bottom_tip").copy(), self.animations_library.get("explosion_right_tip").copy(), self.animations_library.get("explosion_left_tip").copy(), 
                    self.animations_library.get("explosion_horizontal_shaft").copy(), self.animations_library.get("explosion_vertical_shaft").copy())
                self.deadly_sprites.add(cluster.get_explosions())

                self.bomb_sprites.remove(bomb)
                needs_update = True

        # --- Explosion Updates --- #
        for deadly_sprite in self.deadly_sprites:
            if deadly_sprite.needs_update():
                needs_update=True
                deadly_sprite.update()
            elif not deadly_sprite.is_alive():
                self.deadly_sprites.remove(deadly_sprite)
                needs_update=True
        
        # --- Death Handling --- #
        kill_list = pygame.sprite.groupcollide(self.deadly_sprites, self.bomber_sprites, False, False)
        if len(kill_list) > 0:
            for bomber_collision_group in kill_list.values():
                for bomber in bomber_collision_group:
                    bomber.death()

        # --- Map Animations --- #
        for col in self.map.map:
            for tile in col:
                if tile.needs_update():
                    needs_update = True

        # --- End Game Handling --- #
        living_players = 0
        for bomber in self.bomber_sprites:
            if bomber.is_alive():
                living_players += 1
        if living_players == 1:
            self.game_over()

        return needs_update

    def game_over(self):
        # TODO - Implement game over handling with Dylan's UI tools
        # print("Game Over")
        return

class Bomber(AnimatedEntity):
    def __init__(self, neutralImage, *, deathAnimation, movement_plane=False, barrier_sprites=False, world_map=False, config=False):
        AnimatedEntity.__init__(self, neutralImage, deathAnimation, movement_plane=movement_plane, barrier_sprites=barrier_sprites)

        if world_map and config:
            p1_spawn_tile_xy = world_map.assign_spawn_point()
            p1_spawn_tile = world_map.map[p1_spawn_tile_xy[0]][p1_spawn_tile_xy[1]]
            self.set_scale((int(config.tileWidth*.75),int(config.tileHeight*.75)))
            self.place_at(center=p1_spawn_tile.rect.center)

class Bomb(AnimatedEntity):
    def __init__(self, neutral_image, *, deathAnimation):
        AnimatedEntity.__init__(self, neutral_image, deathAnimation)

    def drop_bomb(self, player, world_map):
        if player.is_alive():
            # Will drop bomb in the center of whatever tile the player is centered over
            tile_center = world_map.coordinates_to_tile(player.rect.center).rect.center
            self.place_at(center=tile_center)
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

    def explode_at(self, center_point):
        self.place_at(center=center_point)
        self.death()

class StaticTile(Graphic):
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
            self.set_surface(surfaceName, surfaceImage)
            if scale:
                self.set_scale(scale)

    def __set_image__(self, image):
        if not self.graphicsLive:
            Graphic.__init__(self, image)
            self.graphicsLive = True

    def set_surface(self, surface, image):
        self.surface = surface
        self.__set_image__(image)

    def update(self):
        pass
        
    def needs_update(self):
        return False

class DynamicTile(AnimatedEntity):
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
    def __init__(self, static_image_library, animation_dict, numTilesX, numTilesY, tileWidth, tileHeight):
        self.width = numTilesX
        self.height = numTilesY
        self.graphicsLibrary = static_image_library
        self.animations_library = animation_dict
        self.scaleWidth = tileWidth
        self.scaleHeight = tileHeight

        self.active_spawns = 0
        self.spawn_points = [(2,1),(self.width-3, self.height-2),(self.width-3,1),(2, self.height-2)]
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
                        self.map[col].append(StaticTile('wall_3', self.graphicsLibrary.get('wall_3'), (self.scaleWidth,self.scaleHeight), barrier=True))
                    elif cell == self.height - 1:
                        # World Barrier - Bottom Middle
                        self.map[col].append(StaticTile('wall_12', self.graphicsLibrary.get('wall_12'), (self.scaleWidth,self.scaleHeight), barrier=True))
                    else:
                        # Playable Map Area
                        if (col % 2) != 0 and (cell % 2) == 0:
                            # Hard-Barrier Generation
                            self.map[col].append(StaticTile('solid', self.graphicsLibrary.get('solid'), (self.scaleWidth,self.scaleHeight), barrier=True))
                        elif (col,cell) in self.spawn_buffers:
                            # Preserve Potential Spawn Points
                            self.map[col].append(StaticTile('terrain', self.graphicsLibrary.get('terrain'), (self.scaleWidth,self.scaleHeight), barrier=False))
                        elif random.randint(0, 2) == 0:
                            # Soft-Barrier Generation
                            self.map[col].append(DynamicTile('destructable_new', self.graphicsLibrary.get('destructable_new'), (self.scaleWidth,self.scaleHeight), destructable="True", barrier=True, death_animation=self.animations_library.get('destructable_death').copy()))
                        else:
                            # Fill Remaining Terrain
                            self.map[col].append(StaticTile('terrain', self.graphicsLibrary.get('terrain'), (self.scaleWidth,self.scaleHeight), barrier=False))
                else:
                    # World Barrier - Side Sections
                    if col == 0 or col == self.width - 1:
                        # Roof
                        right_most_columns = False
                        if col == self.width - 1:
                            right_most_columns = True

                        if cell == self.height - 1:
                            self.map[col].append(StaticTile('wall_10', self.graphicsLibrary.get('wall_10'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        elif cell == self.height - 2:
                            self.map[col].append(StaticTile('wall_1', self.graphicsLibrary.get('wall_1'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        elif cell == 0:
                            self.map[col].append(StaticTile('wall_1', self.graphicsLibrary.get('wall_1'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        else:
                            self.map[col].append(StaticTile('wall_5', self.graphicsLibrary.get('wall_5'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                    elif col == 1 or col == self.width - 2:
                        # Floor 
                        right_most_columns = False
                        if col == self.width - 2:
                            right_most_columns = True

                        if cell == self.height -1:
                            self.map[col].append(StaticTile('wall_11', self.graphicsLibrary.get('wall_11'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        elif cell == self.height - 2:
                            self.map[col].append(StaticTile('wall_9', self.graphicsLibrary.get('wall_9'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        elif cell == 0:
                            self.map[col].append(StaticTile('wall_2', self.graphicsLibrary.get('wall_2'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        elif cell == 1:
                            self.map[col].append(StaticTile('wall_6', self.graphicsLibrary.get('wall_6'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                        else:
                            self.map[col].append(StaticTile('wall_7', self.graphicsLibrary.get('wall_7'), (self.scaleWidth,self.scaleHeight), flip_x=right_most_columns, barrier=True))
                self.map[col][cell].place_at(topleft=(self.scaleWidth * col, self.scaleHeight * cell))

    def update(self, display):
        for colNum, col in enumerate(self.map):
            for rowNum, tile in enumerate(col):
                if tile.graphicsLive:
                    tile.update()
                    display.blit(tile.image, tile.rect.topleft)
                    if tile.state == 'dead':
                        self.map[colNum][rowNum] = StaticTile('terrain', self.graphicsLibrary.get('terrain'), (self.scaleWidth,self.scaleHeight), barrier=False)
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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from arcade import plethoraAPI
from arcade.common.spritesheet import SpriteResourceReference, SpriteSheet, SpriteBook
from arcade.common.graphics_manager import AnimatedEntity, Graphic, Animation, AnimationFrame
from arcade.common.resource_library import ResourceLibrary
from arcade.games.bomberman.bomberman_map import StaticTile, DynamicTile, Map
from arcade.games.bomberman.bomberman_animations import BombermanAnimationLibrary
from arcade.games.bomberman.bomberman_config import GameConfig
from typing import List, Tuple
import pathlib

class Bomberman(plethoraAPI.Game):
    """The Bomberman Game!
    """
    def __init__(self) -> None:
        """Initialize a new game of Bomberman.

        :return: Newly instantiated game.
        :rtype: Bomberman
        """
        # --- PyGame Core Inits --- #
        self.config = GameConfig()
        super().__init__(size=(self.config.gameWidth, self.config.gameHeight), fps=20)
        self.bomber_sprites = pygame.sprite.Group()
        self.bomb_sprites = pygame.sprite.Group()
        self.deadly_sprites = pygame.sprite.Group()

        # --- Sprite Load-In --- #
        self.static_image_library = ResourceLibrary(SpriteBook(self.config.sprites, self.config.assetPath).get_all_sprites())

        # --- Animations Setup --- #
        animations = BombermanAnimationLibrary(self.static_image_library, self.config)
        self.animations_library = ResourceLibrary(animations.get_dict())

        # --- Map Setup --- #
        self.map = Map(self.static_image_library, self.animations_library, self.config.totalTilesX, self.config.totalTilesY, self.config.tileWidth, self.config.tileHeight)

        # --- Player Initialization --- #
        self.p1 = Bomber(self.static_image_library.get("bomber_w_neutral"), death_animation=self.animations_library.get("bomber_w_death"), movement_plane=self.map.map, barrier_sprites=self.bomb_sprites, world_map=self.map, config=self.config)
        self.bomber_sprites.add(self.p1)

        self.p2 = Bomber(self.static_image_library.get("bomber_b_neutral"), death_animation=self.animations_library.get("bomber_b_death"), movement_plane=self.map.map, barrier_sprites=self.bomb_sprites, world_map=self.map, config=self.config)
        self.bomber_sprites.add(self.p2)

    def onevent(self, event: pygame.event) -> bool:
        """Event handler, inherited from the PlethoraPy API.

        :param pygame.event event: The event to handle.
        :return: True if a render is needed, False otherwise.
        :rtype: bool
        """
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
                    b = Bomb(self.static_image_library.get("bomb_l_inactive"), death_animation=self.animations_library.get("bomb_ticking"))
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
                    b = Bomb(self.static_image_library.get("bomb_l_inactive"), death_animation=self.animations_library.get("bomb_ticking"))
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
        """Render handler, inherited from the PlethoraPy API.

        :return: True if another render is needed, False otherwise.
        :rtype: bool
        """
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
                player.update()

        # --- Bomb Updates --- #
        for bomb in self.bomb_sprites:
            if bomb.needs_update():
                needs_update = True
                bomb.update()
            elif not bomb.is_alive():
                # --- Generate Explosion Area --- #
                explosion = Explosion(self.static_image_library.get("bomb_l_inactive"), death_animation=self.animations_library.get("explosion_center"))
                explosion.explode_at(bomb.rect.center)
                explosion.set_scale((self.config.tileWidth,self.config.tileHeight))
                self.deadly_sprites.add(explosion)
                cluster = ExplosionCluster((self.config.tileWidth,self.config.tileHeight), bomb.rect.center,self.map, self.static_image_library.get("aftermath"), self.animations_library.get("explosion_center"), self.animations_library.get("explosion_top_tip"),
                    self.animations_library.get("explosion_bottom_tip"), self.animations_library.get("explosion_right_tip"), self.animations_library.get("explosion_left_tip"), 
                    self.animations_library.get("explosion_horizontal_shaft"), self.animations_library.get("explosion_vertical_shaft"))
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
        """Handle a Game Over condition.

        :rtype: None
        """
        # TODO - Implement game over handling with Dylan's UI tools, temp solution: reset game
        # print("Game Over")
        # here = pathlib.Path(plethoraAPI.__file__).parent
        # plethoraAPI.UIButton(0,0,"Exit Game",self.exit_game, pygame.font.Font(os.path.join(here,"fonts","exo","Exo-Regular.ttf"), 30))
        self.reset()
    
    def reset(self):
        """Reset the game for a new round.

        :rtype: None
        """
        self.bomber_sprites = pygame.sprite.Group()
        self.bomb_sprites = pygame.sprite.Group()
        self.deadly_sprites = pygame.sprite.Group()

        self.map = Map(self.static_image_library, self.animations_library, self.config.totalTilesX, self.config.totalTilesY, self.config.tileWidth, self.config.tileHeight)

        self.p1 = Bomber(self.static_image_library.get("bomber_w_neutral"), death_animation=self.animations_library.get("bomber_w_death"), movement_plane=self.map.map, barrier_sprites=self.bomb_sprites, world_map=self.map, config=self.config)
        self.bomber_sprites.add(self.p1)
        self.p2 = Bomber(self.static_image_library.get("bomber_b_neutral"), death_animation=self.animations_library.get("bomber_b_death"), movement_plane=self.map.map, barrier_sprites=self.bomb_sprites, world_map=self.map, config=self.config)
        self.bomber_sprites.add(self.p2)

    def exit_game(self):
        """Exit the game, return to Plethora.

        :rtype: None
        """
        self.onexit()

class Bomber(AnimatedEntity):
    """Bomber class (player). Main characters of the game.
    """
    def __init__(self, neutral_image:pygame.image, *, death_animation:Animation, movement_plane=False, barrier_sprites:pygame.sprite.Group=False, world_map:Map=False, config:GameConfig=False):
        """Create a new bomber.

        :param pygame.image neutral_image: Neutral image used when an animation is not active.
        :param Animation death_animation: Death animation of the bomber.
        :param bool movement_plane: Movement/map plane of tiles that the Bomber can move on.
        :param pygame.sprite.Group barrier_sprites: Other sprites that the Bomber can not move through/accross.
        :param Map world_map: World map that the Bomber exists on.
        :param GameConfig config: Game configuration object.
        :return: Newly instantiated Bomber.
        :rtype: Bomber.
        """
        AnimatedEntity.__init__(self, neutral_image, death_animation, movement_plane=movement_plane, barrier_sprites=barrier_sprites)

        if world_map and config:
            p1_spawn_tile_xy = world_map.assign_spawn_point()
            p1_spawn_tile = world_map.map[p1_spawn_tile_xy[0]][p1_spawn_tile_xy[1]]
            self.set_scale((int(config.tileWidth*.75),int(config.tileHeight*.75)))
            self.place_at(center=p1_spawn_tile.rect.center)

class Bomb(AnimatedEntity):
    """Bomb class which will begin ticking down when dropped, then 'die'. Externally, an Explosion Cluster should be
    generated around the bomb.
    """
    def __init__(self, neutral_image:pygame.image, *, death_animation:Animation):
        """Create a new Bomb.

        :param pygame.image neutral_image: Neutral image used when an animation is not active.
        :param Animation death_animation: Death animation of the bomber.
        :return: Newly instantiated Bomb.
        :rtype: Bomb
        """
        AnimatedEntity.__init__(self, neutral_image, death_animation)

    def drop_bomb(self, player:Bomber, world_map:Map) -> None:
        """Drop the bomb from a Bomber, on the map.

        :param Bomber player: Player which the bomb will drop from.
        :param Map world_map: Map to drop the bomb upon.
        :rtype: None
        """
        if player.is_alive():
            # Will drop bomb in the center of whatever tile the player is centered over
            tile_center = world_map.coordinates_to_tile(player.rect.center).rect.center
            self.place_at(center=tile_center)
            self.death()

class ExplosionCluster():
    """
    A cluster of explosions at a certain distance, centered around one tile, interrupted by barriers.
    """
    def __init__(self, tile_scale:Tuple[int,int], epicenter_coordinates:Tuple[int,int], world_map:Map, neutral_image:pygame.image, center_animation:Animation, 
        top_tip_animation:Animation, bottom_tip_animation:Animation, right_tip_animation:Animation, left_tip_animation:Animation, 
        horizontal_shaft_animation:Animation, vertical_shaft_animation:Animation):
        """Generate a new explosion cluster.

        :param tile_scale:Tuple[int,int] scale: ...
        :param tile_scale:Tuple[int,int] epicenter_coordinates: ...
        :param Map world_map:
        :param pygame.image neutral_image: 
        :param Animation center_animation: Animation for the center of the explosion.
        :param Animation top_tip_animation: Animation for the top tip of the explosion.
        :param Animation bottom_tip_animation: Animation for the bottom tip of the explosion.
        :param Animation right_tip_animation: Animation for the right tip of the explosion.
        :param Animation left_tip_animation: Animation for the left tip of the explosion.
        :param Animation horizontal_shaft_animation: Animation for the horizontal shaft of the explosion.
        :param Animation vertical_shaft_animation: Animation for the horizontal shaft of the explosion.
        :return: Newly instantiated explosion cluster.
        :rtype: ExplosionCluster
        """
        central_tile = world_map.coordinates_to_tile(epicenter_coordinates)
        exploding_tiles, destructable_tiles = world_map.get_around(central_tile, distance=4)
        self.explosions = list()
        for tile in exploding_tiles:
            if tile[1] == 'up':
                if tile[2]: 
                    self.explosions.append(Explosion(neutral_image, death_animation=top_tip_animation, explosion_coordinates=tile[0].rect.center, scale=tile_scale))
                else:
                    self.explosions.append(Explosion(neutral_image, death_animation=vertical_shaft_animation, explosion_coordinates=tile[0].rect.center, scale=tile_scale))
            elif tile[1] == 'down':
                if tile[2]: 
                    self.explosions.append(Explosion(neutral_image, death_animation=bottom_tip_animation, explosion_coordinates=tile[0].rect.center, scale=tile_scale))
                else:
                    self.explosions.append(Explosion(neutral_image, death_animation=vertical_shaft_animation, explosion_coordinates=tile[0].rect.center, scale=tile_scale))
            elif tile[1] == 'left':
                if tile[2]: 
                    self.explosions.append(Explosion(neutral_image, death_animation=left_tip_animation, explosion_coordinates=tile[0].rect.center, scale=tile_scale))
                else:
                    self.explosions.append(Explosion(neutral_image, death_animation=horizontal_shaft_animation, explosion_coordinates=tile[0].rect.center, scale=tile_scale))
            elif tile[1] == 'right':
                if tile[2]: 
                    self.explosions.append(Explosion(neutral_image, death_animation=right_tip_animation, explosion_coordinates=tile[0].rect.center, scale=tile_scale))
                else:
                    self.explosions.append(Explosion(neutral_image, death_animation=horizontal_shaft_animation, explosion_coordinates=tile[0].rect.center, scale=tile_scale))
        for destructable in destructable_tiles:
            destructable.death()

    def get_explosions(self) -> List[object]:
        """Accessor function for the explosions list.

        :return: Explosions generated by the cluster.
        :rtype: List[Explosion]
        """
        return self.explosions

class Explosion(AnimatedEntity):
    def __init__(self, neutral_image:pygame.image, *, death_animation:Animation, explosion_coordinates:Tuple[int,int]=False, scale:Tuple[int,int]=False):
        """Desc

        :param pygame.image neutral_image: Neutral image to be used when the explosion is not animating.
        :param Animation death_animation: Tick-down animation
        :param Tuple[int,int] explosion_coordinates: Coordinates of the explosion's center.
        :param Tuple[int,int] scale: Scale of the explosion.
        :return: Newly instantiated Explosion.
        :rtype: Type
        """
        AnimatedEntity.__init__(self, neutral_image, death_animation)
        if explosion_coordinates:
            self.explode_at(explosion_coordinates)
            if scale:
                self.set_scale(scale)

    def explode_at(self, center_point:Tuple[int,int]) -> None:
        """Generate explosion at a point.

        :param Tuple[int,int] center_point: (x,y) Coordinate pair to explode at.
        :rtype: None
        """
        self.place_at(center=center_point)
        self.death()

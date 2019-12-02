#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from arcade.common.graphics_manager import Graphic, AnimatedEntity, Animation
from arcade.common.resource_library import ResourceLibrary
import random
import pygame
from typing import Union, List, Tuple

class StaticTile(Graphic):
    """Static map tile.

    """
    def __init__(self, surface_name:str='terrain', surface_image:pygame.image=False, scale:Tuple[int,int]=False, image_rotation:int=0, *, flip_x:bool=False, flip_y:bool=False, barrier:bool=False):
        """Initialize a new static map tile.

        :param str surface_name: Name of the surface of the tile (corresponds to a resource key).
        :param pygame.image surface_image: 
        :param tuple scale: Horizontal by vertical scale of the tile.
        :param int image_rotation: Degree to rotate the tile image by.
        :param bool flip_x: Flip the tile on the x-axis.
        :param bool flip_y: Flip the tile on the y-axis.
        :param bool barrier: Is the tile a barrier for moving entities?
        :return: Newly instantiated Static Tile.
        :rtype: StaticTile
        """
        self.destructable = False
        self.surface = surface_name
        self.graphicsLive = False
        self.barrier = barrier
        self.state = 'static'
        if surface_name and surface_image:
            if image_rotation > 0:
                surface_image = pygame.transform.rotate(surface_image,image_rotation)
            if flip_y or flip_x:
                surface_image = pygame.transform.flip(surface_image,flip_x,flip_y)
            self.set_surface(surface_name, surface_image)
            if scale:
                self.set_scale(scale)

    def __set_image__(self, image:pygame.image) -> None:
        """Set the image of the tile.

        :param pygame.image image: The image to apply to the tile.
        :rtype: None
        """
        if not self.graphicsLive:
            Graphic.__init__(self, image)
            self.graphicsLive = True

    def set_surface(self, surface:str, image:pygame.image) -> None:
        """Set the surface of the tile. 

        :param str surface: The surface name. Typically the key/label of a resource.
        :param pygame.image image: The image to use as the tile's image.
        :rtype: None
        """
        self.surface = surface
        self.__set_image__(image)

    def update(self) -> None:
        """Placeholder for tile updates. Static tiles do not change, so no update is needed.

        :rtype: None
        """
        pass
        
    def needs_update(self) -> bool:
        """Placeholder for tile updates. Static tiles do not change, so no update is needed.

        :rtype: None
        """
        return False

class DynamicTile(AnimatedEntity):
    """Dynamic map tile. Typically used for animated or destructable tiles.

    """
    def __init__(self, surface_name:str='destructable_new', surface_image:pygame.image=False, scale:Tuple[int,int]=False, *, destructable:bool=False, barrier:bool=False, death_animation:Animation=False):
        """Initialize a new dynamic tile.

        :param str surface_name: Name of the surface of the tile (corresponds to a resource key).
        :param pygame.image surface_image: 
        :param tuple scale: Horizontal by vertical scale of the tile.
        :param bool destructable: Is the tile destructable?
        :param bool barrier: Is the tile a barrier for moving entities?
        :param Animation death_animation: Death animation for the dynamic tile.
        :return: Newly instantiated Dynamic Tile.
        :rtype: DynamicTile
        """
        AnimatedEntity.__init__(self, surface_image, death_animation)
        self.destructable = destructable
        self.surface = surface_name
        self.graphicsLive = False
        self.barrier = barrier
        if scale:
            self.set_scale(scale)
        self.graphicsLive=True

class Map():
    """World map, grid of tiles and other properties.

    """
    def __init__(self, static_image_library:ResourceLibrary, animation_library:ResourceLibrary, num_tiles_x:int, num_tiles_y:int, tile_width:int, tile_height:int):
        """Create a new Map for the game.

        :param ResourceLibrary static_image_library: Resource library of static images.
        :param ResourceLibrary animation_library: Resource library of animations.
        :param int num_tiles_x: Number of tiles in the grid map, horizontally (columns).
        :param int num_tiles_y: Number of tiles in the grid map, vertically (rows).
        :param int tile_width: Width of each tile.
        :param int tile_height: Height of each tile.
        :return: Newly instantiated map.
        :rtype: Map
        """
        self.width = num_tiles_x
        self.height = num_tiles_y
        self.graphicsLibrary = static_image_library
        self.animations_library = animation_library
        self.scaleWidth = tile_width
        self.scaleHeight = tile_height

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

    def assign_spawn_point(self) -> StaticTile:
        """Claim a spawn area for a player.

        :return: The tile for the player to use as a spawn point.
        :rtype: StaticTile
        """
        spawn_tile = self.spawn_points[self.active_spawns]
        self.active_spawns += 1
        return spawn_tile

    def reset(self) -> None:
        """Reset the Map, generating new terrain.

        :rtype: None
        """
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
                            self.map[col].append(DynamicTile('destructable_new', self.graphicsLibrary.get('destructable_new'), (self.scaleWidth,self.scaleHeight), destructable="True", barrier=True, death_animation=self.animations_library.get('destructable_death')))
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

    def update(self, display:pygame.display) -> None:
        """Update all tiles in the map.

        :param pygame.display display: Display to update the Map on.
        :rtype: None
        """
        for colNum, col in enumerate(self.map):
            for rowNum, tile in enumerate(col):
                if tile.graphicsLive:
                    tile.update()
                    display.blit(tile.image, tile.rect.topleft)
                    if tile.state == 'dead':
                        self.map[colNum][rowNum] = StaticTile('terrain', self.graphicsLibrary.get('terrain'), (self.scaleWidth,self.scaleHeight), barrier=False)
                        self.map[colNum][rowNum].place_at(topleft=(self.scaleWidth * colNum, self.scaleHeight * rowNum))

    def coordinates_to_tile(self, coordinates:Tuple[int,int]) -> Union[StaticTile, DynamicTile]:
        """Get a tile by coordinates.

        :param tuple coordinates: (x,y) coordinate pair of the tile.
        :return: The tile which collides with the coordinate point given.
        :rtype: Union[StaticTile, DynamicTile]
        """
        for colNum, col in enumerate(self.map):
            for rowNum, tile in enumerate(col):
                if tile.rect.collidepoint(coordinates):
                    return tile

    def __get_index_pair__(self, target_tile:Union[StaticTile, DynamicTile]) -> tuple:
        """Get the internal index pair of a given tile.

        :param Union[StaticTile, DynamicTile] target_tile: The tile to search for.
        :return: Column and row numbers where the tile is stored internally.
        :rtype: tuple
        """
        for colNum, col in enumerate(self.map):
            for rowNum, tile in enumerate(col):
                if tile == target_tile:
                    return (colNum, rowNum)

    def get_around(self, current_tile:Union[StaticTile, DynamicTile], *, index_pair:Tuple[int,int]=False, distance=1) -> Tuple[List[Union[StaticTile, DynamicTile]], List[DynamicTile]]:
        """Get all tiles above, below, left, and right, or a tile on the map, up to a certain distance. Return any
        destructable tiles which are in this path. The path stops if a barrier is reached in that direction.

        :param Union[StaticTile, DynamicTile] current_tile: current_tile: Center tile to search around.
        :param Tuple[int,int] index_pair: Column and row (if known) of the center tile.
        :param int index_pair: Distance around the center tile to search.
        :return: List of tiles in reach and within distance, and a list of destructable tiles effected.
        :rtype: List[Union[StaticTile, DynamicTile]]
        """
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

    def get_above(self, current_tile:Union[StaticTile, DynamicTile], index_pair:Tuple[int,int]=False, distance=1) -> Union[bool, StaticTile, DynamicTile]:
        """Get the tile above the current tile by a certain distance, if it can be reached and exists.

        :param Union[StaticTile, DynamicTile] current_tile: The current/center tile to search from.
        :param Tuple[int,int] index_pair: Column and row of the current tile, if known.
        :param int distance: Distance from current tile to search (ignoring obstacles and paths).
        :return: Returns the given tile, or False if it can't be found.
        :rtype: Union[bool, StaticTile, DynamicTile]
        """
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

    def get_below(self, current_tile, index_pair=False, distance=1) -> Union[bool, StaticTile, DynamicTile]:
        """Get the tile below the current tile by a certain distance, if it can be reached and exists.

        :param Union[StaticTile, DynamicTile] current_tile: The current/center tile to search from.
        :param Tuple[int,int] index_pair: Column and row of the current tile, if known.
        :param int distance: Distance from current tile to search (ignoring obstacles and paths).
        :return: Returns the given tile, or False if it can't be found.
        :rtype: Union[bool, StaticTile, DynamicTile]
        """
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

    def get_left(self, current_tile, index_pair=False, distance=1) -> Union[bool, StaticTile, DynamicTile]:
        """Get the tile left of the current tile by a certain distance, if it can be reached and exists.

        :param Union[StaticTile, DynamicTile] current_tile: The current/center tile to search from.
        :param Tuple[int,int] index_pair: Column and row of the current tile, if known.
        :param int distance: Distance from current tile to search (ignoring obstacles and paths).
        :return: Returns the given tile, or False if it can't be found.
        :rtype: Union[bool, StaticTile, DynamicTile]
        """
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

    def get_right(self, current_tile, index_pair=False, distance=1) -> Union[bool, StaticTile, DynamicTile]:
        """Get the tile right of the current tile by a certain distance, if it can be reached and exists.

        :param Union[StaticTile, DynamicTile] current_tile: The current/center tile to search from.
        :param Tuple[int,int] index_pair: Column and row of the current tile, if known.
        :param int distance: Distance from current tile to search (ignoring obstacles and paths).
        :return: Returns the given tile, or False if it can't be found.
        :rtype: Union[bool, StaticTile, DynamicTile]
        """
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
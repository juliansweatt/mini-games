#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from arcade.common.spritesheet import SpriteResourceReference, SpriteSheet, SpriteBook
import os.path

# Color Definitions
AVATAR_TRANSPARENT_GREEN = (64, 144, 56)
TILE_TRANSPARENT_YELLOW = (255, 255, 128)

class GameConfig():
    """Bomberman Game Configuration. Used to easily set and change back-end presets and globals
    throughout the game.

    """
    def __init__(self):
        # Configurations marked 'Editable' can be changed and the game will adapt to fit the new preference
        self.gameHeight = 800 # Editable
        self.gameWidth = self.gameHeight
        self.gamePath = os.path.join('src', 'arcade', 'games','bomberman')
        self.assetPath = os.path.join(self.gamePath, 'assets')
        self.playableTilesX = 19 # Editable
        self.playableTilesY = 17 # Editable
        self.totalTilesX = self.playableTilesX + 2
        self.totalTilesY = self.playableTilesY + 4
        self.tileWidth = int(self.gameWidth/self.totalTilesX)
        self.tileHeight = int(self.gameWidth/self.totalTilesY)
        self.explosion_duration = 4 # Editable
        self.sprites = {
            "avatars.png": (
                SpriteResourceReference("bomber_w_neutral",71,45,17,26,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_b_neutral",226,45,17,26,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying1",29,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying2",48,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying3",65,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying4",82,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying5",99,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_w_dying6",117,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_b_dying1",183,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_b_dying2",202,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_b_dying3",219,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_b_dying4",236,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_b_dying5",253,76,17,24,AVATAR_TRANSPARENT_GREEN),
                SpriteResourceReference("bomber_b_dying6",271,76,17,24,AVATAR_TRANSPARENT_GREEN),
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
                # Numbering is Left -> Right, Top -> Bottom on the Sprite Sheet
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
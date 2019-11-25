#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from arcade.common.graphics_manager import Animation, AnimationFrame

class BombermanAnimationLibrary():
    def __init__(self, static_images, config):
        self.__animation_dict__ = dict()
        self.static_image_library = static_images
        self.config = config
        self.__generate_animations_library__()

    def get_dict(self):
        return self.__animation_dict__

    def __generate_animations_library__(self):
        black_player_death_animation = Animation()
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_w_dying1")))
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_w_dying2")))
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_w_dying3")))
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_w_dying4")))
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_w_dying5")))
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_w_dying6")))
        self.__animation_dict__["bomber_w_death"] = black_player_death_animation

        black_player_death_animation = Animation()
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_b_dying1")))
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_b_dying2")))
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_b_dying3")))
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_b_dying4")))
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_b_dying5")))
        black_player_death_animation.add_frame(AnimationFrame(self.static_image_library.get("bomber_b_dying6")))
        self.__animation_dict__["bomber_b_death"] = black_player_death_animation

        bomb_ticking_animation = Animation()
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library.get("bomb_l_inactive"), 10))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library.get("bomb_l_active"), 10))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library.get("bomb_l_inactive"), 5))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library.get("bomb_l_active"), 5))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library.get("bomb_l_inactive"), 3))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library.get("bomb_l_active"), 3))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library.get("bomb_l_inactive"), 1))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library.get("bomb_l_active"), 1))
        self.__animation_dict__["bomb_ticking"] = bomb_ticking_animation

        explosion_center_animation = Animation()
        explosion_center_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_center_1"), self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_center_2"), self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_center_3"), self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_center_4"), self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_center_5"), self.config.explosion_duration))
        self.__animation_dict__["explosion_center"] = explosion_center_animation

        explosion_top_tip_animation = Animation()
        explosion_top_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_top_tip_1"), self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_top_tip_2"), self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_top_tip_3"), self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_top_tip_4"), self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_top_tip_5"), self.config.explosion_duration))
        self.__animation_dict__["explosion_top_tip"] = explosion_top_tip_animation

        explosion_bottom_tip_animation = Animation()
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_bottom_tip_1"), self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_bottom_tip_2"), self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_bottom_tip_3"), self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_bottom_tip_4"), self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_bottom_tip_5"), self.config.explosion_duration))
        self.__animation_dict__["explosion_bottom_tip"] = explosion_bottom_tip_animation
        
        explosion_right_tip_animation = Animation()
        explosion_right_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_right_tip_1"), self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_right_tip_2"), self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_right_tip_3"), self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_right_tip_4"), self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_right_tip_5"), self.config.explosion_duration))
        self.__animation_dict__["explosion_right_tip"] = explosion_right_tip_animation

        explosion_left_tip_animation = Animation()
        explosion_left_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_left_tip_1"), self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_left_tip_2"), self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_left_tip_3"), self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_left_tip_4"), self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_left_tip_5"), self.config.explosion_duration))
        self.__animation_dict__["explosion_left_tip"] = explosion_left_tip_animation

        explosion_vertical_shaft_animation = Animation()
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_vertical_shaft_1"), self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_vertical_shaft_2"), self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_vertical_shaft_3"), self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_vertical_shaft_4"), self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_vertical_shaft_5"), self.config.explosion_duration))
        self.__animation_dict__["explosion_vertical_shaft"] = explosion_vertical_shaft_animation

        explosion_horizontal_shaft_animation = Animation()
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_horizontal_shaft_1"), self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_horizontal_shaft_2"), self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_horizontal_shaft_3"), self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_horizontal_shaft_4"), self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.static_image_library.get("explosion_horizontal_shaft_5"), self.config.explosion_duration))
        self.__animation_dict__["explosion_horizontal_shaft"] = explosion_horizontal_shaft_animation

        destructable_death_animation = Animation()
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library.get("destructable_death_1"), self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library.get("destructable_death_2"), self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library.get("destructable_death_3"), self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library.get("destructable_death_4"), self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library.get("destructable_death_5"), self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library.get("destructable_death_6"), self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library.get("destructable_death_7"), self.config.explosion_duration))
        self.__animation_dict__["destructable_death"] = destructable_death_animation
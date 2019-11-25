#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from arcade.common.graphicsManager import Animation, AnimationFrame

class BombermanAnimationLibrary():
    def __init__(self, static_images, config):
        self.animation_library = dict()
        self.static_image_library = static_images
        self.config = config
        self.__generate_animations_library__()

    def get_library(self):
        return self.animation_library

    def __generate_animations_library__(self):
        self.animation_library = dict()
        death_animation = Animation()
        death_animation.add_frame(AnimationFrame(self.static_image_library["bomber_w_dying1"]))
        death_animation.add_frame(AnimationFrame(self.static_image_library["bomber_w_dying2"]))
        death_animation.add_frame(AnimationFrame(self.static_image_library["bomber_w_dying3"]))
        death_animation.add_frame(AnimationFrame(self.static_image_library["bomber_w_dying4"]))
        death_animation.add_frame(AnimationFrame(self.static_image_library["bomber_w_dying5"]))
        death_animation.add_frame(AnimationFrame(self.static_image_library["bomber_w_dying6"]))
        self.animation_library["bomber_w_death"] = death_animation

        bomb_ticking_animation = Animation()
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library["bomb_l_inactive"], 10))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library["bomb_l_active"], 10))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library["bomb_l_inactive"], 5))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library["bomb_l_active"], 5))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library["bomb_l_inactive"], 3))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library["bomb_l_active"], 3))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library["bomb_l_inactive"], 1))
        bomb_ticking_animation.add_frame(AnimationFrame(self.static_image_library["bomb_l_active"], 1))
        self.animation_library["bomb_ticking"] = bomb_ticking_animation

        explosion_center_animation = Animation()
        explosion_center_animation.add_frame(AnimationFrame(self.static_image_library["explosion_center_1"], self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.static_image_library["explosion_center_2"], self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.static_image_library["explosion_center_3"], self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.static_image_library["explosion_center_4"], self.config.explosion_duration))
        explosion_center_animation.add_frame(AnimationFrame(self.static_image_library["explosion_center_5"], self.config.explosion_duration))
        self.animation_library["explosion_center"] = explosion_center_animation

        explosion_top_tip_animation = Animation()
        explosion_top_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_top_tip_1"], self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_top_tip_2"], self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_top_tip_3"], self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_top_tip_4"], self.config.explosion_duration))
        explosion_top_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_top_tip_5"], self.config.explosion_duration))
        self.animation_library["explosion_top_tip"] = explosion_top_tip_animation

        explosion_bottom_tip_animation = Animation()
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_bottom_tip_1"], self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_bottom_tip_2"], self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_bottom_tip_3"], self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_bottom_tip_4"], self.config.explosion_duration))
        explosion_bottom_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_bottom_tip_5"], self.config.explosion_duration))
        self.animation_library["explosion_bottom_tip"] = explosion_bottom_tip_animation
        
        explosion_right_tip_animation = Animation()
        explosion_right_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_right_tip_1"], self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_right_tip_2"], self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_right_tip_3"], self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_right_tip_4"], self.config.explosion_duration))
        explosion_right_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_right_tip_5"], self.config.explosion_duration))
        self.animation_library["explosion_right_tip"] = explosion_right_tip_animation

        explosion_left_tip_animation = Animation()
        explosion_left_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_left_tip_1"], self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_left_tip_2"], self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_left_tip_3"], self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_left_tip_4"], self.config.explosion_duration))
        explosion_left_tip_animation.add_frame(AnimationFrame(self.static_image_library["explosion_left_tip_5"], self.config.explosion_duration))
        self.animation_library["explosion_left_tip"] = explosion_left_tip_animation

        explosion_vertical_shaft_animation = Animation()
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.static_image_library["explosion_vertical_shaft_1"], self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.static_image_library["explosion_vertical_shaft_2"], self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.static_image_library["explosion_vertical_shaft_3"], self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.static_image_library["explosion_vertical_shaft_4"], self.config.explosion_duration))
        explosion_vertical_shaft_animation.add_frame(AnimationFrame(self.static_image_library["explosion_vertical_shaft_5"], self.config.explosion_duration))
        self.animation_library["explosion_vertical_shaft"] = explosion_vertical_shaft_animation

        explosion_horizontal_shaft_animation = Animation()
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.static_image_library["explosion_horizontal_shaft_1"], self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.static_image_library["explosion_horizontal_shaft_2"], self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.static_image_library["explosion_horizontal_shaft_3"], self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.static_image_library["explosion_horizontal_shaft_4"], self.config.explosion_duration))
        explosion_horizontal_shaft_animation.add_frame(AnimationFrame(self.static_image_library["explosion_horizontal_shaft_5"], self.config.explosion_duration))
        self.animation_library["explosion_horizontal_shaft"] = explosion_horizontal_shaft_animation

        destructable_death_animation = Animation()
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library["destructable_death_1"], self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library["destructable_death_2"], self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library["destructable_death_3"], self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library["destructable_death_4"], self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library["destructable_death_5"], self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library["destructable_death_6"], self.config.explosion_duration))
        destructable_death_animation.add_frame(AnimationFrame(self.static_image_library["destructable_death_7"], self.config.explosion_duration))
        self.animation_library["destructable_death"] = destructable_death_animation
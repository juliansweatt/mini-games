#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame

class Graphic():
    def __init__(self, staticImage):
        self.image = staticImage
        self.rect = self.image.get_rect()

    def set_scale(self, scale):
        center = self.rect.center
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def placeAt(self, topleft=False, center=False):
        if center:
            self.image.get_rect().center = center
            self.rect.center = center
        elif topleft:
            self.image.get_rect().topleft = topleft
            self.rect.topleft = topleft

class AnimationFrame():
    def __init__(self, image, duration_frames=1):
        self.image = image
        self.duration = duration_frames

    def set_scale(self, scale):
        self.image = pygame.transform.scale(self.image, scale)

    def copy(self):
        return AnimationFrame(self.image.copy(), self.duration)

class Animation():
    def __init__(self):
        self.animation = list()
        self.__current_index__ = 0
        self.__current_frame__ = False
        self.__current_duration__ = 0
        self.__final_frame__ = False

    def add_frame(self, frame:AnimationFrame):
        if not self.__current_frame__:
            self.__current_frame__ = frame
            self.__current_duration__ = frame.duration
        self.animation.append(frame)

    def get_current_frame(self):
        if self.__current_frame__:
            return self.__current_frame__.image

    def next(self):
        if self.__current_duration__ > 0:
            # Frame Duration Decrement
            self.__current_duration__ -= 1
        else:
            self.__current_index__ += 1
            if self.__current_index__ >= len(self.animation):
                self.__current_index__ = 0
                self.__current_duration__ = self.animation[self.__current_index__].duration
                if self.__final_frame__:
                    self.__final_frame__ = False
            else:
                self.__current_frame__ = self.animation[self.__current_index__]
                self.__current_duration__ = self.animation[self.__current_index__].duration
                if self.__current_index__ == len(self.animation) -1:
                    self.__final_frame__ = True
        return self.__current_frame__.image

    def set_scale(self, scale):
        for i, frame in enumerate(self.animation):
            self.animation[i].set_scale(scale)

    def is_final_frame(self):
        if self.__final_frame__:
            return True
        else:
            return False

    def copy(self):
        animation = Animation()
        for frame in self.animation:
            animation.add_frame(frame.copy())
        return animation

class AnimatedEntity(pygame.sprite.Sprite, Graphic):
    def __init__(self, neutralImage, deathAnimation = False):
        pygame.sprite.Sprite.__init__(self)
        Graphic.__init__(self, neutralImage)
        self.neutralImage = neutralImage
        self.state = 'neutral'
        self.rect = self.image.get_rect()
        self.animations = dict()
        if deathAnimation:
            self.animations['death'] = deathAnimation
        self.animating = False
        self.movement = 'none'

    def set_scale(self, scale):
        Graphic.set_scale(self, scale)
        for key, state in self.animations.items():
            self.animations.get(key).set_scale(scale)
    
    def setState(self, state):
        self.index = 0
        if self.animations.get(state):
            self.current_animation = self.animations[state]
        else:
            self.current_animation = list()

    def death(self):
        if self.state != 'dead':
            self.setState('death')
            self.state = 'death'
            self.animating = True

    def is_alive(self):
        if self.state == 'dead':
            return False
        else:
            return True
    
    def needsUpdate(self):
        return self.animating | self.isMoving()

    def update(self):
        if self.state == 'death' and self.current_animation.is_final_frame():
            # Stop Updating
            self.animating = False
            self.state = 'dead'
        else:
            if self.state != 'neutral' and self.animating:
                self.image = self.current_animation.next()
        if self.movement != 'none':
            if self.movement == 'right':
                self.__move__(right=True)
            elif self.movement == 'left':
                self.__move__(left=True)
            elif self.movement == 'up':
                self.__move__(up=True)
            elif self.movement == 'down':
                self.__move__(down=True)
    
    def __move__(self, *, left=False, right=False, up=False, down=False):
        movement_increment = 5
        if right:
            self.rect.x += movement_increment
        elif left:
            self.rect.x -= movement_increment
        elif up:
            self.rect.y -= movement_increment
        elif down:
            self.rect.y += movement_increment
        return True # TODO: Implement move validation
    
    def toggle_movement(self, direction):
        if direction == 'right':
            self.movement = 'right'
        elif direction == 'left':
            self.movement = 'left'
        elif direction == 'up':
            self.movement = 'up'
        elif direction == 'down':
            self.movement = 'down'
        elif direction == 'none':
            self.movement = 'none'

        return self.isMoving()

    def isMoving(self):
        return self.movement != 'none'

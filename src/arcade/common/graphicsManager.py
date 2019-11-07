#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame

class Graphic():
    def __init__(self, staticImage):
        self.image = staticImage
        self.rect = self.image.get_rect()

    def setScale(self, scale):
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

class AnimatedEntity(pygame.sprite.Sprite, Graphic):
    def __init__(self, neutralImage, deathAnimation = False):
        pygame.sprite.Sprite.__init__(self)
        Graphic.__init__(self, neutralImage)
        self.neutralImage = neutralImage
        self.images = list()
        self.index = 0
        self.state = 'neutral'
        self.rect = self.image.get_rect()
        self.animations = dict()
        if deathAnimation:
            self.animations['death'] = deathAnimation
        self.animating = False

    def setScale(self, scale):
        Graphic.setScale(self, scale)
        for key, state in self.animations.items():
            for i, animationFrame in enumerate(state):
                self.animations.get(key)[i] = pygame.transform.scale(animationFrame, scale)
        if len(self.images) > 0:
            for i, image in enumerate(self.images):
                self.images[i] = pygame.transform.scale(animationFrame, scale)
    
    def setState(self, state):
        self.index = 0
        if self.animations.get(state):
            self.images = self.animations[state]
        else:
            self.images = list()

    def death(self):
        self.setState('death')
        self.state = 'death'
        self.animating = True
    
    def needsUpdate(self):
        return self.animating

    def update(self):
        if self.state == 'death' and self.index == len(self.animations['death']):
            # Stop Updating
            self.animating = False
            self.state = 'dead'
        else:
            if self.state != 'neutral' and type(self.images) == list:
                if self.index > len(self.images):
                    self.index = 0
                
                if self.index < len(self.images):
                    self.image = self.images[self.index]
                self.index += 1
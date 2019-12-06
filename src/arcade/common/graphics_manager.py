#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame

class Graphic():
    """General class for a static PyGame graphic.

    """
    def __init__(self, staticImage:object):
        """Create a Graphic.

        :param pygame.image staticImage: Static image to create a Graphic from.
        :return The newly instantiated Graphic.
        :rtype: Graphic
        """
        self.image = staticImage
        self.rect = self.image.get_rect()

    def set_scale(self, scale:tuple) -> None:
        """Set scale of the Graphic.

        :param scale: Scale to set Graphic to.
        :type scale: (int, int) Vertical by horizontal scale.
        :rtype: None
        """
        center = self.rect.center
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def place_at(self, topleft:tuple=False, center:tuple=False, right:tuple=False, left:tuple=False) -> None:
        """Place Graphic at a particular point.

        :param topleft: Set Graphic placement by topleft coordinate.
        :param center: Set Graphic placement by center coordinate.
        :type topleft: (int, int) x,y coordinates
        :type center: (int, int) x,y coordinates
        :type left: (int, int) x,y coordinates
        :type right: (int, int) x,y coordinates
        :rtype: None
        """
        if center:
            self.image.get_rect().center = center
            self.rect.center = center
        elif topleft:
            self.image.get_rect().topleft = topleft
            self.rect.topleft = topleft

class AnimationFrame():
    """A single animation frame. Should be used as part of the Animation class.

    """
    def __init__(self, image:pygame.image, duration_frames:int=1):
        """Create Animation Frame.

        :param pygame.image image: Static image of this frame.
        :param int duration_frames: Amount of frames (FPS) this image should occupy in the animation.
        :return The newly instantiated AnimationFrame.
        :rtype: AnimationFrame
        """
        self.image = image
        self.duration = duration_frames

    def set_scale(self, scale:tuple) -> None:
        """Set the scale of this Animation Frame.

        :param scale: New scale of the Animation Frame.
        :type scale: (int, int) Horizontal by vertical scale.
        :rtype: None
        """
        self.image = pygame.transform.scale(self.image, scale)

    def copy(self) -> object:
        """Deep copy Animation Frame

        :return Copy of the Animation Frame
        :rtype: AnimationFrame
        """
        return AnimationFrame(self.image.copy(), self.duration)

class Animation():
    """An animation, defined by a list of Animation Frames.

    """

    def __init__(self):
        """Create a new Animation object.

        :return Newly instantiated Animation.
        :rtype: Animation
        """
        self.animation = list()
        self.__current_index__ = 0
        self.__current_frame__ = False
        self.__current_duration__ = 0
        self.__final_frame__ = False

    def add_frame(self, frame:AnimationFrame) -> None:
        """Add an AnimationFrame to the Animation.

        :param AnimationFrame frame: New Animation Frame to add to the Animation.
        :rtype: None
        """
        if not self.__current_frame__:
            self.__current_frame__ = frame
            self.__current_duration__ = frame.duration
        self.animation.append(frame)

    def get_current_frame(self) -> pygame.image:
        """Get the current frame of the Animation.

        :return Current image of the Animation.
        :rtype: pygame.image
        """
        if self.__current_frame__:
            return self.__current_frame__.image

    def next(self) -> pygame.image:
        """Progress to the next frame of the animation.

        :return The new current image of the Animation.
        :rtype: pygame.image
        """
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

    def set_scale(self, scale) -> None:
        """Set the scale of the whole Animation (all Animation Frames currently in the Animation).

        :param scale: New scale of the Animation.
        :type scale: (int, int) Horizontal by vertical scale.
        :rtype: None
        """
        for i, frame in enumerate(self.animation):
            self.animation[i].set_scale(scale)

    def is_final_frame(self) -> bool:
        """Check if the Animation has reached the end.

        :return Returns True if on the final frame, else True.
        :rtype: bool
        """
        if self.__final_frame__:
            return True
        else:
            return False

    def copy(self) -> object:
        """Deep copy the Animation.

        :return Deep copy of the Animation (new object).
        :rtype: Animation
        """
        animation = Animation()
        for frame in self.animation:
            animation.add_frame(frame.copy())
        return animation

class AnimatedEntity(pygame.sprite.Sprite, Graphic):
    """An Animated Entity used in PyGame. An Animated Entity is a PyGame Sprite which may have several states,
    animations associated with those states, and may be destroyed or killed during the game.

    """
    def __init__(self, neutral_image:pygame.image, death_animation:Animation=False, *, movement_plane=False, barrier_sprites:pygame.sprite.Group=False):
        """Create a new Animated Entity.

        :param pygame.image image: The static image that the entity will default to if no state or animation is available.
        :param Animation death_animation: The death animation for the entity.
        :param Map movement_plane: Optional: Map object used to restrain a moveable entity.
        :param pygame.sprite.Group barrier_sprites: Sprites which this entity can not overlap/pass through.
        :return The newly instantiated Animated Entity
        :rtype: AnimatedEntity
        """
        pygame.sprite.Sprite.__init__(self)
        Graphic.__init__(self, neutral_image)
        self.neutral_image = neutral_image
        self.state = 'neutral'
        self.rect = self.image.get_rect()
        self.animations = dict()
        if death_animation:
            self.animations['death'] = death_animation
        self.animating = False
        self.movement = 'none'
        self.movement_plane = movement_plane
        self.barrier_sprites = barrier_sprites

    def place_at(self, topleft:bool=False, center:bool=False) -> None:
        """Place the Animated Entity at a particular point.

        :param topleft: Set Animated Entity placement by topleft coordinate.
        :param center: Set Animated Entity placement by center coordinate.
        :type topleft: (int, int) x,y coordinates
        :type center: (int, int) x,y coordinates
        :rtype: None
        """
        if center:
            self.rect.center = center
        elif topleft:
            self.rect.topleft = topleft

    def set_scale(self, scale:tuple) -> None:
        """Set the scale of this Animated Entity.

        :param scale: New scale of the Animated Entity.
        :type scale: (int, int) Horizontal by vertical scale.
        :rtype: None
        """
        Graphic.set_scale(self, scale)
        for key, state in self.animations.items():
            self.animations.get(key).set_scale(scale)
    
    def set_state(self, state:str) -> None:
        """Set the state of the Animated Entity.

        :param str state: New state name.
        :rtype: None
        """
        self.index = 0
        if self.animations.get(state):
            self.current_animation = self.animations[state]
        else:
            self.current_animation = list()

    def death(self) -> None:
        """Kill or destroy the Animated Entity.

        :rtype: None
        """
        if self.state != 'dead':
            self.set_state('death')
            self.state = 'death'
            self.animating = True

    def is_alive(self) -> bool:
        """Check if the Animated Entity is still alive.

        :return True if alive, False if dead.
        :rtype: bool
        """
        if self.state == 'dead':
            return False
        else:
            return True
    
    def needs_update(self) -> bool:
        """Check if the Animated Entity needs to be updated at a higher level.

        :return True if update is needed, False otherwise.
        :rtype: bool
        """
        return self.animating | self.is_moving()

    def update(self) -> None:
        """Update the Animated Entity. Used to handle animation and movement progression. 

        :rtype: None
        """
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

    def __validate_movement__(self, current_rect:pygame.Rect, candidate_rect:pygame.Rect) -> bool:
        """Check if a proposed movement is within the defined constraints of the Animated Entity.

        :param tpygame.Rectype current_rect: Current position.
        :param tpygame.Rectype candidate_rect: Proposed new location.
        :return True if valid, False if invalid.
        :rtype: bool
        """
        if not self.is_alive():
            return False
        if self.movement_plane:
            for colNum, col in enumerate(self.movement_plane):
                for rowNum, tile in enumerate(col):
                    if tile.barrier:
                        if tile.rect.colliderect(candidate_rect):
                            return False
            for barrier in self.barrier_sprites:
                if not barrier.rect.colliderect(current_rect):
                    if barrier.rect.colliderect(candidate_rect):
                        return False
            return True
        else:
            # Unrestricted Movement Plane
            return True
    
    def __move__(self, *, left:bool=False, right:bool=False, up:bool=False, down:bool=False) -> bool:
        """One single movement in a particular direction, validated.

        :param bool left: Move left.
        :param bool right: Move right.
        :param bool up: Move up.
        :param bool down: Move down.
        :return True if movement could be made, False otherwise.
        :rtype: bool
        """
        movement_increment = 5
        temp_rect = self.rect.copy()
        if right:
            temp_rect.x += movement_increment
            if self.__validate_movement__(self.rect, temp_rect):
                self.rect.x += movement_increment
                return True
        elif left:
            temp_rect.x -= movement_increment
            if self.__validate_movement__(self.rect, temp_rect):
                self.rect.x -= movement_increment
                return True
        elif up:
            temp_rect.y -= movement_increment
            if self.__validate_movement__(self.rect, temp_rect):
                self.rect.y -= movement_increment
                return True
        elif down:
            temp_rect.y += movement_increment
            if self.__validate_movement__(self.rect, temp_rect):
                self.rect.y += movement_increment
                return True
        return False # Invalid Movement
    
    def toggle_movement(self, direction:str) -> bool:
        """Toggle movement in a particular direction.

        :param str direction: Toggle movement in a particular direction, or stop movement.
        :return desc
        :rtype: type
        """
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

        return self.is_moving()

    def is_moving(self) -> bool:
        """Check if the entity is actively moving (or attempting to move)

        :return True if moving, False otherwise
        :rtype: bool
        """
        return self.movement != 'none'

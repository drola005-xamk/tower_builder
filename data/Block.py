import pygame
from pygame import mixer

BLOCK_ART = ["resources/images/block_perfect.png", "resources/images/block_green.png", "resources/images/block_yellow.png", "resources/images/block_red.png"]

class Block(pygame.sprite.Sprite):
    """Class for the blocks you build on top of each other"""
    def __init__(self, pos, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(BLOCK_ART[1])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.__x_speed = speed
        self.__y_speed = 10
        self.__falling = False
        self.__moving_horizontal = True
        self.__bad_alignment = False

    #Move block on x-axis
    def __x_movement(self):
        if self.__moving_horizontal:
            self.rect.x += self.__x_speed

            #Change block direction depending on position
            if self.rect.x < 0:
                self.rect.x = 0
                self.__x_speed = abs(self.__x_speed)
            if self.rect.x > 480-self.image.get_width():
                self.rect.x = 480-self.image.get_width()
                self.__x_speed = -self.__x_speed
    
    #Move block on y_axis. Stop movement when block at bottom of the screen.
    def __y_movement(self):
        if self.__falling:
            if self.rect.y < 640-50:
                self.rect.y += self.__y_speed
            else:
                self.__falling = False

    #Block update method
    def update(self):
        self.__x_movement()
        self.__y_movement()

    #Stop moving on x-axis and start falling down on y-axis
    def drop(self):
        self.__moving_horizontal = False
        self.__falling = True

    #Depending on block-to-block alignment, change image and play sound effect.
    def change_block_art(self, alignment: str):
        if alignment == "PERFECT":
            self.image = pygame.image.load(BLOCK_ART[0])
            self.perfect_collision_sound()
        if alignment == "GOOD":
            self.image = pygame.image.load(BLOCK_ART[1])
            self.collision_sound()
        if alignment == "FAIR":
            self.image = pygame.image.load(BLOCK_ART[2])
            self.collision_sound()
        if alignment == "BAD":
            self.image = pygame.image.load(BLOCK_ART[3])
            self.collision_sound()
            self.__bad_alignment = True

    #Check if block is colliding with another block. If colliding, stop block on that position.
    def is_colliding(self, other: 'Block'):
        if other != None:
            if pygame.sprite.collide_rect(self, other):
                self.__falling = False
                #Move block up y_speed amount, so blocks are not overlapping
                self.rect.y -= self.__y_speed
                return True
            else:
                return False
    
    #Play sound effect
    def collision_sound(self):
        sound = mixer.Sound("resources/sounds/vgmenuhighlight.wav")
        sound.play()
    
    #Play sound effect
    def perfect_collision_sound(self):
        sound = mixer.Sound("resources/sounds/vgmenuselect.wav")
        sound.play()

    #Return moving_horizontal bool
    @property
    def moving_horizontal(self):
        return self.__moving_horizontal

    #Return falling bool
    @property
    def falling(self):
        return self.__falling

    #Return bad_alignment bool
    @property
    def bad_alignment(self):
        return self.__bad_alignment

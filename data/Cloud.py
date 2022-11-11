import pygame
from random import randint

CLOUD_ART = ["resources/images/Clouds.png", "resources/images/clouds2.png", "resources/images/clouds3.png", "resources/images/clouds4.png"]

class Cloud(pygame.sprite.Sprite):
    """Class of cloud object"""
    def __init__(self, pos, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(CLOUD_ART[randint(0,3)])
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.__x_speed = speed
    
    #Update method. If cloud is past screen left edge, remove it from all sprite.Group()
    def update(self):
        self.rect.x -= self.__x_speed
        if self.rect.x < -200:
            self.kill()

#Generator function outside of the class, that creates a generator with x amount of clouds having x speed.
def cloud_generator(cloud_amount: int, max_speed: int):
    while cloud_amount > 0:
            yield Cloud((480 + randint(0, 500), randint(0, 320)), randint(1, max_speed))
            cloud_amount -= 1
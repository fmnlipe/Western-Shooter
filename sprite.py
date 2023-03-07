import pygame as pg
from pygame.math import Vector2 as vector

class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 3)

class Bala (pg.sprite.Sprite):
    def __init__(self, pos, direction, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = pos)

        self.pos = vector(self.rect.center)
        self.direction = direction
        self.speed = 400
    
    def update(self, deltatime):
        self.pos += self.direction * self.speed * deltatime
        self.rect.center = (round(self.pos.x), round(self.pos.y))
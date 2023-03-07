import pygame as pg
from pygame.math import Vector2 as vector
from os import walk
from math import sin

class Entidade(pg.sprite.Sprite):
    def __init__(self, pos, groups, path, colisao_sprites):
        super().__init__(groups)

        self.importar_imagem(path)
        self.frame_index = 0
        self.status = 'down_idle'


        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        #float based movement
        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200

        self.attacking = False
        self.health = 9
        self.is_vulnerable = True
        self.hit_timer = None

        #colisão
        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height/2)
        self.colisao_sprites = colisao_sprites
        self.mask = pg.mask.from_surface(self.image)

        #sound
        self.hit_sound = pg.mixer.Sound('sound/hit.mp3')
        self.hit_sound.set_volume(0.5)

        self.shoot_sound = pg.mixer.Sound('sound/bullet.wav')
        self.shoot_sound.set_volume(0.2)

    def damage(self):  
        if self.is_vulnerable:
            self.health -= 1
            self.is_vulnerable = False
            self.hit_timer = pg.time.get_ticks()
            self.hit_sound.play()

    def vulnerabilidade(self):
        if not self.is_vulnerable:
            current_time = pg.time.get_ticks()
            if current_time - self.hit_timer > 400:
                self.is_vulnerable = True

    def importar_imagem(self, path):
        self.animations = {}

        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pg.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

    def movimento(self, deltatime):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        #horizontal
        self.pos.x += self.direction.x *self.speed * deltatime
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.colisao("horizontal")

        #vertical
        self.pos.y += self.direction.y *self.speed * deltatime
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.colisao("vertical")
    
    def blink(self):
        if not self.is_vulnerable:
            if self.func_de_onda():
                mask = pg.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0,0,0))
                self.image = white_surf

    def func_de_onda(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False
    
    def colisao(self, direction):
        for sprite in self.colisao_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def morte(self):
        if self.health <= 0:
            self.kill()

import pygame as pg
from pygame.math import Vector2 as vector
from entidade import *

class Monster:
    def get_player_distance_direction(self):
        pos_inimigo = vector(self.rect.center)
        pos_jogador = vector(self.jogador.rect.center)
        distance = (pos_jogador - pos_inimigo).magnitude()

        if distance != 0:
            direction = (pos_jogador - pos_inimigo).normalize()
        else:
            direction = vector()
        
        return (distance, direction)
    
    def face_player(self):
        distance, direction = self.get_player_distance_direction()
        
        if distance < self.perceber:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0: #jogador na esquerda
                    self.status =  'left_idle'
                elif direction.x > 0: #jogador na direita
                    self.status = 'right_idle'
            else:
                if direction.y < 0: #jogador em cima
                    self.status = 'up_idle'
                elif direction.y > 0: #jogador embaixo
                    self.status = 'down_idle'            

    def walk_to_player(self):
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance < self.mover:
            self.direction = direction
            self.status = self.status.split('_')[0]
        else:
              self.direction = vector()  


class Caixão(Entidade, Monster):
    def __init__(self, pos, groups, path, colisao_sprites, jogador):
        super().__init__(pos, groups, path, colisao_sprites)
        
        self.speed = 120
        
        self.jogador = jogador
        self.perceber = 550
        self.mover = 400
        self.attack_radius = 50
        self.health = 5

    def atacar(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0
        
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def animar(self, deltatime):
        current_animation = self.animations[self.status]

        if int(self.frame_index) == 4 and self.attacking:
            if self.get_player_distance_direction()[0] < self.attack_radius:
                self.jogador.damage()

        self.frame_index += 7 * deltatime
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pg.mask.from_surface(self.image)

    def update(self, deltatime):
        
        self.face_player()
        self.walk_to_player()
        self.atacar()
        self.movimento(deltatime)
        
        self.animar(deltatime)
        self.colisao('horizontal')
        self.blink()

        self.morte()
        self.vulnerabilidade()

    

class Cacto(Entidade, Monster):
    def __init__(self, pos, groups, path, colisao_sprites, jogador, criar_balas):
        super().__init__(pos, groups, path, colisao_sprites)


        self.speed = 90
        
        self.jogador = jogador
        self.perceber = 600
        self.mover = 500
        self.attack_radius = 350
        self.speed = 90

        self.criar_balas = criar_balas
        self.tiro = False

        self.health = 3

    def atacar(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0
            self.tiro = False
                
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'     
        
    def animar(self, deltatime):
        current_animation = self.animations[self.status]

        if int(self.frame_index) == 6 and self.attacking and not self.tiro:
            direction = self.get_player_distance_direction()[1]
            pos = self.rect.center + direction * 150
            self.criar_balas(pos, direction)
            self.tiro = True
            self.shoot_sound.play()

        self.frame_index += 7 * deltatime
        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pg.mask.from_surface(self.image)
    

    def update(self, deltatime):
        self.face_player()
        self.walk_to_player()
        self.atacar()
        
        self.movimento(deltatime)
        self.animar(deltatime)
        self.colisao('horizontal')

        self.blink()
        self.morte()
        self.vulnerabilidade()
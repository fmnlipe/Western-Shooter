import pygame as pg, sys
from pygame.math import Vector2 as vector
from entidade import *

class Jogador(Entidade):
    def __init__(self, pos, groups, path, colisao_sprites, criar_bala):
        super().__init__(pos, groups, path, colisao_sprites)
        
        
        #ataque
        self.attacking = False
        self.criar_bala = criar_bala
        self.tiro = False



    def status_entity(self):
        # parado
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # ataque
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def comandos(self):
        key = pg.key.get_pressed()

        if not self.attacking:
            #horizontal
            if key[pg.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif key[pg.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            #vertical
            if key[pg.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif key[pg.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            #ataque
            if key[pg.K_x]:
                self.attacking = True
                self.direction = vector()
                self.frame_index = 0
                self.tiro = False

                match self.status.split('_')[0]:
                    case 'left': self.bala_direção = vector(-1,0)
                    case 'right': self.bala_direção = vector(1,0)
                    case 'up': self.bala_direção = vector(0,-1)
                    case 'down': self.bala_direção = vector(0,1)

    def animar(self, deltatime):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * deltatime

        if int(self.frame_index) == 2 and self.attacking == True and not self.tiro:
            bala_posição_inicial = self.rect.center + self.bala_direção * 80
            self.criar_bala(bala_posição_inicial, self.bala_direção)
            self.tiro = True
            self.shoot_sound.play()



        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pg.mask.from_surface(self.image)

    def morte(self):
        if self.health <= 0:
            pg.quit()
            sys.exit()


    def update(self, deltatime):
        self.comandos()
        self.status_entity()
        self.movimento(deltatime)
        self.animar(deltatime)
        self.blink()
        self.morte()
        self.vulnerabilidade()

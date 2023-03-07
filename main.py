import pygame as pg, sys, random
from settings import *
from pygame.math import Vector2 as vector
from jogador import Jogador
from pytmx.util_pygame import load_pygame
from sprite import *
from inimigo import *

class Allsprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pg.display.get_surface()
        self.background = pg.image.load("graphics/other/bg.png").convert()

    def customize_draw(self, jogador):

        self.offset.x = jogador.rect.centerx - comprimento_tela/2
        self.offset.y = jogador.rect.centery - altura_tela/2

        self.display_surface.blit(self.background, -self.offset)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery ):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class Setup:
    def __init__(self):
        pg.init()
        self.tela = pg.display.set_mode((comprimento_tela, altura_tela))
        pg.display.set_caption("Faroeste Doidão")
        self.clock = pg.time.Clock()
        self.bala_surf = pg.image.load("graphics/other/particle.png").convert_alpha()
    
        #grupos e sprites de colisão
        self.all_sprites = Allsprites()
        self.obstaculos = pg.sprite.Group()
        self.balas = pg.sprite.Group()
        self.monsters = pg.sprite.Group()

        self.setup()
        self.music = pg.mixer.Sound('sound/music.mp3')
        self.music.play(loops = -1)
    
    def criar_balas(self, pos, direction):
        Bala(pos, direction, self.bala_surf, [self.all_sprites, self.balas])

    def colisao_bala(self):
        if pg.sprite.spritecollide(self.player, self.balas, True, pg.sprite.collide_mask):
            self.player.damage()
        
        for obstaculos in self.obstaculos.sprites():
            pg.sprite.spritecollide(obstaculos, self.balas, True,pg.sprite.collide_mask)

        for bala in self.balas.sprites():
            sprites = pg.sprite.spritecollide(bala, self.monsters, False, pg.sprite.collide_mask)

            if sprites:
                bala.kill()
                for sprite in sprites:
                    sprite.damage()

    def setup(self):
        tmx_map = load_pygame("mapa.tmx")
        
        # tiles
        for x, y, surf in tmx_map.get_layer_by_name("Camada de Blocos 2").tiles():
            Sprite((x * 64, y * 64), surf, [self.all_sprites, self.obstaculos])
        
        # objects
        for obj in tmx_map.get_layer_by_name("objetos"):
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstaculos])
        
        for obj in tmx_map.get_layer_by_name('spawn'):
            if obj.name == "player":
                self.player = Jogador(
                    pos =(obj.x, obj.y), 
                    groups = self.all_sprites,
                    path = paths['player'], 
                    colisao_sprites =
                    self.obstaculos, 
                    criar_bala = self.criar_balas)
            
            if obj.name == "caixão":
                Caixão((obj.x, obj.y),[self.all_sprites, self.monsters],  paths['caixão'],self.obstaculos, self.player)

            if obj.name == "cacto":
                Cacto((obj.x, obj.y), [self.all_sprites, self.monsters], paths['cacto'], self.obstaculos, self.player, self.criar_balas)

        
    
    def play(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit
            
            deltatime = self.clock.tick()/1000

            #atualizar grupos
            self.all_sprites.update(deltatime)
            self.colisao_bala()

            #desenhar
            self.tela.fill("black")
            self.all_sprites.customize_draw(self.player)
            
            pg.display.update()

if __name__ == '__main__':
    game = Setup()
    game.play()
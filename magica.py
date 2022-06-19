import pygame
from config import *
from random import randint

class MagicaJogador:
    def __init__(self, animacao_jogador):
        self.animacao_jogador = animacao_jogador
    
    def heal(self, jogador, forca, custo, groups):
        if jogador.energia >= custo:
            jogador.vida += forca
            jogador.energia -= custo
            if jogador.vida >= jogador.status['health']:
                jogador.vida = jogador.status['health']
            self.animacao_jogador.criar_particulas('aura', jogador.rect.center,groups)
            self.animacao_jogador.criar_particulas('heal', jogador.rect.center + pygame.math.Vector2(0, -60), groups)
    
    def flame(self, jogador, custo, groups):
        if jogador.energia >= custo:
            jogador.energia -= custo
            
        if jogador.estatus.split('_')[0] == 'right': direcao = pygame.math.Vector2(1, 0)
        elif jogador.estatus.split('_')[0] == 'left': direcao = pygame.math.Vector2(-1, 0)
        elif jogador.estatus.split('_')[0] == 'up': direcao = pygame.math.Vector2(0, -1) 
        else: direcao = pygame.math.Vector2(0, 1) 
        
        for i in range(1, 6):
            if direcao.x:
                offset_x = (direcao.x *i) * TILESIZE
                x = jogador.rect.centerx + offset_x + randint(- TILESIZE // 3, TILESIZE // 3)
                y = jogador.rect.centery + randint(- TILESIZE // 3, TILESIZE // 3)
                self.animacao_jogador.criar_particulas('flame', (x, y), groups)
            else:
                offset_y = (direcao.y *i) * TILESIZE
                x = jogador.rect.centerx  + randint(- TILESIZE // 3, TILESIZE // 3)
                y = jogador.rect.centery + offset_y + randint(- TILESIZE // 3, TILESIZE // 3)
                self.animacao_jogador.criar_particulas('flame', (x, y), groups)
                
import pygame
from config import*

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups,tipo_sprite,superfice = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.tipo_sprite = tipo_sprite
        self.image = superfice
        
        if tipo_sprite == 'objeto': # DESLOCAR OBJETOS MAIORES QUE 64
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)  # CRIANDO E POSICIONANDO A IMAGEM 
        self.ponto_colisao = self.rect.inflate(0, -10) # DIMINUI OS SPRITES NO PONTO DE COLISAO OBSTACULOS
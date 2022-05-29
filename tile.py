import pygame
from config import*

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.imagem = pygame.image.load('graphics/test/rock.png').convert_alpha() # CARREGANDO IMAGEM
        self.rect = self.imagem.get_rect(topleft =pos)  # CRIANDO E POSICIONANDO A IMAGEM 
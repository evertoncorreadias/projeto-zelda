import pygame
from config import*

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/rock.png').convert_alpha() # CARREGANDO IMAGEM
        self.rect = self.image.get_rect(topleft =pos)  # CRIANDO E POSICIONANDO A IMAGEM 
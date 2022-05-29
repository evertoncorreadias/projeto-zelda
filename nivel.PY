import pygame

class Nivel:
    def __init__(self):
        
        self.exibe_superfice = pygame.display.get_surface()
        
        self.sprites_visiveis = pygame.sprite.Group() # GRUPO COM SPRITES VISÍVEIS
        self.sprites_obstaculos = pygame.sprite.Group() # GRUPO DE SPRITES OBSTACULOS 
        
    def executar(self):
        # ATUALIZAR E DESENHAR O JOGO
        pass
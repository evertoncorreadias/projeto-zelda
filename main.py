import pygame, sys
from config import *


class Jogo:
    def __init__(self):

        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        self.relogio = pygame.time.Clock()
        
    
    def executar(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.relogio.tick(FPS)

if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()

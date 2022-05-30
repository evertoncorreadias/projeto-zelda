import pygame, sys
from config import *
from nivel import Nivel


class Jogo:
    def __init__(self):

        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        self.relogio = pygame.time.Clock()
        self.nivel = Nivel()
        
    
    def executar(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    

            self.janela.fill('black')
            self.relogio.tick(FPS)
            self.nivel.executar()
            pygame.display.update()

if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()

import pygame, sys
from config import *
from nivel import Nivel


class Jogo:
    def __init__(self):   

        pygame.init()
        self.janela = pygame.display.set_mode((LARGURA, ALTURA))
        self.relogio = pygame.time.Clock()
        self.nivel = Nivel()
        
        # SOM 
        som_principal = pygame.mixer.Sound('audio/main.ogg')
        som_principal.set_volume(0.5)
        som_principal.play(loops = -1 )
           
    def executar(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.nivel.alternar_menu()
                    

            self.janela.fill(WATER_COLOR)
            self.relogio.tick(FPS)
            self.nivel.executar()
            pygame.display.update()

if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()

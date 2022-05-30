import pygame
from config import*

class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha() # CARREGANDO IMAGEM
        self.rect = self.image.get_rect(topleft =pos)  # CRIANDO E POSICIONANDO A IMAGEM 
        
        self.direcao = pygame.math.Vector2()
        self.speed = 5
        
    def controle(self):
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_UP]:
            self.direcao.y = -1
        elif teclas[pygame.K_DOWN]:
            self.direcao.y = 1
        else:
            self.direcao.y = 0
            
        if teclas[pygame.K_RIGHT]:
            self.direcao.x = 1
        elif teclas[pygame.K_LEFT]:
            self.direcao.x = -1
        else:
            self.direcao.x = 0
            
    def mover(self,speed):
        if self.direcao.magnitude() != 0:             # reduzir velocidade na diagonal
            self.direcao = self.direcao.normalize()   # reduzir velocidade na diagonal
        self.rect.center += self.direcao * speed
            
    def update(self):
        self.controle()
        self.mover(self.speed)
        
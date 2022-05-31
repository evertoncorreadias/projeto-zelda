import pygame
from config import*

class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, groups,sprites_obstaculos):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha() # CARREGANDO IMAGEM
        self.rect = self.image.get_rect(topleft =pos)  # CRIANDO E POSICIONANDO A IMAGEM 
        self.ponto_colisao = self.rect.inflate(0,-26) # DIMINUI OS SPRITES NO PONTO DE COLISAO JOGADOR
        self.direcao = pygame.math.Vector2()
        self.speed = 5
        
        self.sprites_obstaculos = sprites_obstaculos
        
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
        if self.direcao.magnitude() != 0:             # REDUZIR VELOCIDAD NA DIAGONAL
            self.direcao = self.direcao.normalize()   # REDUZIR VELOCIDAD NA DIAGONAL
        
        
        self.ponto_colisao.x += self.direcao.x * speed       
        self.colisao('horizontal')                  # COLISAO HORIZONTAL
        self.ponto_colisao.y += self.direcao.y * speed
        self.colisao('vertical')                    # COLISAO VERTICAL
        self.rect.center = self.ponto_colisao.center
    def colisao(self,direcao):
        if direcao == 'horizontal':
            for sprite in self.sprites_obstaculos:
                if sprite.ponto_colisao.colliderect(self.ponto_colisao):
                    if self.direcao.x > 0: # MOVENDO PARA DIREITA
                        self.ponto_colisao.right = sprite.ponto_colisao.left  # COLISAO
                    if self.direcao.x < 0: # MOVENDO PARA ESQUERDA
                        self.ponto_colisao.left = sprite.ponto_colisao.right # COLISAO
                        
        if direcao == 'vertical':
            for sprite in self.sprites_obstaculos:
                if sprite.ponto_colisao.colliderect(self.ponto_colisao):
                    if self.direcao.y > 0: # MOVENDO PARA BAIXO
                        self.ponto_colisao.bottom = sprite.ponto_colisao.top  # COLISAO
                    if self.direcao.y < 0: # MOVENDO PARA CIMA
                        self.ponto_colisao.top = sprite.ponto_colisao.bottom # COLISAO
                    
            
    def update(self):
        self.controle()
        self.mover(self.speed)
        
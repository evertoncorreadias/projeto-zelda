import pygame

class Entidade(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.indice_frame = 0
        self.velocidade_animacao = 0.15
        self.direcao = pygame.math.Vector2()
        
    
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
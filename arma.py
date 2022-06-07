import pygame

class Arma(pygame.sprite.Sprite):
    def __init__(self,jogador,groups):
        super().__init__(groups)
        direcao = jogador.estatus.split('_')[0]
        
        # GRAFICO
        pasta_arma = f'graphics/weapons/{jogador.arma}/{direcao}.png'
        self.image = pygame.image.load(pasta_arma).convert_alpha()
         
        # POSICIONAMENTO
        if direcao == 'right':
            self.rect = self.image.get_rect(midleft = jogador.rect.midright + pygame.math.Vector2(0, 16))
        elif direcao == 'left':
            self.rect = self.image.get_rect(midright = jogador.rect.midleft + pygame.math.Vector2(0, 16))
        elif direcao == 'down':
            self.rect = self.image.get_rect(midtop = jogador.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom = jogador.rect.midtop + pygame.math.Vector2(-10, 0))
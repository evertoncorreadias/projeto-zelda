import pygame
from config import *
from jogador import Jogador
from tile import Tile
from depuracao import depuracao


class Nivel:
    def __init__(self):
        # EXIBE A SUPERFICE
        self.exibe_superfice = pygame.display.get_surface()
        # GRUPOS DE SPRITES
        self.sprites_visiveis = MovimentoCamera()# pygame.sprite.Group()/modificado com criaçao a camera # GRUPO COM SPRITES VISÍVEIS
        self.sprites_obstaculos = pygame.sprite.Group() # GRUPO DE SPRITES OBSTACULOS 
        # CONFIGURAÇÃO DE SPRITES
        self.criar_mapa()
        
        
    def criar_mapa(self):
        for indice_linha,linha in enumerate(WORLD_MAP):      # PERCORRE CADA POSIÇAO DO MAPA INDICANDO O INDICE
            for indice_col,coluna in enumerate(linha):
                x = indice_col * TILESIZE
                y = indice_linha * TILESIZE    
                if coluna == 'x':
                    Tile((x,y), [self.sprites_visiveis, self.sprites_obstaculos])  
                if coluna == 'p':
                    self.jogador = Jogador((x, y), [self. sprites_visiveis],self.sprites_obstaculos)
                
                                              
                                     
        
    def executar(self):
        # ATUALIZAR E DESENHAR O JOGO
        self.sprites_visiveis.desenho_customizado(self.jogador)  # draw(self.exibe_superfice) SUBSTITUIDO PELA FUNÇAO CRIADA
        self.sprites_visiveis.update()
        depuracao(self.jogador.direcao)
        
        
class MovimentoCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)
        self.exibe_superfice = pygame.display.get_surface()
        self.metade_largura = self.exibe_superfice.get_size()[0] //2 # METADE DA LARGURA TELA 
        self.metade_altura = self.exibe_superfice.get_size()[1] //2  # METADE DA ALTURA TELA
        self.deslocamento_tela = pygame.math.Vector2() # CRIANDO VETOR DE DESLOCAMENTO DE TELA
         
        #CRIANDO O FUNDO 'MAPA'
        self.fundo_mapa = pygame.image.load('graphics/tilemap/ground.png')
        self.mapa_rect = self.fundo_mapa.get_rect(topleft = (0,0))
        
    def desenho_customizado(self,jogador):
        # OBTER DESLOCAMENTO 
        self.deslocamento_tela.x = jogador.rect.centerx - self.metade_largura
        self.deslocamento_tela.y = jogador.rect.centery - self.metade_altura
      
        
        pos_fundo_mapa = self.mapa_rect.topleft - self.deslocamento_tela
        self.exibe_superfice.blit(self.fundo_mapa,pos_fundo_mapa)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            deslocamento_pos = sprite.rect.topleft - self.deslocamento_tela
            self.exibe_superfice.blit(sprite.image,deslocamento_pos) 

    
        
    
   
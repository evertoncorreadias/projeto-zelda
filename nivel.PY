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
        self.sprites_visiveis = pygame.sprite.Group() # GRUPO COM SPRITES VISÍVEIS
        self.sprites_obstaculos = pygame.sprite.Group() # GRUPO DE SPRITES OBSTACULOS 
        # CONFIGURAÇÃO DE SPRITES
        self.criar_mapa()
        
        
    def criar_mapa(self):
        for indice_linha,linha in enumerate(WORLD_MAP):      # PERCORRE CADA POSIÇAO DO MAPA INDICANDO O INDICE
            for indice_col,coluna in enumerate(linha):
                x = indice_col * TILESIZE
                y = indice_linha * TILESIZE    
                if coluna == 'x':
                    Tile((x,y), [self.sprites_visiveis])  
                if coluna == 'p':
                    self.jogador = Jogador((x, y), [self. sprites_visiveis])
                
                                              
                                     
        
    def executar(self):
        # ATUALIZAR E DESENHAR O JOGO
        self.sprites_visiveis.draw(self.exibe_superfice)
        self.sprites_visiveis.update()
        depuracao(self.jogador.direcao)
        
    
   
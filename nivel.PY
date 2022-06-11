import pygame
from arma import Arma
from config import *
from jogador import Jogador
from tile import Tile
from depuracao import depuracao
from suporte import *
from random import choice
from arma import Arma
from ui import UI
from inimigo import Inimigo


class Nivel:
    def __init__(self):
        # EXIBE A SUPERFICE
        self.exibe_superfice = pygame.display.get_surface()
        # GRUPOS DE SPRITES
        self.sprites_visiveis = MovimentoCamera()# pygame.sprite.Group()/modificado com criaçao a camera # GRUPO COM SPRITES VISÍVEIS
        self.sprites_obstaculos = pygame.sprite.Group() # GRUPO DE SPRITES OBSTACULOS 
        
        # SPRITE ATAQUE
        self.ataque_atual = None
        
        # CONFIGURAÇÃO DE SPRITES
        self.criar_mapa()
        
        # INTERFACE DO USUARIO
        self.ui = UI()
        
               
    def criar_mapa(self):
        
        layouts = {
            'limite': importar_csv_layout('map/map_FloorBlocks.csv'),
            'grama': importar_csv_layout('map/map_Grass.csv'),
            'objeto': importar_csv_layout('map/map_Objects.csv'),
            'entities': importar_csv_layout('map/map_Entities.csv')
        }
        
        graficos = {
            'grama' : importar_pasta('graphics/Grass'),
            'objeto' : importar_pasta('graphics/objects')
        }
        for estilo,layout in layouts.items():
            for indice_linha,linha in enumerate(layout):      # PERCORRE CADA POSIÇAO DO MAPA INDICANDO O INDICE
                for indice_col,coluna in enumerate(linha):
                    if coluna != '-1':
                        x = indice_col * TILESIZE
                        y = indice_linha * TILESIZE    
                        if estilo == 'limite':
                            Tile( (x, y), [self.sprites_obstaculos],'invisivel')
                        if estilo == 'grama':
                            imagem_grama_aleatoria = choice(graficos['grama'])
                            Tile((x, y), [self.sprites_visiveis, self.sprites_obstaculos],'grama',imagem_grama_aleatoria)
                            
                        if estilo == 'objeto':
                            superficie = graficos['objeto'][int(coluna)]
                            Tile((x, y), [self.sprites_visiveis, self.sprites_obstaculos],'objeto', superficie)
   
                        if estilo == 'entities':
                            if coluna == '394':
                                self.jogador = Jogador((x,y),
                                [self. sprites_visiveis],
                                self.sprites_obstaculos,
                                self.criar_ataque,
                                self.destruir_arma,
                                self.criar_magica)
                            else:
                                if coluna == '390': monster_name = 'bamboo'
                                elif coluna == '391':monster_name = 'spirit'
                                elif coluna == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                Inimigo(monster_name, (x, y), [self. sprites_visiveis],self.sprites_obstaculos)
    
    
    def criar_ataque(self):
        self.ataque_atual = Arma(self.jogador,[self.sprites_visiveis],self.sprites_obstaculos)
    
    def criar_magica(self,estilo,forca,custo):
        pass
    
    def destruir_arma(self): 
        if self.ataque_atual:
            self.ataque_atual.kill()
        self.ataque_atual = None
           
                                                                                                         
    def executar(self):
        # ATUALIZAR E DESENHAR O JOGO
        self.sprites_visiveis.desenho_customizado(self.jogador)  # draw(self.exibe_superfice) SUBSTITUIDO PELA FUNÇAO CRIADA
        self.sprites_visiveis.update()
        self.sprites_visiveis.inimigo_update(self.jogador)
        self.ui.mostrar(self.jogador)
        # depuracao(self.jogador.estatus)
        
            
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

       
    def inimigo_update(self,jogador):
        sprite_inimigo =[sprite for sprite in self.sprites() if hasattr(sprite, 'tipo_sprite') and  sprite.tipo_sprite == 'enemy']
        for inimigo in sprite_inimigo:
            inimigo.inimigo_update(jogador)
       
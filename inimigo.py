import pygame
from config import *
from entidade import Entidade
from suporte import *

class Inimigo(Entidade):
    def __init__(self, nome_monstro, pos, groups,sprites_obstaculos):
        super().__init__(groups)
        
        self.tipo_sprite = 'enemy'
        
        # CONFIGURAÇÃO GRAFICA
        self.importar_graficos(nome_monstro)
        self.estatus = 'idle'
        self.image = self.animacoes[self.estatus][self.indice_frame]
        
        # MOVIMENTO
        self.rect = self.image.get_rect(topleft = pos)
        self.ponto_colisao = self.rect.inflate(0, -10)
        self.sprites_obstaculos = sprites_obstaculos
        
        # STATUS
        self.monster_name = nome_monstro
        monster_info = monster_data[self.monster_name]
        self.vida =monster_info['health']
        self.exp = monster_info['exp']
        self.velocidade = monster_info['speed']
        self.dano_ataque = monster_info['damage']
        self.resistencia = monster_info['resistance']
        self.raio_ataque = monster_info['attack_radius']
        self.raio_info = monster_info['notice_radius']
        self.tipo_ataque = monster_info['attack_type']
        
        
    def importar_graficos(self,nome):
        self.animacoes = {'idle': [], 'move':[], 'attack':[]}
        arquivo_principal = f'graphics/monsters/{nome}/'
        for animacao in self.animacoes.keys():
            self.animacoes[animacao] = importar_pasta(arquivo_principal + animacao)   
    
    def pegar_distancia_direcao_jogador(self,jogador):
        inimigo_vec = pygame.math.Vector2(self.rect.center)
        jogador_vec =  pygame.math.Vector2(jogador.rect.center)
        
        distancia = (jogador_vec -inimigo_vec).magnitude()
        if distancia > 0:
           direcao = (jogador_vec -inimigo_vec).normalize()
        else:
            direcao = pygame.math.Vector2()
        
        
        
        return distancia, direcao
            
    def pegar_estatus(self,jogador):
        
        distancia = self.pegar_distancia_direcao_jogador(jogador)[0]
        
        if distancia <= self.raio_ataque:
             self.estatus = 'attack'
        elif distancia <= self.raio_info:
            self.estatus = 'move'
        else:
            self.estatus ='idle' 
            
    def acoes(self,jogador):
        if self.estatus == 'attack':
            pass
        elif self.estatus =='move':
            self.direcao = self.pegar_distancia_direcao_jogador(jogador)[1]
        else:
            self.direcao = pygame.math.Vector2()
        
    def update(self):
        self.mover(self.velocidade)
        
    def inimigo_update(self,jogador):
       self.pegar_estatus(jogador)
       self.acoes(jogador)
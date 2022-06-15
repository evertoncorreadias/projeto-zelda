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
        
        # INTERAÇÃO JOGADOR
        self.pode_atacar = True
        self.tempo_ataque = None
        self.esfriamento_ataque = 400
        
        # TEMPO DE INVENCIBILIDADE
        self.vulneravel = True
        self.tempo_de_hit = None
        self.duracao_invencibilidade =300
        
        
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
        
        if distancia <= self.raio_ataque and self.pode_atacar:
            if self.estatus != 'attack':
                self.indice_frame = 0
            self.estatus = 'attack'
        elif distancia <= self.raio_info:
            self.estatus = 'move'
        else:
            self.estatus ='idle' 
            
    def acoes(self,jogador):
        if self.estatus == 'attack':
            self.tempo_ataque = pygame.time.get_ticks()
        elif self.estatus =='move':
            self.direcao = self.pegar_distancia_direcao_jogador(jogador)[1]
        else:
            self.direcao = pygame.math.Vector2()
    
    def animar(self):
        animacao = self.animacoes[self.estatus]
        
        self.indice_frame += self.velocidade_animacao
        if self.indice_frame >= len(animacao):
            if self.estatus == 'attack':
                self.pode_atacar = False
            self.indice_frame = 0
            
        self.image = animacao[int(self.indice_frame)]
        self.rect = self.image.get_rect(center = self.ponto_colisao.center)
            
    def esfriamento(self):
        if not self.pode_atacar:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_ataque >= self.esfriamento_ataque:
                self.pode_atacar = True
    
    def pegar_dano(self,jogador,tipo_ataque):   
        if tipo_ataque == 'weapon':
            self.vida -= jogador.pegar_dano_arma()  
        else:
            pass
        
    def checar_morte(self):
        if self.vida <= 0:
            self.kill()
               
    def update(self):
        self.mover(self.velocidade)
        self.animar()
        self.esfriamento()
        self.checar_morte()
        
    def inimigo_update(self,jogador):
       self.pegar_estatus(jogador)
       self.acoes(jogador)
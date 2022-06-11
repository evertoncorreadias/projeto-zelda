import pygame
from config import*
from suporte import importar_pasta
from entidade import Entidade

class Jogador(Entidade):
    def __init__(self, pos, groups,sprites_obstaculos,criar_ataque,destruir_arma,criar_magica):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha() # CARREGANDO IMAGEM
        self.rect = self.image.get_rect(topleft =pos)  # CRIANDO E POSICIONANDO A IMAGEM 
        self.ponto_colisao = self.rect.inflate(0,-26) # DIMINUI OS SPRITES NO PONTO DE COLISAO JOGADOR
        
        # GRAFICOS
        self.importar_imagem_jogador()
        self.estatus = "down"
         
        # ATAQUE
        self.atacando = False
        self.esfriar_ataque = 400
        self.tempo_ataque = None
        self.criar_ataque = criar_ataque
        
        self.sprites_obstaculos = sprites_obstaculos
        
        # ARMAS
        self.indice_arma = 0
        self.arma = list(weapon_data.keys())[self.indice_arma]
        self.destruir_arma = destruir_arma
        
        # MAGICA
        self.criar_magica = criar_magica
        self.indice_magica = 0
        self.magica = list(magic_data.keys())[self.indice_magica]
        self.pode_mudar_magica = True
        self.tempo_troca_magica = None
        
        # TEMPORIZADOR DE TROCA DE ARMA
        self.pode_mudar_arma = True
        self.tempo_troca_arma = None
        self.duracao_troca = 200
        
        # ESTATISTICAS
    
        self.status = {'health': 180, 'energy': 60, 'attack': 10, 'magic':4, 'speed': 5}
        self.vida = self.status['health'] *0.2
        self.energia = self.status['energy'] *0.5
        self.exp = 123
        self.velocidade = self.status['speed']
                   
    def importar_imagem_jogador(self):
        pasta_personagens = 'graphics/player/'
        self.animacoes = {'up': [], 'down': [], 'left': [], 'right':[],
                          'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle':[],
                          'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack':[]}
        
        for animacao in self.animacoes.keys():
            diretorio_completo = pasta_personagens + '/' + animacao
            self.animacoes[animacao] = importar_pasta(diretorio_completo)
                   
    def controle(self): 
        if not self.atacando:
            teclas = pygame.key.get_pressed()
            # MOVIMENTO DO JOGADOR
            if teclas[pygame.K_UP]:
                self.direcao.y = -1
                self.estatus = 'up'
            elif teclas[pygame.K_DOWN]:
                self.direcao.y = 1
                self.estatus = 'down'
            else:
                self.direcao.y = 0
                
            if teclas[pygame.K_RIGHT]:
                self.direcao.x = 1
                self.estatus = 'right'
            elif teclas[pygame.K_LEFT]:
                self.direcao.x = -1
                self.estatus = 'left'
            else:
                self.direcao.x = 0
            # ATAQUE DO JOGADOR   
            if teclas[pygame.K_SPACE]:
                self.atacando =True
                self.tempo_ataque = pygame.time.get_ticks()
                self.criar_ataque()
                
            # MAGICA DO JOGADOR
            if teclas[pygame.K_LCTRL]:
                self.atacando =True
                self.tempo_ataque = pygame.time.get_ticks()
                estilo = list(magic_data.keys())[self.indice_magica]
                forca = list(magic_data.values())[self.indice_magica]['strength'] + self.status['magic']
                custo = list(magic_data.values())[self.indice_magica]['cost']
                self.criar_magica(estilo, forca, custo)
                
            if teclas[pygame.K_q] and self.pode_mudar_arma:
                self.pode_mudar_arma = False
                self.tempo_troca_arma = pygame.time.get_ticks()
                
                if self.indice_arma < len(list(weapon_data.keys())) - 1:
                    self.indice_arma += 1
                else:
                    self.indice_arma = 0
                self.arma = list(weapon_data.keys())[self.indice_arma]
                
            if teclas[pygame.K_e] and self.pode_mudar_magica:
                self.pode_mudar_magica = False
                self.tempo_troca_magica = pygame.time.get_ticks()
                
                if self.indice_magica < len(list(magic_data.keys())) - 1:
                    self.indice_magica += 1
                else:
                    self.indice_magica = 0
                self.magica = list(magic_data.keys())[self.indice_magica]
        
    def pegar_estatus(self):
        
        # ESTATUS OCIOSO
        if self.direcao.x == 0 and self.direcao.y == 0:
            if not 'idle' in self.estatus and not 'attack' in self.estatus:
                self.estatus = self.estatus + '_idle' 
                
        # ESTATUS ATAQUE
        if self.atacando:
            self.direcao.x = 0
            self.direcao.y = 0
            if not 'attack' in self.estatus:
                if 'idle' in self.estatus:
                    self.estatus = self.estatus.replace('_idle', '_attack')
                else:
                    self.estatus = self.estatus + '_attack' 
        else:
            if 'attack' in self.estatus:
                self.estatus = self.estatus.replace('_attack', '')
            
    def animar(self): #ANIMAÇÃO DO JOGADOR
        animacao = self.animacoes[self.estatus]
        
        #LOOP SOBRE O INDICE DO FRAME
        self.indice_frame += self.velocidade_animacao
        if self.indice_frame >= len(animacao):
            self.indice_frame = 0
            
        # ACERTANDO A IMAGEM
        self.image = animacao[int(self.indice_frame)]
        self.rect = self.image.get_rect(center = self.ponto_colisao.center)
                                                                  
    def esfriamento(self):   # conta o tempo de ataque do jogador
        tempo_atual = pygame.time.get_ticks()  
        if self.atacando:
            if tempo_atual - self.tempo_ataque >= self.esfriar_ataque:  
                self.atacando = False  
                self.destruir_arma() 
                
        if not self.pode_mudar_arma:
            if tempo_atual - self.tempo_troca_arma > self.duracao_troca:
                self.pode_mudar_arma = True
        
        if not self.pode_mudar_magica:
            if tempo_atual - self.tempo_troca_magica > self.duracao_troca:
                self.pode_mudar_magica = True
            
    def update(self):
        self.controle()
        self.esfriamento()
        self.pegar_estatus()
        self.animar()
        self.mover(self.velocidade)
        
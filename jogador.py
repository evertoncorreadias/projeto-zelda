import pygame
from config import*
from suporte import importar_pasta

class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, groups,sprites_obstaculos,criar_ataque,destruir_arma):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha() # CARREGANDO IMAGEM
        self.rect = self.image.get_rect(topleft =pos)  # CRIANDO E POSICIONANDO A IMAGEM 
        self.ponto_colisao = self.rect.inflate(0,-26) # DIMINUI OS SPRITES NO PONTO DE COLISAO JOGADOR
        
        # GRAFICOS
        self.importar_imagem_jogador()
        self.estatus = "down"
        self.indice_frame = 0
        self.velocidade_animacao = 0.15
                
        
         # MOVIMENTO
        self.direcao = pygame.math.Vector2()
        self.speed = 5
        
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
        # TEMPORIZADOR DE TROCA DE ARMA
        self.pode_mudar_arma = True
        self.tempo_troca_arma = None
        self.duracao_troca = 200
        
        
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
                print('magica')
                
            if teclas[pygame.K_q] and self.pode_mudar_arma:
                self.pode_mudar_arma = False
                self.tempo_troca_arma = pygame.time.get_ticks()
                
                if self.indice_arma < len(list(weapon_data.keys())) - 1:
                    self.indice_arma += 1
                else:
                    self.indice_arma = 0
                self.arma = list(weapon_data.keys())[self.indice_arma]
        
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
                                               
    def esfriamento(self):   # conta o tempo de ataque do jogador
        tempo_atual = pygame.time.get_ticks()  
        if self.atacando:
            if tempo_atual - self.tempo_ataque >= self.esfriar_ataque:  
                self.atacando = False  
                self.destruir_arma() 
                
        if not self.pode_mudar_arma:
            if tempo_atual - self.tempo_troca_arma > self.duracao_troca:
                self.pode_mudar_arma = True
            
    def update(self):
        self.controle()
        self.esfriamento()
        self.pegar_estatus()
        self.animar()
        self.mover(self.speed)
        
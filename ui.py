import pygame
from config import *

class UI:
    def __init__(self):
        # GERAL
        self.exibe_superfice =pygame.display.get_surface()
        self.fonte = pygame.font.Font( UI_FONT, UI_FONT_SIZE)
        
        # CONFIGURAÇÃO BARRA SAUDE E ENERGIA
        self.barra_vida = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.barra_energia = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        
        # CONVERTER DICIONARIO ARMAS
        self.grafico_armas = []
        for arma in weapon_data.values():
            diretorio = arma['graphic']
            arma = pygame.image.load(diretorio).convert_alpha()
            self.grafico_armas.append(arma)
            
        # CONVERTER DICIONARIO MAGICA
        self.grafico_magica = []
        for magica in magic_data.values():
            magica = pygame.image.load(magica['graphic']).convert_alpha()
            self.grafico_magica.append(magica)
               
    def mostrar_barra(self, atual, maximo, fundo_rect, cor):
        
        # DESENHAR FUNDO
        pygame.draw.rect(self.exibe_superfice, UI_BG_COLOR, fundo_rect)
        
        #CONVERTENDO ESTATUS PARA PIXEL
        proporcao = atual / maximo
        largura_atual = fundo_rect.width * proporcao
        atual_rect = fundo_rect.copy()
        atual_rect.width = largura_atual
        
        # DESENHAR A BARRA
        pygame.draw.rect(self.exibe_superfice, cor, atual_rect)
        pygame.draw.rect(self.exibe_superfice, UI_BORDER_COLOR, atual_rect,3)
        
    def mostrar_exp(self,exp):
        superficie_texto = self.fonte.render(str(int(exp)), False, TEXT_COLOR)
        x = self.exibe_superfice.get_size()[0] - 20
        y = self.exibe_superfice.get_size()[1] - 20
        texto_rect = superficie_texto.get_rect(bottomright = (x,y))  
        
        pygame.draw.rect(self.exibe_superfice, UI_BG_COLOR, texto_rect.inflate(20, 20)) # FUNDO PRETO EXPERIENCIA JOGADOR
        self.exibe_superfice.blit(superficie_texto, texto_rect)
        pygame.draw.rect(self.exibe_superfice, UI_BORDER_COLOR, texto_rect.inflate(20, 20),3)  # BORDA DA EXPERIENCIA
    
    def caixa_selecao(self,esquerda,topo,mudou_arma):
        fundo_rect = pygame.Rect(esquerda, topo, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.exibe_superfice, UI_BG_COLOR, fundo_rect)
        if mudou_arma:
            pygame.draw.rect(self.exibe_superfice, UI_BORDER_COLOR_ACTIVE, fundo_rect,3)
        else:
            pygame.draw.rect(self.exibe_superfice, UI_BORDER_COLOR, fundo_rect,3)
        return fundo_rect
        
    def troca_armas(self, indice_arma,mudou_arma):
        fundo_rect = self.caixa_selecao(10,630,mudou_arma) # SELEÇÃO DE ARMAS
        superfice_arma = self.grafico_armas[indice_arma]
        arma_rect = superfice_arma.get_rect(center = fundo_rect.center)
         
        self.exibe_superfice.blit(superfice_arma, arma_rect)
            
    def troca_magica(self, indice_magica,mudou_magica):
        fundo_rect = self.caixa_selecao(85,635,mudou_magica) # SELEÇÃO DE ARMAS
        superfice_magica = self.grafico_magica[indice_magica]
        magica_rect = superfice_magica.get_rect(center = fundo_rect.center)
         
        self.exibe_superfice.blit(superfice_magica, magica_rect)
                   
    def mostrar(self,jogador):
        self.mostrar_barra(jogador.vida, jogador.status['health'],self.barra_vida, HEALTH_COLOR)
        self.mostrar_barra(jogador.energia, jogador.status['energy'],self.barra_energia, ENERGY_COLOR)
        
        self.mostrar_exp(jogador.exp)
        self.troca_armas(jogador.indice_arma,not jogador.pode_mudar_arma)
        self.troca_magica(jogador.indice_magica,not jogador.pode_mudar_magica)
        

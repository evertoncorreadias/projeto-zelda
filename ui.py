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
        
        
    def mostrar(self,jogador):
        self.mostrar_barra(jogador.vida, jogador.status['health'],self.barra_vida, HEALTH_COLOR)
        self.mostrar_barra(jogador.energia, jogador.status['energy'],self.barra_energia, ENERGY_COLOR)
        
        self.mostrar_exp(jogador.exp)
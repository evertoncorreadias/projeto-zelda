import pygame
from config import *

class Atualizar:
    def __init__(self,jogador):
       # CONFIGURAÇOES GERAIS
       self.exibe_superfice = pygame.display.get_surface()
       self.jogador = jogador 
       self.atributo_num = len(jogador.status)
       self.atributo_nomes = list(jogador.status.keys())
       self.valor_max = list(jogador.status_max.values())
       self.fonte = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
       
       # TAMANHO ITENS
       self.altura = self.exibe_superfice.get_size()[1] * 0.8
       self.largura = self.exibe_superfice.get_size()[0] // 6
       self.criar_itens()
       
       # SELEÇAO DE SISTEMA
       self.selecao_indice = 0
       self.selecao_tempo = None
       self.pode_mover = True
       
       
    def entrada(self):
        teclas = pygame.key.get_pressed()
        if self.pode_mover:
            if teclas[pygame.K_RIGHT] and self.selecao_indice < self.atributo_num - 1:
                self.selecao_indice += 1
                self.pode_mover = False
                self.selecao_tempo = pygame.time.get_ticks()
                
            elif teclas[pygame.K_LEFT] and self.selecao_indice >= 1:
                self.selecao_indice -=1
                self.pode_mover = False
                self.selecao_tempo = pygame.time.get_ticks()
                
            if teclas[pygame.K_SPACE]:
                self.pode_mover = False
                self.selecao_tempo = pygame.time.get_ticks()
                self.itens_lista[self.selecao_indice].gatilho(self.jogador)
       
    def esfriamento_selecao(self):
        if not self.pode_mover:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.selecao_tempo >= 300:
                self.pode_mover = True
    
    def criar_itens(self):
        self.itens_lista = []
        
        for item,indice in enumerate(range(self.atributo_num)):
            largura_total = self.exibe_superfice.get_size()[0]
            incremento = largura_total // self.atributo_num
            esquerda = (item * incremento) + (incremento - self.largura) // 2
            topo = self.exibe_superfice.get_size()[1] * 0.1
            
            item = Item(esquerda, topo, self.largura, self.altura, indice, self.fonte)
            self.itens_lista.append(item)
           
    def display(self):
         self.entrada()
         self.esfriamento_selecao()
         
         for indice,item in enumerate(self.itens_lista):
             nome = self.atributo_nomes[indice]
             valor = self.jogador.pegar_valor_indice(indice)
             valor_max = self.valor_max[indice]
             custo = self.jogador.pegar_custo_indice(indice)
             item.display(self.exibe_superfice, self.selecao_indice, nome, valor, valor_max, custo)
             
         
class Item:
    def __init__(self, l, t, a, h ,indice, fonte):
        self.rect = pygame.Rect(l, t, a, h)
        self.indice = indice
        self.fonte = fonte
        
    def mostrar_nomes(self,superfice,nome,custo,selecionado):
        cor = TEXT_COLOR_SELECTED if selecionado else TEXT_COLOR
        
        titulo = self.fonte.render(nome, False, cor)
        titulo_rect = titulo.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0, 20))
        
        custo_surf = self.fonte.render(f'{int(custo)}', False, cor)
        custo_rect = custo_surf.get_rect(midbottom = self.rect.midbottom - pygame.math.Vector2(0, 20))
        
        superfice.blit(titulo, titulo_rect)
        superfice.blit(custo_surf, custo_rect)
        
    def mostrar_barra(self, superfice, valor, valor_max, selecionado):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        cor = BAR_COLOR_SELECTED if selecionado else BAR_COLOR
        
        altura_total = bottom[1] - top[1]
        numero_relativo = (valor / valor_max) * altura_total
        valor_rect = pygame.Rect(top[0] - 15, bottom[1] - numero_relativo, 30, 10)
        
        pygame.draw.line(superfice, cor, top, bottom,5)
        pygame.draw.rect(superfice,cor,valor_rect)
        
    def gatilho(self, jogador):
        atualizar_atributo = list(jogador.status.keys())[self.indice]
        
        if jogador.exp >= jogador.atualizar_custo[atualizar_atributo] and jogador.status[atualizar_atributo] < jogador.status_max[atualizar_atributo]:
            jogador.exp -= jogador.atualizar_custo[atualizar_atributo]
            jogador.status[atualizar_atributo] *= 1.2
            jogador.atualizar_custo[atualizar_atributo] *= 1.4
            
        if jogador.status[atualizar_atributo] > jogador.status_max[atualizar_atributo]:
            jogador.status[atualizar_atributo] = jogador.status_max[atualizar_atributo]
         
        
    def display(self, superfice, selecao_num, nome, valor, valor_max, custo):
        if self.indice == selecao_num:
           pygame.draw.rect(superfice, UPGRADE_BG_COLOR_SELECTED, self.rect)
           pygame.draw.rect(superfice, UI_BG_COLOR, self.rect,4 )
        else: 
            pygame.draw.rect(superfice, UI_BG_COLOR, self.rect)
            pygame.draw.rect(superfice, UI_BG_COLOR, self.rect,4 )
        self.mostrar_nomes(superfice, nome, custo, self.indice == selecao_num)
        self.mostrar_barra(superfice, valor,valor_max, self.indice == selecao_num)
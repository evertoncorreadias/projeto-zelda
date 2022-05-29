import pygame
pygame.init()
fonte = pygame.font.Font(None, 30)

def depuracao(info,y =10, x =10):
   exibe_superfice = pygame.display.get_surface()
   dep_sup = fonte.render(str(info), True, 'White') 
   dep_rect = dep_sup.get_rect(topleft = (x,y))
   pygame.draw.rect(exibe_superfice, 'Black', dep_rect)
   exibe_superfice.blit(dep_sup, dep_rect)
from mimetypes import init
import pygame
from suporte import importar_pasta
from random import choice

class AnimacaoJogador:
    def __init__(self):
        self.frames = {
        # MAGICAS
        'flame': importar_pasta('graphics/particles/flame/frames'),
        'aura': importar_pasta('graphics/particles/aura'),
        'heal': importar_pasta('graphics/particles/heal/frames'),

        # ATAQUES
        'claw': importar_pasta('graphics/particles/claw'),
        'slash': importar_pasta('graphics/particles/slash'),
        'sparkle': importar_pasta('graphics/particles/sparkle'),
        'leaf_attack': importar_pasta('graphics/particles/leaf_attack'),
        'thunder': importar_pasta('graphics/particles/thunder'),

        # MORTE DOS MONSTROS
        'squid': importar_pasta('graphics/particles/smoke_orange'),
        'raccoon': importar_pasta('graphics/particles/raccoon'),
        'spirit': importar_pasta('graphics/particles/nova'),
        'bamboo': importar_pasta('graphics/particles/bamboo'),

        # FOLHAS
        'leaf': (
            importar_pasta('graphics/particles/leaf1'),
            importar_pasta('graphics/particles/leaf2'),
            importar_pasta('graphics/particles/leaf3'),
            importar_pasta('graphics/particles/leaf4'),
            importar_pasta('graphics/particles/leaf5'),
            importar_pasta('graphics/particles/leaf6'),
            self.reflexo_imagem(importar_pasta('graphics/particles/leaf1')),
            self.reflexo_imagem(importar_pasta('graphics/particles/leaf2')),
            self.reflexo_imagem(importar_pasta('graphics/particles/leaf3')),
            self.reflexo_imagem(importar_pasta('graphics/particles/leaf4')),
            self.reflexo_imagem(importar_pasta('graphics/particles/leaf5')),
            self.reflexo_imagem(importar_pasta('graphics/particles/leaf6'))
            )
        }
        
        
    def reflexo_imagem(self,frames):  
        novos_frames = []
        for frame in frames:
            giro_frame = pygame.transform.flip(frame,True,False)
            novos_frames.append(giro_frame)
        return novos_frames      

    def criar_particulas_grama(self, pos, groups):
        animacao_frames = choice(self.frames['leaf'])
        EfeitoParticula(pos,animacao_frames,groups)
        
    def criar_particulas(self, tipo_animacao, pos,groups):
        frames_animacao = self.frames[tipo_animacao]
        EfeitoParticula(pos, frames_animacao, groups)
        
    
class EfeitoParticula(pygame.sprite.Sprite):
    def __init__(self, pos ,frames_animacao, groups):
        super().__init__(groups)
        self.tipo_sprite = 'magic'
        self.indice_frame = 0
        self.velocidade_animacao = 0.15
        self.frames = frames_animacao
        self.image = self.frames[self.indice_frame]
        self.rect = self.image.get_rect(center = pos)
    
        
    def animar(self):
        self.indice_frame += self.velocidade_animacao
        if self.indice_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.indice_frame)]
            
    def update(self):
        self.animar()
        
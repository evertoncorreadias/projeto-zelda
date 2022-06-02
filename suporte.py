import pygame
from csv import reader
from os import walk

import pygame

def importar_csv_layout(diretorio): # abre, converte o arquivo csv e salva ele em uma lista
    terreno_mapa =[]
    with open(diretorio) as mapa_nivel:
        layout = reader(mapa_nivel,delimiter = ',')
        for linha in layout:
            terreno_mapa.append(list(linha))
        return terreno_mapa
             
# print(importar_csv_layout('map/map_FloorBlocks.csv'))


def importar_pasta(diretorio): 
    lista_superficie = []
    for _,__,img_files in walk(diretorio):
        for image in img_files:
            diretorio_completo = diretorio + '/' + image
            imagem_superficie = pygame.image.load(diretorio_completo).convert_alpha()
            lista_superficie.append(imagem_superficie)
    return lista_superficie         

            
        
    
import pygame
import os
from pygame.locals import *
from sys import exit

def mostrar_inicio():
    BASE_DIR = os.path.dirname(__file__)
    IMG_DIR = os.path.join(BASE_DIR, "imagens")

    def img(nome_arquivo):
        return os.path.join(IMG_DIR, nome_arquivo)

    pygame.init()
    LARGURA = 800
    ALTURA = 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))

    imagem_inicio = pygame.image.load(img("background.png"))
    imagem_inicio = pygame.transform.scale(imagem_inicio, (LARGURA, ALTURA))
    pygame.display.set_caption("Robot Defense - Template")

    estado = 'menu'

    logo = pygame.image.load(img('naveDoJogo.png')).convert_alpha()
    logo = pygame.transform.scale(logo, (50 * 3, 30 * 5))
    logo_x = 330
    logo_y = 200

    logo_vel = 60.0
    logo_y_min = 50 - 10
    logo_y_max = 50 + 10

    botao = pygame.image.load(img('botãostart.png')).convert_alpha()
    botao = pygame.transform.scale(botao, (32*7, 32*7))
    botao_x = 290
    botao_y = 250
    botao_rect = botao.get_rect(topleft=(botao_x, botao_y))
    FPS = 60

    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(FPS) / 1000.0
        logo_y += logo_vel * dt

        if logo_y < logo_y_min: 
            logo_y= logo_y_min
            logo_vel = -logo_vel
        elif logo_y> logo_y_max:
            logo_y= logo_y_max
            logo_vel = -logo_vel

        if estado == 'menu':
            tela.blit(imagem_inicio, (0,0))

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
               mouse_x, mouse_y = pygame.mouse.get_pos()
               if botao_rect.collidepoint(mouse_x, mouse_y):
                 print ("botão acionado")
                 if estado == 'menu':
                    return
                
        tela.blit(botao,(botao_x, botao_y))
        tela.blit(logo,(logo_x, logo_y))
        pygame.display.update()
        clock.tick(60)

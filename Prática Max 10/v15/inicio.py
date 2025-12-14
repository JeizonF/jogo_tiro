import pygame
import os
from pygame.locals import *
from sys import exit



def desenhar_pause(tela):
    overlay = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))  # preto semi-transparente FIXO

    tela.blit(overlay, (0, 0))

    fonte = pygame.font.Font(None, 72)
    texto = fonte.render("PAUSADO", True, (255, 255, 255))
    rect = texto.get_rect(center=tela.get_rect().center)
    tela.blit(texto, rect)


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

    logo = pygame.image.load(img('Nome do Jogo.png')).convert_alpha()
    logo = pygame.transform.scale(logo, (140 * 3, 100 * 5))
    logo_x = LARGURA // 4
    logo_y = 50

    logo_vel = 60.0
    logo_y_min = 50 - 10
    logo_y_max = 50 + 10

    botao = pygame.image.load(img('botãostart.png')).convert_alpha()
    botao = pygame.transform.scale(botao, (32*7, 32*7))
    botao_x = 290
    botao_y = 300
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

def mostrar_game_over(pontos):
    BASE_DIR = os.path.dirname(__file__)
    IMG_DIR = os.path.join(BASE_DIR, "imagens")
    FONT_DIR = os.path.join(BASE_DIR, "recursos", "fonts")

    def img(nome):
        return os.path.join(IMG_DIR, nome)

    def font(nome):
        return os.path.join(FONT_DIR, nome)

    pygame.init()
    LARGURA, ALTURA = 800, 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Robot Defense")

    background = pygame.image.load(img("background.png"))
    background = pygame.transform.scale(background, (LARGURA, ALTURA))

    fonte_titulo = pygame.font.Font(font("Eight-Bit Madness.ttf"), 120)
    fonte_texto = pygame.font.Font(font("Eight-Bit Madness.ttf"), 40)

    botao_reiniciar = pygame.image.load(img("botaoreiniciar.png")).convert_alpha()
    botao_reiniciar = pygame.transform.scale(botao_reiniciar, (32 * 10, 32 * 7))
    botao_rect = botao_reiniciar.get_rect(center=(LARGURA // 2, 380))

    clock = pygame.time.Clock()
    rodando = True

    while rodando:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(pygame.mouse.get_pos()):
                    return  

        tela.blit(background, (0, 0))

        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))

        titulo = fonte_titulo.render("GAME OVER", True, (255, 0, 0))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 120))

        texto_pontos = fonte_texto.render(f"Pontos: {pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (LARGURA // 2 - texto_pontos.get_width() // 2, 220))

        tela.blit(botao_reiniciar, botao_rect)

        pygame.display.flip()

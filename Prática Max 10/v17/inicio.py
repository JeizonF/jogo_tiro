import pygame
import os
from pygame.locals import *
from sys import exit



def desenhar_pause(tela):
    overlay = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120)) 

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
    LARGURA, ALTURA = 800, 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Robot Defense - Template")

    background = pygame.image.load(img("background.png"))
    background = pygame.transform.scale(background, (LARGURA, ALTURA))

    # fontes
    fonte_titulo = pygame.font.Font(None, 64)
    fonte_texto = pygame.font.Font(None, 32)

    # imagens
    logo = pygame.image.load(img('Nome do Jogo.png')).convert_alpha()
    logo = pygame.transform.scale(logo, (140 * 3, 100 * 5))

    botao = pygame.image.load(img('botãostart.png')).convert_alpha()
    botao = pygame.transform.scale(botao, (32 * 7, 32 * 7))
    botao_rect = botao.get_rect(center=(LARGURA // 2, 420))

    clock = pygame.time.Clock()

    estado = "creditos"
    velocidade_creditos = 40  
    y_creditos = ALTURA + 20
    


    while True:
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                exit()

            if evento.type == KEYDOWN:
                if estado == "creditos":
                    estado = "menu"

            if evento.type == MOUSEBUTTONDOWN:
                if estado == "menu" and botao_rect.collidepoint(pygame.mouse.get_pos()):
                    return  # entra no jogo

        # ---------------- DESENHO ----------------

        tela.blit(background, (0, 0))

        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        tela.blit(overlay, (0, 0))

        if estado == "creditos":
            textos = [
                "CRÉDITOS",
                "",
                "Robot Defense",
                "",
                "Lógicas",
                "Arthur - Robô cíclico",
                "Alisson - Explosões",
                "Junior - Boss",
                "Wesley - Robô saltador e tela de dificuldade",
                "Jeizon - Robô ziguezague, robô lento, robô rápido, robô caçador,",
                "buffs, easter egg, corações, parte da tela de dificuldade e tela de pause",
                "",
                "Arte",
                "Alisson - Jogador, tiros, robô rápido, robô cíclico e explosões",
                "Gabriel - Robô lento, robô caçador, robô saltador, easter egg e buffs",
                "",
                "Sons",
                "Gabriel - Músicas e efeitos sonoros",
                "",
                "Telas",
                "Arthur - Início e Game Over",
                "Wesley - Dificuldade",
                "Jeizon - Pause",
                "",
                "Pressione qualquer tecla para continuar"
            ]

            y = y_creditos
            for i, linha in enumerate(textos):
                if i == 0:
                    texto = fonte_titulo.render(linha, True, (255, 255, 255))
                    x = LARGURA // 2 - texto.get_width() // 2
                    tela.blit(texto, (x, y))
                    y += 70
                else:
                    texto = fonte_texto.render(linha, True, (255, 255, 255))
                    x = LARGURA // 2 - texto.get_width() // 2
                    tela.blit(texto, (x, y))
                    y += 32

            y_creditos -= velocidade_creditos * (clock.get_time() / 1000)


        elif estado == "menu":
            logo_rect = logo.get_rect(center=(LARGURA // 2, 120))
            tela.blit(logo, logo_rect)
            tela.blit(botao, botao_rect)

        pygame.display.flip()


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

import pygame
import os
import random
import math
from sons import *

BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "imagens")

def img(nome_arquivo):
    return os.path.join(IMG_DIR, nome_arquivo)

pygame.init()

LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))

background = pygame.image.load(img("background.png"))
background = pygame.transform.scale(background, (LARGURA, ALTURA))
pygame.display.set_caption("Robot Defense - Template")

tema = Tema()
FPS = 60
clock = pygame.time.Clock()


dificuldade = "medio" 
spawn_intervalo = 400 
velocidade_multiplicador = 1.0
dano_multi = 1

class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.velocidade = velocidade * velocidade_multiplicador
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image = pygame.image.load(img("naveDoJogo.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.vida = 5
        self.tiro_triplo = False
        self.buff_velocidade_tempo = 0
        self.buff_tiro_tempo = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.mover(0, -self.velocidade)
        if keys[pygame.K_s]:
            self.mover(0, self.velocidade)
        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)
        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)

        self.rect.x = max(0, min(self.rect.x, LARGURA - 70))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 70))

        if self.buff_tiro_tempo > 0:
            self.buff_tiro_tempo -= 1
            if self.buff_tiro_tempo <= 0:
                self.tiro_triplo = False
        if self.buff_velocidade_tempo > 0:
            self.buff_velocidade_tempo -= 1
            if self.buff_velocidade_tempo <= 0:
                self.velocidade = 5 * velocidade_multiplicador

class Tiro(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image = pygame.image.load(img("tiro.png"))
        self.image = pygame.transform.scale(self.image, (20, 20))
        Sons.som_tiro()

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()

class Tiro2(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image = pygame.image.load(img("tiro.png"))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.direcao = 1

    def update(self):
        self.rect.y -= self.velocidade
        self.rect.x += -self.direcao * 5
        if self.rect.y < 0:
            self.kill()

class Tiro3(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image = pygame.image.load(img("tiro.png"))
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.direcao = 1

    def update(self):
        self.rect.y -= self.velocidade
        self.rect.x += self.direcao * 5
        if self.rect.y < 0:
            self.kill()

class Robo(Entidade):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 0, 0))
        self.tipo = "normal"
        self.dano = dano_multi

    def atualizar_posicao(self):
        raise NotImplementedError

class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.direcao = 1
        self.image = pygame.image.load(img("robo_ziguezague.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3
        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

class RoboSaltador(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.image = pygame.image.load(img("robo_saltador.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.velocidade_y = -3 * velocidade_multiplicador
        self.gravidade = 0.2
        self.chao_y = ALTURA - 60
        self.descida = 1
        self.direcao = 3
        self.bateu = False

    def atualizar_posicao(self):
        self.velocidade_y += self.gravidade
        self.rect.y += self.velocidade_y
        self.rect.y += self.descida

        if self.rect.y >= self.chao_y:
            self.rect.y = self.chao_y
            self.velocidade_y = -10 * velocidade_multiplicador
            self.bateu = True

        if self.bateu:
            self.rect.x += self.direcao * 2
            if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
                self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

class RoboLento(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.direcao = 1
        self.image = pygame.image.load(img("robo_lento.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))

    def atualizar_posicao(self):
        self.rect.y += self.velocidade * 0.5

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

class RoboRapido(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.direcao = 1
        self.image = pygame.image.load(img("robo_rapido.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))

    def atualizar_posicao(self):
        self.rect.y += self.velocidade * 2

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

class RoboCiclico(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=2)
        self.image = pygame.image.load(img("robo_ciclico.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.centro_x = x
        self.centro_y = y
        self.raio = 60
        self.angulo = 0
        self.velocidade_angular = 0.08

    def atualizar_posicao(self):
        self.angulo += self.velocidade_angular
        self.rect.x = self.centro_x + self.raio * math.cos(self.angulo)
        self.rect.y = self.centro_y + self.raio * math.sin(self.angulo)
        self.centro_y += 1 * velocidade_multiplicador

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA + 50:
            self.kill()

class RoboCacador(Robo):
    def __init__(self, x, y, alvo):
        super().__init__(x, y, velocidade=3)
        self.image = pygame.image.load(img("robo_cacador.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.alvo = alvo

    def atualizar_posicao(self):
        if self.rect.x < self.alvo.rect.x - self.velocidade:
            self.rect.x += self.velocidade
        elif self.rect.x > self.alvo.rect.x + self.velocidade:
            self.rect.x -= self.velocidade

        if self.rect.y < self.alvo.rect.y:
            self.rect.y += self.velocidade
        elif self.rect.y > self.alvo.rect.y:
            self.rect.y -= self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

class RoboChefao(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.image = pygame.image.load(img("robo_chefao.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.vida = 30
        self.tipo = "chefao"

    def atualizar_posicao(self):
        self.rect.y = 200

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

class VidaExtra(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.tipo = "vida"
        self.image = pygame.image.load(img("buff cura.png"))
        self.image = pygame.transform.scale(self.image, (40 * 2, 40 * 2))
        self.direcao = 1

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao
        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()

class Velocidade(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.tipo = "velocidade"
        self.image = pygame.image.load(img("buff energia.png"))
        self.image = pygame.transform.scale(self.image, (50 * 2, 50 * 2))
        self.direcao = 1

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao
        if self.rect.x <= 0 or self.rect.x >= LARGURA - 105:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()

class TiroTriplo(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.tipo = "tiro"
        self.image = pygame.image.load(img("buff municao.png"))
        self.image = pygame.transform.scale(self.image, (50 * 2, 50 * 2))
        self.direcao = 1

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao
        if self.rect.x <= 0 or self.rect.x >= LARGURA - 105:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()

def menu():
    global dificuldade, spawn_intervalo, velocidade_multiplicador, dano_multi
    menu_rodando = True
    opcao_selecionada = 0
    opcoes = ["Facil", "Medio", "Dificil"]
    
    font_titulo = pygame.font.SysFont(None, 50)
    font_opcao = pygame.font.SysFont(None, 40)
    
    while menu_rodando:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                elif event.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                elif event.key == pygame.K_RETURN:
                    dificuldade = opcoes[opcao_selecionada].lower()
                    if dificuldade == "facil":
                        spawn_intervalo = 600
                        dano_multi = 1
                        velocidade_multiplicador = 0.8
                    elif dificuldade == "medio":
                        spawn_intervalo = 400
                        velocidade_multiplicador = 1.0
                        dano_multi = 2
                    elif dificuldade == "dificil":
                        spawn_intervalo = 250
                        velocidade_multiplicador = 1.5
                        dano_multi = 3
                    menu_rodando = False
        
        TELA.blit(background, (0, 0))
        
        titulo = font_titulo.render("Robot Defense", True, (255, 255, 255))
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 150))
        
        for macdemarco, opcao in enumerate(opcoes):
            cor = (255, 255, 0) if macdemarco == opcao_selecionada else (255, 255, 255)
            texto_opcao = font_opcao.render(opcao, True, cor)
            TELA.blit(texto_opcao, (LARGURA // 2 - texto_opcao.get_width() // 2, 250 + macdemarco * 50))
        
        instrucoes = font_opcao.render("Use as setas para navegar e Enter para selecionar", True, (255, 255, 255))
        TELA.blit(instrucoes, (LARGURA // 2 - instrucoes.get_width() // 2, 450))
        
        pygame.display.flip()
menu()
power_up = pygame.sprite.Group()
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()

chefao_vivo = None
if chefao_vivo is None:
    roboChe = RoboChefao(random.randint(200, LARGURA - 40), -100)
    todos_sprites.add(roboChe)
    inimigos.add(roboChe)
    chefao_vivo = roboChe

jogador = Jogador(LARGURA // 2, ALTURA - 60)
todos_sprites.add(jogador)

pontos = 0
spawn_timer = 0
tiro_timer = 0

coracao = pygame.image.load(img("coracao.png"))
coracao = pygame.transform.scale(coracao, (32, 32))
coracao_vazio = pygame.image.load(img("coracao_vazio.png"))
coracao_vazio = pygame.transform.scale(coracao_vazio, (32, 32))
vida_maxima = jogador.vida

def desenhar_coracoes(tela, vida_atual, vida_maxima, cor_cheio, cor_vazio):
    for i in range(vida_maxima):
        x = 10 + i * 40
        if i < vida_atual:
            tela.blit(cor_cheio, (x, 10))
        else:
            tela.blit(cor_vazio, (x, 10))


menu()

rodando = True
while rodando:
    tema.som_tema()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    keys = pygame.key.get_pressed()
    tiro_timer += 1
    if keys[pygame.K_SPACE] and tiro_timer >= 15:
        tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
        todos_sprites.add(tiro)
        tiros.add(tiro)
        if jogador.tiro_triplo:
            tiro2 = Tiro2(jogador.rect.centerx, jogador.rect.y)
            tiro3 = Tiro3(jogador.rect.centerx, jogador.rect.y)
            todos_sprites.add(tiro2, tiro3)
            tiros.add(tiro2, tiro3)
        tiro_timer = 0

    spawn_timer += 1
    if spawn_timer > spawn_intervalo:
        roboZ = RoboZigueZague(random.randint(40, LARGURA - 40), -40)
        roboS = RoboSaltador(random.randint(40, LARGURA - 40), -40)
        roboL = RoboLento(random.randint(40, LARGURA - 40), -40)
        roboR = RoboRapido(random.randint(40, LARGURA - 40), -40)
        roboC = RoboCiclico(random.randint(40, LARGURA - 40), -40)
        roboCa = RoboCacador(random.randint(40, LARGURA - 40), -40, jogador)
        vida_ex = VidaExtra(random.randint(40, LARGURA - 40), -40)
        velo = Velocidade(random.randint(40, LARGURA - 40), -40)
        t_triplo = TiroTriplo(random.randint(40, LARGURA - 40), -40)
        todos_sprites.add(roboC, roboZ, roboL, roboR, roboS, roboCa, vida_ex, velo, t_triplo)
        inimigos.add(roboC, roboZ, roboL, roboR, roboCa, roboS)
        power_up.add(velo, t_triplo, vida_ex)
        spawn_timer = 0

    colisoes = pygame.sprite.groupcollide(inimigos, tiros, False, True)
    for inimigo, lista_tiros in colisoes.items():
        if inimigo.tipo == "chefao":
            inimigo.vida -= len(lista_tiros)
            if inimigo.vida <= 0:
                inimigo.kill()
                chefao_vivo = None
                if chefao_vivo is None:
                    roboChe = RoboChefao(random.randint(200, LARGURA - 40), -100)
                    todos_sprites.add(roboChe)
                    inimigos.add(roboChe)
        else:
            inimigo.kill()
            Sons.som_morte()
            pontos += 1

    colisao_power = pygame.sprite.spritecollide(jogador, power_up, True)
    if colisao_power:
        Sons.som_buff()
        for p in colisao_power:
            if p.tipo == "vida":
                jogador.vida += 1
                if jogador.vida > vida_maxima:
                    vida_maxima += 1
            elif p.tipo == "velocidade":
                jogador.velocidade = 10
                jogador.buff_velocidade_tempo = 5 * FPS
            elif p.tipo == "tiro":
                jogador.tiro_triplo = True
                jogador.buff_tiro_tempo = 5 * FPS

    colisao_inimigo = pygame.sprite.spritecollide(jogador, inimigos, True)
    for inimigo in colisao_inimigo:
        Sons.som_morte()
        jogador.vida -= inimigo.dano
        if jogador.vida <= 0:
            print("GAME OVER!")
            rodando = False

    todos_sprites.update()

    TELA.blit(background, (0, 0))
    todos_sprites.draw(TELA)
    desenhar_coracoes(TELA, jogador.vida, vida_maxima, coracao, coracao_vazio)

    font = pygame.font.SysFont(None, 30)
    texto = font.render(f"Pontos: {pontos}", True, (255, 255, 255))
    TELA.blit(texto, (10, 570))

    pygame.display.flip()

pygame.quit()

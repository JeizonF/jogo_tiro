import pygame
from sons import * 
import random


pygame.init()

LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))

background = pygame.image.load("v6/imagens/background.png")

background = pygame.transform.scale(background, (LARGURA, ALTURA))
pygame.display.set_caption("Robot Defense - Template")
tema = Tema()
morto = False
FPS = 60
clock = pygame.time.Clock()


# CLASSE BASE
class Entidade(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade):
        super().__init__()
        self.velocidade = velocidade
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=(x, y))

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image = pygame.image.load("v6/imagens/naveDoJogo.png") # verde
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

        # limites de tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - 40))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 40))

        if self.buff_tiro_tempo > 0:
            self.buff_tiro_tempo -=1
            if self.buff_tiro_tempo <=0:
                self.tiro_triplo = False
        if self.buff_velocidade_tempo > 0:
            self.buff_velocidade_tempo -=1
            if self.buff_velocidade_tempo <=0:
                self.velocidade = 5
    


# TIRO (DO JOGADOR)
class Tiro(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 15)
        x = x + 44
        self.rect = self.image.get_rect(center=(x, y))
        self.image = pygame.image.load("v6/imagens/tiro.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        Sons.som_tiro()

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()
class Tiro2(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 15)
        x = x + 44
        self.rect = self.image.get_rect(center=(x, y))
        self.image = pygame.image.load("v6/imagens/tiro.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.direcao = 1
    def update(self):
        self.rect.y -= self.velocidade
        self.rect.x += -self.direcao *5
        if self.rect.y < 0:
            self.kill()
class Tiro3(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 15)
        x = x + 44
        self.rect = self.image.get_rect(center=(x, y))
        self.image = pygame.image.load("v6/imagens/tiro.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.direcao = 1

    def update(self):
        self.rect.y -= self.velocidade
        self.rect.x += self.direcao *5
        if self.rect.y < 0:
            
            self.kill()


# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 0, 0))  # vermelho
        self.tipo = "normal"

    def atualizar_posicao(self):
        raise NotImplementedError


# ROBO EXEMPLO — ZigueZague
class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.direcao = 1
        self.image = pygame.image.load("v6/imagens/robo_ziguezague.png")
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
        self.image = pygame.image.load("v6/imagens/robo_saltador.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        

        self.velocidade_y = -3  
        self.gravidade = 0.2 
        self.chao_y = ALTURA - 60 
        self.descida = 1
        self.direcao = 3
        self.bateu = False

    def atualizar_posicao(self):
        
        self.velocidade_y += self.gravidade
        
        self.rect.y += self.velocidade_y
        
        self.rect.y += self.descida
        
        
        # Pro robo pular
        if self.rect.y >= self.chao_y:
            self.rect.y = self.chao_y 
            self.velocidade_y = -10  # pulo
            self.bateu = True

        # Pro robo se movimentar para os lados
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
        self.image = pygame.image.load("v6/imagens/robo_lento.png")
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
        self.image = pygame.image.load("v6/imagens/robo_rapido.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        
        
    def atualizar_posicao(self):
        self.rect.y += self.velocidade * 2

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

class RoboCiclico(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade=3)
        self.image = pygame.image.load("v6/imagens/robo_ciclico.png")
        self.image = pygame.transform.scale(self.image, (70, 70))


        self.etapa = 0          # qual parte do ciclo está (0 a 3)
        self.contador = 0       # quanto já andou dentro de uma etapa
        self.tamanho = 40      
        self.direcao = 3
        

    def atualizar_posicao(self):
    
        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1
            self.rect.x += self.direcao *10
              
        # 0 = direita
        if self.etapa == 0:
            self.rect.x += self.direcao
            self.contador += 1
            if self.contador >= self.tamanho:
                self.etapa = 1
                self.contador = 0
            

        # 1 = baixo
        elif self.etapa == 1:
            self.rect.y += self.velocidade
            self.contador += 1
            if self.contador >= self.tamanho:
                self.etapa = 2
                self.contador = 0

        # 2 = esquerda
        elif self.etapa == 2:
            self.rect.x -= self.direcao
            self.contador += 1
            if self.contador >= self.tamanho:
                self.etapa = 3
                self.contador = 0

        # 3 = cima
        elif self.etapa == 3:
            self.rect.y -= self.velocidade
            self.contador += 1
            if self.contador >= self.tamanho:
                self.etapa = 0
                self.contador = 0

      
        self.rect.y += 1

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

class RoboCacador(Robo):
    def __init__(self, x, y, alvo):
        super().__init__(x, y, velocidade=3)
        self.direcao = 1
        self.image = pygame.image.load("v6/imagens/robo_cacador.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.alvo = alvo
        
        
      

    def atualizar_posicao(self):


            # Se está à esquerda DO JOGADOR por mais de 3px → anda pra direita
        if self.rect.x < self.alvo.rect.x - self.velocidade:
            self.rect.x += self.velocidade

        # Se está à direita DO JOGADOR por mais de 3px → anda pra esquerda
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
        self.image = pygame.image.load("v6/imagens/robo_chefao.png")
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
        self.image = pygame.image.load("v6/imagens/buff cura.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
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
        self.image = pygame.image.load("v6/imagens/buff energia.png")
        self.image = pygame.transform.scale(self.image, (70*2, 70*2))
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
        self.image = pygame.image.load("v6/imagens/buff municao.png")
        self.image = pygame.transform.scale(self.image, (70*2, 70*2))
        self.direcao = 1

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao

        if self.rect.x <= 0 or self.rect.x >= LARGURA - 105:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()

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


coracao = pygame.image.load("v6/imagens/coracao.png")
coracao = pygame.transform.scale(coracao, (32, 32))
coracao_vazio = pygame.image.load("v6/imagens/coracao_vazio.png")
coracao_vazio = pygame.transform.scale(coracao_vazio, (32, 32))
vida_maxima = jogador.vida

def desenhar_coracoes(tela, vida_atual, vida_maxima, cor_cheio, cor_vazio):
    for i in range(vida_maxima):
        x = 10 + i * 40  # posição dos corações

        if i < vida_atual:
            tela.blit(cor_cheio, (x, 10))
        else:
            tela.blit(cor_vazio, (x, 10))





rodando = True
while rodando:
    tema.som_tema()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
                todos_sprites.add(tiro)
                tiros.add(tiro)
                if jogador.tiro_triplo == True:
                     tiro2 = Tiro2(jogador.rect.centerx, jogador.rect.y)
                     tiro3 = Tiro3(jogador.rect.centerx, jogador.rect.y)
                     todos_sprites.add(tiro2,tiro3)
                     tiros.add(tiro2,tiro3)

    # timer de entrada dos inimigos
    spawn_timer += 1
   
    


    if spawn_timer > 400:
        roboZ = RoboZigueZague(random.randint(40, LARGURA - 40), -40)
        roboS = RoboSaltador(random.randint(40, LARGURA - 40), -40)
        roboL = RoboLento(random.randint(40, LARGURA - 40), -40)
        roboR = RoboRapido(random.randint(40, LARGURA - 40), -40)
        roboC = RoboCiclico(random.randint(40, LARGURA - 40), -40)
        roboCa = RoboCacador(random.randint(40, LARGURA - 40), -40, jogador)
        vida_ex = VidaExtra(random.randint(40, LARGURA - 40), -40) 
        velo = Velocidade(random.randint(40, LARGURA - 40), -40)
        t_triplo = TiroTriplo(random.randint(40, LARGURA - 40), -40)
        todos_sprites.add(roboC,roboZ,roboL,roboR,roboS,roboCa,vida_ex,velo,t_triplo)
        inimigos.add(roboC,roboZ,roboL,roboR,roboCa,roboS)
        power_up.add(velo,t_triplo, vida_ex)
        spawn_timer = 0

    # colisão tiro x robô
    
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
                    vida_maxima += 1  # adiciona coracao
            elif p.tipo == "velocidade":
                jogador.velocidade = 10
                jogador.buff_velocidade_tempo = 5 * FPS
            elif p.tipo == "tiro":
                jogador.tiro_triplo = True
                jogador.buff_tiro_tempo = 5 * FPS



    # colisão robô x jogador
    if pygame.sprite.spritecollide(jogador, inimigos, True):
        Sons.som_morte()
        jogador.vida -= 1
        if jogador.vida <= 0:
            print("GAME OVER!")
            rodando = False

    # atualizar
    todos_sprites.update()

    # desenhar
    TELA.blit(background,(0, 0))
    todos_sprites.draw(TELA)

    desenhar_coracoes(TELA, jogador.vida, vida_maxima, coracao, coracao_vazio)



    #Painel de pontos e vida
    font = pygame.font.SysFont(None, 30)
    texto = font.render(f"Pontos: {pontos}", True, (255, 255, 255))
    TELA.blit(texto, (10, 570))

    pygame.display.flip()

pygame.quit()
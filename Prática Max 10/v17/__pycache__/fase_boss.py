import pygame
import os
import random
from sons import Sons, Tema


def Fase_boss(pontos):
    BASE_DIR = os.path.dirname(__file__)
    IMG_DIR = os.path.join(BASE_DIR, "imagens")


    def img(nome):
        return os.path.join(IMG_DIR, nome)


    pygame.init()


    LARGURA = 800
    ALTURA = 600
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Robot Defense - Boss")


    background = pygame.image.load(img("background.png"))
    background = pygame.transform.scale(background, (LARGURA, ALTURA))


    tema = Tema()
    clock = pygame.time.Clock()
    FPS = 60


    class Entidade(pygame.sprite.Sprite):
        def __init__(self, x, y, vel):
            super().__init__()
            self.vel = vel
            self.image = pygame.Surface((10, 10))
            self.rect = self.image.get_rect(center=(x, y))


    class Jogador(Entidade):
        def __init__(self):
            super().__init__(LARGURA//2, ALTURA-60, 5)
            self.image = pygame.image.load(img("naveDoJogo.png"))
            self.image = pygame.transform.scale(self.image, (70, 70))
            self.rect = self.image.get_rect(center=(LARGURA//2, ALTURA-60))
            self.vida = 10
            self.tiro_triplo = False
            self.buff_tiro = 0
            self.buff_vel = 0


        def update(self):
            k = pygame.key.get_pressed()
            if k[pygame.K_a]: self.rect.x -= self.vel
            if k[pygame.K_d]: self.rect.x += self.vel
            if k[pygame.K_w]: self.rect.y -= self.vel
            if k[pygame.K_s]: self.rect.y += self.vel
            self.rect.clamp_ip(TELA.get_rect())


            if self.buff_tiro > 0:
                self.buff_tiro -= 1
                if self.buff_tiro <= 0:
                    self.tiro_triplo = False


            if self.buff_vel > 0:
                self.buff_vel -= 1
                if self.buff_vel <= 0:
                    self.vel = 5


    class Tiro(Entidade):
        def __init__(self, x, y, dx=0):
            super().__init__(x, y, 10)
            self.image = pygame.image.load(img("tiro.png"))
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.rect = self.image.get_rect(center=(x, y))
            self.dx = dx
            Sons.som_tiro()


        def update(self):
            self.rect.y -= self.vel
            self.rect.x += self.dx
            if self.rect.bottom < 0:
                self.kill()


    class TiroBoss(Entidade):  
        def __init__(self, x, y, dx=0):
            super().__init__(x, y, 5)
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 255, 0))  
            pygame.draw.rect(self.image, (255, 200, 0), (0, 0, 20, 20), 2)  
            self.rect = self.image.get_rect(center=(x, y))
            self.dx = dx


        def update(self):
            self.rect.y += self.vel  
            self.rect.x += self.dx
            if self.rect.top > ALTURA:
                self.kill()


    class Boss:
        def __init__(self):
            self.rect = pygame.Rect(100, 40, 600, 80)
            self.vida = 1000  
            self.vida_max = 1000
            self.cooldown = 0
            self.fase = 1  # NOVA: controla a fase do boss


        def atacar(self, tiros_boss_group):
            self.cooldown += 1
            
            # Verifica se deve ativar fase 2
            if self.vida <= 500 and self.fase == 1:
                self.fase = 2
            
            if self.fase == 1:
                cooldown_max = 60  # Fase 1: normal
                if self.cooldown > cooldown_max:
                    centro_x = self.rect.centerx
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom))          # Central
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom, -4))      # Esq 1
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom, -2))      # Esq 2
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom, 2))       # Dir 1
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom, 4))       # Dir 2
                    self.cooldown = 0
            else:  # Fase 2: mais difícil
                cooldown_max = 30  # Aumenta frequência (2x mais rápido)
                if self.cooldown > cooldown_max:
                    centro_x = self.rect.centerx
                    # 7 tiros: 5 originais + 2 extras nas bordas
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom))          # Central
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom, -4))      # Esq 1
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom, -2))      # Esq 2
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom, 2))       # Dir 1
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom, 4))       # Dir 2
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom, -6))      # Esq extra
                    tiros_boss_group.add(TiroBoss(centro_x, self.rect.bottom, 6))       # Dir extra
                    self.cooldown = 0


        def desenhar(self):
            cor = (200, 0, 0) if self.fase == 1 else (255, 100, 0)  # Vermelho -> Laranja na fase 2
            pygame.draw.rect(TELA, cor, self.rect)
            
            barra_largura = 600
            barra_altura = 15
            barra_x = 100
            barra_y = self.rect.bottom + 5
            
            pygame.draw.rect(TELA, (100, 100, 100), (barra_x, barra_y, barra_largura, barra_altura))
            
            vida_percent = self.vida / self.vida_max
            cor_vida = (0, 255, 0) if vida_percent > 0.5 else (255, 255, 0) if vida_percent > 0.25 else (255, 0, 0)
            largura_vida = int(barra_largura * vida_percent)
            pygame.draw.rect(TELA, cor_vida, (barra_x, barra_y, largura_vida, barra_altura))
            
            pygame.draw.rect(TELA, (255, 255, 255), (barra_x, barra_y, barra_largura, barra_altura), 2)
            
            font = pygame.font.SysFont(None, 24)
            texto_vida = font.render(f"BOSS: {self.vida}/1000", True, (255, 255, 255))
            TELA.blit(texto_vida, (barra_x + 10, barra_y - 25))


    class VidaExtra(Entidade):
        def __init__(self, x, y):
            super().__init__(x, y, 3)
            self.tipo = "vida"
            self.image = pygame.image.load(img("buff cura.png"))
            self.image = pygame.transform.scale(self.image, (80, 80))


        def update(self):
            self.rect.y += self.vel
            if self.rect.top > ALTURA:
                self.kill()


    class Velocidade(Entidade):
        def __init__(self, x, y):
            super().__init__(x, y, 3)
            self.tipo = "velocidade"
            self.image = pygame.image.load(img("buff energia.png"))
            self.image = pygame.transform.scale(self.image, (80, 80))


        def update(self):
            self.rect.y += self.vel
            if self.rect.top > ALTURA:
                self.kill()


    class TiroTriploBuff(Entidade):
        def __init__(self, x, y):
            super().__init__(x, y, 3)
            self.tipo = "tiro"
            self.image = pygame.image.load(img("buff municao.png"))
            self.image = pygame.transform.scale(self.image, (80, 80))


        def update(self):
            self.rect.y += self.vel
            if self.rect.top > ALTURA:
                self.kill()


    jogador = Jogador()
    boss = Boss()


    todos_sprites = pygame.sprite.Group(jogador)
    tiros = pygame.sprite.Group()
    tiros_boss = pygame.sprite.Group()
    power_up = pygame.sprite.Group()


    coracao = pygame.image.load(img("coracao.png"))
    coracao = pygame.transform.scale(coracao, (32, 32))
    coracao_vazio = pygame.image.load(img("coracao_vazio.png"))
    coracao_vazio = pygame.transform.scale(coracao_vazio, (32, 32))


    def desenhar_coracoes():
        for i in range(10):
            x = 10 + i * 40
            if i < jogador.vida:
                TELA.blit(coracao, (x, 10))
            else:
                TELA.blit(coracao_vazio, (x, 10))


    rodando = True
    while rodando:
        tema.som_tema()
        clock.tick(FPS)


        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    tiro = Tiro(jogador.rect.centerx, jogador.rect.top)
                    tiros.add(tiro)
                    todos_sprites.add(tiro)


                    if jogador.tiro_triplo:
                        tiros.add(
                            Tiro(jogador.rect.centerx, jogador.rect.top, -5),
                            Tiro(jogador.rect.centerx, jogador.rect.top, 5)
                        )
                        todos_sprites.add(tiros.sprites()[-3:])


        boss.atacar(tiros_boss)
        tiros_boss.update()


        for t in tiros_boss:
            if t.rect.colliderect(jogador.rect):
                jogador.vida -= 1
                t.kill()


        buffs_coletados = pygame.sprite.spritecollide(jogador, power_up, True)
        for buff in buffs_coletados:
            if buff.tipo == "vida" and jogador.vida < 10:
                jogador.vida += 1
            elif buff.tipo == "velocidade":
                jogador.vel = 8
                jogador.buff_vel = 600
            elif buff.tipo == "tiro":
                jogador.tiro_triplo = True
                jogador.buff_tiro = 600


        todos_sprites.update()


        for t in pygame.sprite.spritecollide(boss, tiros, True):
            boss.vida -= 1


        if boss.vida <= 0 or jogador.vida <= 0:
            rodando = False


        if random.randint(1, 400) == 1:
            buff = random.choice([
                VidaExtra(random.randint(40, LARGURA-40), -40),
                Velocidade(random.randint(40, LARGURA-40), -40),
                TiroTriploBuff(random.randint(40, LARGURA-40), -40)
            ])
            power_up.add(buff)
            todos_sprites.add(buff)


        TELA.blit(background, (0, 0))
        todos_sprites.draw(TELA)
        tiros_boss.draw(TELA)
        boss.desenhar()
        desenhar_coracoes()
        pygame.display.flip()


    pygame.quit()
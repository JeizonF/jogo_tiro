import pygame
class Sons():
  def som_morte():
    morte = pygame.mixer.Sound('v4/sounds/inimorrendo.mp3')
    morte.set_volume(1.0)
    morte.play()

  def som_buff():
    buff = pygame.mixer.Sound('v4/sounds/pegandobuff.mp3')
    buff.set_volume(1.0)
    buff.play()

  def som_tiro():
    tiro = pygame.mixer.Sound('v4/sounds/tiropadrao.mp3')
    tiro.set_volume(1.0)
    tiro.play()
    
class Tema:
    def __init__(self):
        pygame.mixer.music.load("v4/sounds/musica.mp3")
        pygame.mixer.music.set_volume(0.8)
    def som_tema(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
import pygame
import os

BASE_DIR = os.path.dirname(__file__)
SND_DIR = os.path.join(BASE_DIR, "sounds")

class Sons:
    @staticmethod
    def som_morte():
        morte = pygame.mixer.Sound(os.path.join(SND_DIR, "inimorrendo.mp3"))
        morte.set_volume(1.0)
        morte.play()

    @staticmethod
    def som_buff():
        buff = pygame.mixer.Sound(os.path.join(SND_DIR, "pegandobuff.mp3"))
        buff.set_volume(1.0)
        buff.play()

    @staticmethod
    def som_tiro():
        tiro = pygame.mixer.Sound(os.path.join(SND_DIR, "tiropadrao.mp3"))
        tiro.set_volume(1.0)
        tiro.play()


class Tema:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(SND_DIR, "musica.mp3"))
        pygame.mixer.music.set_volume(0.8)

    def som_tema(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

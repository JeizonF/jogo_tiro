from inicio import mostrar_inicio
from jogo_tiro import jogo
from fase_boss import Fase_boss

def main():
    mostrar_inicio()
    pontos = jogo()
    Fase_boss(pontos)

if __name__ == '__main__':
    main()

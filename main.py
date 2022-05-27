import numpy as np
import random
import pygame
from pygame.locals import *  # Importando random,pygame e numpy, pacotes que são necessários para o jogo.

from constants import CP  # Constants é um arquivo que pegamos na internet só para gerar as cores de fundo.

N = 4  # Definindo N que será o lado do grid


class Py2048:
    def __init__(self):
        self.grid = np.zeros((N, N), dtype=int)  # Inicia um grid com zeros

        self.W = 400  # tamanho em pixels da largura
        self.H = self.W  # tamanho em pixels da altura = largura , ou seja a janela será um quadrado
        self.SPACING = 10

        pygame.init()  # inicia o pygame
        pygame.display.set_caption("2048")  # Nomeia a janela com 2048

        pygame.font.init()  # Inicia a fonte que será usada
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)  # Define a fonte

        self.screen = pygame.display.set_mode((self.W, self.H))  # Define a escala da tela = W*H

    def __str__(self):
        return str(self.grid)  # Gera o grid

    def new_number(self, k=1):  # Define com 'k' a quantidade de novos números que surgirão a cada rodada
        free_poss = list(
            zip(*np.where(self.grid == 0)))  # define que só gerará números novos quando houver 0 na posição
        for pos in random.sample(free_poss, k=k):
            if random.random() < .1:
                self.grid[pos] = 4  # Define 10% de chance de gerar um 4
            else:
                self.grid[pos] = 2  # Define 90% de chance de gerar um 2

    @staticmethod
    def _get_nums(this):  # Todo esse objeto é para calcular o novo valor do número quando se encontrarem
        this_n = this[this != 0]
        this_n_sum = []
        skip = False
        for j in range(len(this_n)):
            if skip:
                skip = False
                continue
            if j != len(this_n) - 1 and this_n[j] == this_n[j + 1]:
                new_n = this_n[j] * 2
                skip = True
            else:
                new_n = this_n[j]

            this_n_sum.append(new_n)
        return np.array(this_n_sum)

    def make_move(self, move):  # Este objeto define os comandos que moverão o tabuleiro
        for i in range(N):
            if move in 'lr':
                this = self.grid[i, :]
            else:
                this = self.grid[:, i]

            flipped = False
            if move in 'rd':
                flipped = True
                this = this[::-1]

            this_n = self._get_nums(this)

            new_this = np.zeros_like(this)
            new_this[:len(this_n)] = this_n

            if flipped:
                new_this = new_this[::-1]

            if move in 'lr':
                self.grid[i, :] = new_this
            else:
                self.grid[:, i] = new_this

    def draw_game(self):  # Objeto que define como será renderizado o jogo, utilizando das cores do CP
        self.screen.fill(CP['back'])

        for i in range(N):  # Essa condição gera os espacamentos entre os blocos e os textos(Numeros)
            for j in range(N):
                n = self.grid[i][j]

                rect_x = j * self.W // N + self.SPACING
                rect_y = i * self.H // N + self.SPACING
                rect_w = self.W // N - 2 * self.SPACING
                rect_h = self.H // N - 2 * self.SPACING

                pygame.draw.rect(self.screen, CP[n], pygame.Rect(rect_x, rect_y, rect_w, rect_h), border_radius=8)
                if n == 0:
                    continue
                text_surface = self.myfont.render(f'{n}', True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(rect_x + rect_w / 2, rect_y + rect_h / 2))
                self.screen.blit(text_surface, text_rect)

    @staticmethod
    def wait_for_key():  # Recebe os comando das Setas do teclado e transforma em comandos de direção definidos anteriormente(Q,U,L,D e R )
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'q'
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        return 'u'
                    elif event.key == K_RIGHT:
                        return 'r'
                    elif event.key == K_LEFT:
                        return 'l'
                    elif event.key == K_DOWN:
                        return 'd'
                    elif event.key == K_q or event.key == K_ESCAPE:
                        return 'q'

    def game_over(self):  # Atualiza o grid quando um comando é inserido
        grid_bu = self.grid.copy()
        for move in 'lrud':
            self.make_move(move)
            if not all((self.grid == grid_bu).flatten()):
                self.grid = grid_bu
                return False
        return True

    def play(self):  # Define o jogo, Iniciando com 2 números em posições aleatórias no grid
        self.new_number(k=2)

        while True:
            self.draw_game()
            pygame.display.flip()
            cmd = self.wait_for_key()
            if cmd == 'q':
                break

            old_grid = self.grid.copy()
            self.make_move(cmd)
            print(game.grid)
            if self.game_over():
                print('Sua pontuação foi de:',self.grid.sum())
                print('GAME OVER!')
                break

            if not all((self.grid == old_grid).flatten()):
                self.new_number()


if __name__ == '__main__':  # Inicia o pygame.
    game = Py2048()
    game.play()

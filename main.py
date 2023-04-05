import numpy as np
import pygame


class Cube:

    def __init__(self, d=1):
        # Variáveis iniciais
        self.WIDTH = 600
        self.LENGTH = 600
        self.FPS = 60

        # Inicializa os itens do pygame
        pygame.display.set_mode((self.WIDTH, self.LENGTH))
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        # Inicializa a matriz de projeção inicial
        self.d = d
        self.projection_matrix = np.array([[1, 0, 0, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 0, -self.d],
                                            [0, 0, -1/self.d, 0]])


    def rotation_matrix(self, angle, type='x'):
        '''
        A função recebe um ângulo e um tipo de rotação (x, y ou z) e retorna a matriz de rotação correspondente

        Parâmetros
        ----------
        angle - ângulo de rotação em graus
        type : str - tipo de rotação (x, y ou z)

        Retorno: array numpy
        '''
        import math
        angle = math.radians(angle)
        
        if type == 'x':
            R = np.array([[1, 0, 0, 0],
                          [0, math.cos(angle), -math.sin(angle), 0],
                          [0, math.sin(angle), math.cos(angle), 0],
                          [0, 0, 0, 1]])
        elif type == 'y':
            R = np.array([[math.cos(angle), 0, math.sin(angle), 0],
                          [0, 1, 0, 0],
                          [-math.sin(angle), 0, math.cos(angle), 0],
                          [0, 0, 0, 1]])
        elif type == 'z':
            R = np.array([[math.cos(angle), -math.sin(angle), 0, 0],
                          [math.sin(angle), math.cos(angle), 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

        return R


    def play(self):

        # Linha 1 -> todos os X
        # Linha 2 -> todos os y
        # Linha 3 -> todos os z
        # Linha 4 -> 1
        cube = np.array([[1, 1, -1, -1, 1, 1, -1, -1], 
                         [1, -1, -1, 1, 1, -1, -1, 1],
                         [-1, -1, -1, -1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1]])

        angle_x = 0
        angle_y = 0
        angle_z = 0
        rodando = True
        spin = False

        # Loop pygame
        while rodando:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.d += 0.08
                        self.projection_matrix = np.array([[1, 0, 0, 0],
                                                            [0, 1, 0, 0],
                                                            [0, 0, 0, -self.d],
                                                            [0, 0, -1/self.d, 0]])
                    elif event.button == 5:
                        if self.d > 0.08:
                            self.d -= 0.08
                        self.projection_matrix = np.array([[1, 0, 0, 0],
                                                            [0, 1, 0, 0],
                                                            [0, 0, 0, -self.d],
                                                            [0, 0, -1/self.d, 0]])
                        
            keys = pygame.key.get_pressed()

            # Controle do cubo
            # Rotação manual só funciona se a rotação automática (spin: bool) estiver desligada
            if keys[pygame.K_q] and not spin: # Tecla Q começa a rotação automatica
                spin = True
            if keys[pygame.K_t] and spin: # Tecla T termina a rotação automatica
                spin = False
            if keys[pygame.K_a] and not spin: # Tecla A rotação no eixo Y negativa
                angle_y -= 1
            if keys[pygame.K_d] and not spin: # Tecla D rotação no eixo Y positiva
                angle_y += 1
            if keys[pygame.K_s] and not spin: # Tecla S rotação no eixo X negativa
                angle_x -= 1
            if keys[pygame.K_w] and not spin: # Tecla W rotação no eixo X positiva
                angle_x += 1
            if keys[pygame.K_z] and not spin: # Tecla Z rotação no eixo Z negativa
                angle_z -= 1
            if keys[pygame.K_x] and not spin: # Tecla X rotação no eixo Z positiva
                angle_z += 1
            if keys[pygame.K_r]: # Tecla R reseta a rotação do cubo
                self.d = 1
                self.projection_matrix = np.array([[1, 0, 0, 0],
                                        [0, 1, 0, 0],
                                        [0, 0, 0, -self.d],
                                        [0, 0, -1/self.d, 0]])
                cube_ = cube
                spin = False
                angle_x = 0
                angle_y = 0
                angle_z = 0

            if spin: # Rotação automática em todas as direções
                angle_x += 1
                angle_y += 1
                angle_z += 1
            
            self.clock.tick(self.FPS)


            # Rotaciona o cubo
            R_x = self.rotation_matrix(angle_x, 'x')
            R_y = self.rotation_matrix(angle_y, 'y')
            R_z = self.rotation_matrix(angle_z, 'z')

            cube_ = R_z @ R_y @ R_x @ cube
            
            # Translada o cubo na direção z, pois a sua coordenada não pode ser 0 para a projeção, já que ali se encontra o pin hole
            cube_[2] = cube_[2] + 5

            # Faz a projeção
            cube_projection = self.projection_matrix @ cube_

            # Normaliza (elimina o 4º elemento)
            cube_projection = cube_projection / cube_projection[3]

            # Pega as coordenadas x e y
            cube_projection = cube_projection[:2]
            cube_projection = np.vstack((cube_projection, np.ones((1, cube_projection.shape[1]))))

            # Aumenta o cubo em 400x para ficar visível
            E = np.array([[400, 0, 0],
                          [0, 400, 0],
                          [0, 0, 1]])
            
            cube_projection = E @ cube_projection

            # Transporta a origem para o centro da tela
            T = np.array([[1, 0, self.WIDTH/2],
                          [0, 1, self.LENGTH/2],
                          [0, 0, 1]])
            
            cube_projection = T @ cube_projection

            # Gera as coordeandas como linha para serem plotadas
            coordinates = cube_projection.T
            
            # Pinta a tela de preto
            self.screen.fill((0, 0, 0))

            # Desenha os vertices
            for line in coordinates:
                if line[0] > 0 and line[1] > 0:
                    pygame.draw.circle(self.screen, (255, 255, 255), (int(line[0]), int(line[1])), 5)
            
            # As 4 primeiras coordenadas são os vértices de um quadrado, conectando com linhas
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[0][0]), int(coordinates[0][1])), (int(coordinates[1][0]), int(coordinates[1][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[1][0]), int(coordinates[1][1])), (int(coordinates[2][0]), int(coordinates[2][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[2][0]), int(coordinates[2][1])), (int(coordinates[3][0]), int(coordinates[3][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[3][0]), int(coordinates[3][1])), (int(coordinates[0][0]), int(coordinates[0][1])), 3)

            # As 4 últimas coordenadas são os vértices de um quadrado, conectando com linhas
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[4][0]), int(coordinates[4][1])), (int(coordinates[5][0]), int(coordinates[5][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[5][0]), int(coordinates[5][1])), (int(coordinates[6][0]), int(coordinates[6][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[6][0]), int(coordinates[6][1])), (int(coordinates[7][0]), int(coordinates[7][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[7][0]), int(coordinates[7][1])), (int(coordinates[4][0]), int(coordinates[4][1])), 3)

            # Connect the vertices of the first square with the vertices of the second square
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[0][0]), int(coordinates[0][1])), (int(coordinates[4][0]), int(coordinates[4][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[1][0]), int(coordinates[1][1])), (int(coordinates[5][0]), int(coordinates[5][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[2][0]), int(coordinates[2][1])), (int(coordinates[6][0]), int(coordinates[6][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[3][0]), int(coordinates[3][1])), (int(coordinates[7][0]), int(coordinates[7][1])), 3)
            


            pygame.display.update()


        quit()

    def quit():
        pygame.quit()
    


if __name__ == '__main__':
    game = Cube()
    game.play()
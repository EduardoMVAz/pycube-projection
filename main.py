import numpy as np
import pygame


class Cube:

    def __init__(self, d=-1):
        self.WIDTH = 600
        self.LENGTH = 600
        self.FPS = 60

        pygame.display.set_mode((self.WIDTH, self.LENGTH))
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.d = d
        self.projection_matrix = np.array([[1, 0, 0, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 0, -self.d],
                                            [0, 0, -1/self.d, 0]])


    def rotation_matrix(self, angle, type='x'):
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
        while rodando:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    angle_y += 1
                if keys[pygame.K_d]:
                    angle_y -= 1
                if keys[pygame.K_w]:
                    angle_x -= 1
                if keys[pygame.K_s]:
                    angle_x += 1
                if keys[pygame.K_h]:
                    angle_z += 1
                if keys[pygame.K_t]:
                    angle_z -= 1
                if keys[pygame.K_f]:
                    self.d -= 0.01
                    self.projection_matrix = np.array([[1, 0, 0, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 0, -self.d],
                                            [0, 0, -1/self.d, 0]])
                if keys[pygame.K_r]:
                    self.d = -1
                    self.projection_matrix = np.array([[1, 0, 0, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 0, -self.d],
                                            [0, 0, -1/self.d, 0]])
                    cube_ = cube
                    angle_x = 0
                    angle_y = 0
                    angle_z = 0
            
            self.clock.tick(self.FPS)


            # Rotaciona o cubo
            R_x = self.rotation_matrix(angle_x, 'x')
            R_y = self.rotation_matrix(angle_y, 'y')
            R_z = self.rotation_matrix(angle_z, 'z')

            cube_ = R_z @ R_y @ R_x @ cube

            cube_[2] = cube_[2] + 5

            # Faz a projeção
            cube_projection = self.projection_matrix @ cube_

            # Normaliza (elimina o 4º elemento)
            cube_projection = cube_projection / cube_projection[3]

            # Multiplica as coordenadas por 400
            cube_projection = cube_projection * 400

            # Transporta a origem para o centro da tela
            cube_projection[0] = cube_projection[0] + self.WIDTH/2
            cube_projection[1] = cube_projection[1] + self.LENGTH/2

            coordinates = cube_projection.T

            # Draw
            self.screen.fill((0, 0, 0))

            # Vertices
            for line in coordinates:
                pygame.draw.circle(self.screen, (255, 255, 255), (int(line[0]), int(line[1])), 5)
            
            # The first 4 coordinates are the vertices of a square, connect them with lines
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[0][0]), int(coordinates[0][1])), (int(coordinates[1][0]), int(coordinates[1][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[1][0]), int(coordinates[1][1])), (int(coordinates[2][0]), int(coordinates[2][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[2][0]), int(coordinates[2][1])), (int(coordinates[3][0]), int(coordinates[3][1])), 3)
            pygame.draw.line(self.screen, (255, 255, 255), (int(coordinates[3][0]), int(coordinates[3][1])), (int(coordinates[0][0]), int(coordinates[0][1])), 3)

            # The last 4 coordinates are the vertices of a square, connect them with lines
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
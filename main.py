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
                                            [0, 0, 0, -d],
                                            [0, 0, -1/d, 0]])

    def play(self):
        '''
        (200, 200, 200) (200, 400, 200) (400, 200, 200) (400, 400, 200)
        (200, 200, 400) (200, 400, 400) (400, 200, 400) (400, 400, 400)
        '''

        # Linha 1 -> todos os X
        # Linha 2 -> todos os y
        # Linha 3 -> todos os z
        # Linha 4 -> 1
        cube = np.array([[200, 200, 400, 400, 200, 200, 400, 400], 
                         [200, 400, 200, 400, 200, 400, 200, 400],
                         [200, 200, 200, 200, 400, 400, 400, 400],
                         [1, 1, 1, 1, 1, 1, 1, 1]])

        rodando = True
        while rodando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    rodando = False
            
            self.clock.tick(self.FPS)

            # Transformações

            cube_projection = self.projection_matrix @ cube

            # Draw
            self.screen.fill((0, 0, 0))

            # Vertices
            for line in cube_projection.T:
                pygame.draw.circle(self.screen, (255, 255, 255), (int(line[0]/line[3]), int(line[1]/line[3])), 5)
            
            # Lines


        


        quit()


    def quit():
        pygame.quit()
    


if __name__ == '__main__':
    game = Cube()
    game.play()
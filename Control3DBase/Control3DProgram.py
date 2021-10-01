
# from OpenGL.GL import *
# from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(5.0, 5.0, 5.0), Point(0,0,0), Vector(0,1,0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.projection_matrix = ProjectionMatrix()
        #self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.fov = pi / 2
        self.projection_matrix.set_perspective(pi / 2, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.W_key_down = False
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False
        self.T_key_down = False
        self.G_key_down = False
        self.UP_key_down = False
        self.DOWN_key_down = False
        self.RIGHT_key_down = False
        self.LEFT_key_down = False

        self.white_background = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        # if angle > 2 * pi:
        #     angle -= (2 * pi)
        """if self.W_key_down:
            self.view_matrix.pitch(-pi * delta_time)
        if self.S_key_down:
            self.view_matrix.pitch(pi * delta_time)"""
        if self.A_key_down:
            #self.view_matrix.roll(pi * delta_time)
            self.view_matrix.yaw(-pi*delta_time)
        if self.D_key_down:
            #self.view_matrix.slide(1 * delta_time, 0, 0)
            #self.view_matrix.roll(-pi * delta_time)
            self.view_matrix.yaw(pi * delta_time)
        if self.T_key_down:
            self.fov -= 0.25 * delta_time
        if self.G_key_down:
            self.fov += 0.25 * delta_time
        if self.UP_key_down:
            self.view_matrix.slide(0, 0, -3 * delta_time)
        if self.DOWN_key_down:
            self.view_matrix.slide(0, 0, 3 * delta_time)
        if self.RIGHT_key_down:
            self.view_matrix.slide(3 * delta_time, 0, 0)
        if self.LEFT_key_down:
            self.view_matrix.slide(-3 * delta_time, 0, 0)
        else:
            self.white_background = False



    def display(self):
        glEnable(GL_DEPTH_TEST)

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.01, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 1.0, 1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.0, 0.0, -3.0)
        #self.model_matrix.add_rotate_x(self.angle * 0.4)
        #self.model_matrix.add_rotate_y(self.angle * 0.2453)
        self.model_matrix.add_scale(50.0, 1.0, 50.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        """self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 1.0, 1.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.0, 3.5, -3.0)
        #self.model_matrix.add_rotate_x(self.angle * 0.4)
        #self.model_matrix.add_rotate_y(self.angle * 0.2453)
        self.model_matrix.add_scale(50.0, 2.5, 50.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()"""

        #RIGHT BOX WALL
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(15.0, 1.0, 1.0)
        self.model_matrix.add_scale(0.2, 1.0, 8.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        #LEFT BOX WALL
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(5.0, 1.0, 1.0)
        self.model_matrix.add_scale(0.2, 1.0, 8.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        #LOWER BOX WALL
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.9, 1.0, 5.0)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(0.2, 1.0, 8.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(14.5, 1.0, 5.0)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(0.2, 1.0, 1.2)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        #UPPER BOX WALL
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(11.1, 1.0, -3.1)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(0.2, 1, 8.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(5.4, 1.0, -3.1)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(0.2, 1.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        #UPPER LEFT WALLS IN MAZE
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(6.5, 1.0, -1.5)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(0.2, 1.0, 3.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(6.0, 1.0, 1.4)
        self.model_matrix.add_scale(0.2, 1.0, 4.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()



        #LOWER LEFT CORNER WALL
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(5.8, 1.0, 4.0)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(0.2, 1.0, 1.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        #LOWER BOX WALL
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(7.4, 1.0, 4.0)
        self.model_matrix.add_scale(0.2, 1.0, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        #LOWER BOX WALL
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(10.5, 1.0, 3.1)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(0.2, 1.0, 6.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        #LOWER BOX WALL
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(11.2, 1.0, 4.1)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(0.2, 1.0, 5.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        #LOWER BOX WALL
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(14.0, 1.0, 4.5)
        self.model_matrix.add_scale(0.2, 1.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        #UPPER RIGHT CORNER WALLS
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(14.5, 1.0, -0.5)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(0.2, 1.0, 0.8)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(14.0, 1.0, 0.2)
        self.model_matrix.add_scale(0.2, 1.0, 4.3)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(12.5, 1.0, 2.3)
        self.model_matrix.add_rotate_y(pi / 2)
        self.model_matrix.add_scale(0.2, 1.0, 3.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        #CENTER WALLS
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(10.0, 1.0, 2.7)
        self.model_matrix.add_scale(0.2, 1.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        self.shader.set_solid_color(1.0, 0.5, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.7, 1.0, 2.3)
        self.model_matrix.add_rotate_y(pi / 2)
        self.model_matrix.add_scale(0.2, 1.0, 2.5)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()









        '''self.shader.set_solid_color(1.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_rotate_z(self.angle)
        self.model_matrix.add_rotate_y(self.angle)
        self.model_matrix.add_rotate_x(self.angle)
        self.cube.set_verticies(self.shader)'''
        '''for y in range(5):
            for x in range(5):
                for z in range(5):
                    self.shader.set_solid_color(1.0, 0.0, 1.0)
                    self.model_matrix.push_matrix()
                    self.model_matrix.add_translation(-5+x, -5+y,
                                                      0.0-z)  ### --- ADD PROPER TRANSFORMATION OPERATIONS --- ###
                    self.model_matrix.add_scale(0.8, 0.8, 0.8)
                    self.shader.set_model_matrix(self.model_matrix.matrix)
                    self.cube.draw()
                    self.model_matrix.pop_matrix()'''

        #self.model_matrix.pop_matrix()

        pygame.display.flip()

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True

                    if event.key == K_UP:
                        self.UP_key_down = True

                    if event.key == K_DOWN:
                        self.DOWN_key_down = True

                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = True

                    if event.key == K_LEFT:
                        self.LEFT_key_down = True
                        
                    if event.key == K_w:
                        self.W_key_down = True

                    if event.key == K_s:
                        self.S_key_down = True

                    if event.key == K_a:
                        self.A_key_down = True

                    if event.key == K_d:
                        self.D_key_down = True

                    if event.key == K_t:
                        self.T_key_down = True

                    if event.key == K_g:
                        self.G_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False

                    if event.key == K_DOWN:
                        self.DOWN_key_down = False

                    if event.key == K_RIGHT:
                        self.RIGHT_key_down = False

                    if event.key == K_LEFT:
                        self.LEFT_key_down = False

                    if event.key == K_w:
                        self.W_key_down = False

                    if event.key == K_s:
                        self.S_key_down = False

                    if event.key == K_a:
                        self.A_key_down = False

                    if event.key == K_d:
                        self.D_key_down = False

                    if event.key == K_t:
                        self.T_key_down = False

                    if event.key == K_g:
                        self.G_key_down = False

            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()
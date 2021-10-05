
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import pygame
from pygame.locals import *

import sys
import time

from gameobjects import *
from Shaders import *
from Matrices import *

class GraphicsProgram3D:
    def __init__(self):
        pygame.font.init()
        pygame.init()
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()
        self.walls = None
        self.walls_by_x = [
        ]
        self.walls_by_z = []
        self.lvl = 1
        self.model_matrix = ModelMatrix()
        self.player = None
        self.font = pygame.font.SysFont('BubbleShine.ttf', 70)
        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(7, 1, 3.5), Point(10, 1.0, 0), Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.crash_sound = pygame.mixer.Sound("sounds/scream.wav")
        self.lvlup_sound = pygame.mixer.Sound("sounds/lvlcomplete.wav")
        self.soundtrack_sound = pygame.mixer.Sound("sounds/soundtrack.wav")
        #self.shader.set_diffuse_texture(0)
        self.tex_id_wall_diffuse = self.load_texture("./textures/wall1.png")
        self.tex_id_skybox = self.load_texture("./textures/skybox.png")
        self.tex_id_left = self.load_texture("./textures/left.png")
        self.tex_id_right = self.load_texture("./textures/right.png")
        self.tex_id_back = self.load_texture("./textures/back.png")
        self.tex_id_mountains = self.load_texture("./textures/mountains.png")
        self.tex_id_player = self.load_texture("./textures/player.png")
        #self.update_bounding_box()
        self.projection_matrix = ProjectionMatrix()
        #self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.fov = pi / 2
        self.projection_matrix.set_perspective(pi / 2, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.t = 108
        self.cube = Cube()
        self.scale = Point(1, 1, 1)
        self.radius = self.scale.x/2
        self.direction = None
        self.clock = pygame.time.Clock()
        self.textX1 = 30
        self.textY1 = 500
        self.timer = 0
        self.clock.tick()
        self.wall_list = [
            #[10.0, 0.0, 2.0, 10.0, 1.0, 10.0, False],
            [15.0, 1.0, 1.0, 0.2, 1.0, 8.0, False],
            [5.0, 1.0, 1.0, 0.2, 1.0, 8.0, False],
            [8.9, 1.0, 5.0, 0.2, 1.0, 8.0, True],
            [14.5, 1.0, 5.0, 0.2, 1.0, 1.2, True],
            [11.1, 1.0, -3.1, 0.2, 1, 8.0, True],
            [5.4, 1.0, -3.1, 0.2, 1.0, 1.0, True],
            [8.0, 1.0, -1.5, 0.2, 1.0, 6.0, True],
            [6.0, 1.0, 1.4, 0.2, 1.0, 4.0, False],
            [5.8, 1.0, 4.0, 0.2, 1.0, 1.5, True],
            [7.4, 1.0, 4.0, 0.2, 1.0, 2.0, False],
            [10.5, 1.0, 3.1, 0.2, 1.0, 6.5, True],
            [11.2, 1.0, 4.1, 0.2, 1.0, 5.5, True],
            [14.0, 1.0, 4.5, 0.2, 1.0, 1.0, False],
            [13.2, 1.0, -0.8, 0.2, 1.0, 4.5, False],
            [10.2, 1.0, 1.4, 0.2, 1.0, 6.0, True],
            [12.0, 1.0, -0.2, 0.2, 1.0, 3.0, False],
            [7.3, 1.0, 0.4, 0.2, 1.0, 1.9, False],
            [8.3, 1.0, -0.6, 0.2, 1.0, 2.0, False],
            [10.9, 1.0, -0.6, 0.2, 1.0, 2.0, False],
            [6.7, 1.0, -0.5, 0.2, 1.0, 1.4, True],
            [9.6, 1.0, 0.5, 0.2, 1.0, 2.8, True],
            [14.0, 1.0, 0.2, 0.2, 1.0, 4.3, False],
            [13.0, 1.0, 2.3, 0.2, 1.0, 3.8, True],
            [10.0, 1.0, 2.7, 0.2, 1.0, 1.0, False],
            [8.7, 1.0, 2.3, 0.2, 1.0, 2.5, True],
            #[6.6, 1.0, -5.1, 0.2, 1.0, 1.123, True],
        ]
        self.wall_list2 = [
            #[8.1, 0.0, 0.0, 4.0, 1.0, 7.0, False],
            [10.0, 1.0, 1.0, 0.2, 1.0, 4.0, False],
            [6.2, 1.0, 1.0, 0.2, 1.0, 4.0, False],
            [6.8, 1.0, 3.0, 0.2, 1.0, 1.0, True],
            [9.0, 1.0, 3.0, 0.2, 1.0, 2.0, True],
            [7.2, 1.0, -1.0, 0.2, 1, 2.0, True],
            [9.5, 1.0, -1.0, 0.2, 1, 1.0, True],
            [9.15, 1.0, -0.0, 0.2, 1.0, 0.5, True],
            [7.2, 1.0, -0.0, 0.2, 1, 2.0, True],
            [9.0, 1.0, -0.5, 0.2, 1, 0.8, False],
            [8.75, 1.0, 1.0, 0.2, 1.0, 1.3, True],
            [8.1, 1.0, 0.6, 0.2, 1, 1.0, False],
            [6.8, 1.0, 2.0, 0.2, 1.0, 1.0, True],
            [7.2, 1.0, 1.5, 0.2, 1, 1.0, False],
            [8.6, 1.0, 2.0, 0.2, 1.0, 1.3, True],
            [8.1, 1.0, 2.6, 0.2, 1, 1.0, False],

        ]
        self.wall_pos = []
        self.angle = 0
        self.collisionNormal = False
        self.collisionAngle = False
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
        self.falling = False
        self.white_background = False
        self.check_if_won()
        self.check_if_died()
        #self.countdown()
        self.collison_check()
        self.wall_min_x = None
        self.wall_max_x = None
        self.wall_max_z = None
        self.wall_min_z = None
        self.ang_wall_min_x = None
        self.ang_wall_max_x = None
        self.ang_wall_max_z = None
        self.ang_wall_min_z = None

    def check_if_won(self):
        if self.view_matrix.eye.x >= 8.0 and self.view_matrix.eye.x <= 9 and self.view_matrix.eye.z <= -0.9 and self.view_matrix.eye.z >= -1.1 and self.lvl ==1:
            self.lvl = 2
            pygame.mixer.Sound.play(self.lvlup_sound)
            self.view_matrix.look(Point(8, 1, 5.5), Point(0, 1.0, 0), Vector(0, 1, 0))
            print("You solved the maze!")


        if self.view_matrix.eye.x >= 6.0 and self.view_matrix.eye.x <= 8 and self.view_matrix.eye.z <= -2.5 and self.view_matrix.eye.z >= -4.0 and self.lvl == 2:
            pygame.quit()
            quit()

    def check_if_died(self):
        if (self.view_matrix.eye.x >= 10.0 and self.lvl==1) or self.view_matrix.eye.x <= 6 and self.view_matrix.eye.z <= 4 and self.view_matrix.eye.z >= -3 and self.lvl == 1:
            self.falling = True
        if self.view_matrix.eye.z >= 5.0 and self.lvl == 1:
            self.falling = True
        if (self.view_matrix.eye.x >= 30.0 and self.lvl==2) or self.view_matrix.eye.x <= 5.0 and self.view_matrix.eye.z <= 10 and self.view_matrix.eye.z >= -10 and self.lvl == 2:
            self.falling = True
        if self.view_matrix.eye.z >= 7.3 and self.lvl == 2:
            self.falling = True

    def countdown(self):
        while self.t > 0:
            time.sleep(1)
            self.t -= 1

    def collison_check(self):
        if self.lvl == 1:
            for item in self.wall_list2:
                if not item[6]:
                    self.wall_min_x = item[0] - item[3] / 2
                    self.wall_max_x = item[0] + item[3] / 2
                    self.wall_min_z = item[2] - item[5] / 2
                    self.wall_max_z = item[2] + item[5] / 2
                    if self.wall_min_x-0.05 <= self.view_matrix.eye.x <= self.wall_max_x+0.05:
                        if self.wall_min_z-0.05 <= self.view_matrix.eye.z <= self.wall_max_z+0.05:
                            self.collisionNormal = True
                            return True
                    else:
                        self.collisionNormal = False
                if item[6]:
                    self.ang_wall_max_x = item[0] + item[5] / 2
                    self.ang_wall_min_x = item[0] - item[5] / 2
                    self.ang_wall_max_z = item[2] + item[3] / 2
                    self.ang_wall_min_z = item[2] - item[3] / 2
                    if self.ang_wall_min_x-0.05 <= self.view_matrix.eye.x <= self.ang_wall_max_x+0.05:
                        if self.ang_wall_min_z-0.05 <= self.view_matrix.eye.z <= self.ang_wall_max_z+0.05:
                            self.collisionAngle = True
                            return True
                    else:
                        self.collisionAngle = False
        if self.lvl == 2:
            for item in self.wall_list:
                if not item[6]:
                    self.wall_min_x = item[0] - item[3] / 2
                    self.wall_max_x = item[0] + item[3] / 2
                    self.wall_min_z = item[2] - item[5] / 2
                    self.wall_max_z = item[2] + item[5] / 2
                    if self.wall_min_x-0.05 <= self.view_matrix.eye.x <= self.wall_max_x+0.05:
                        if self.wall_min_z-0.05 <= self.view_matrix.eye.z <= self.wall_max_z+0.05:
                            self.collisionNormal = True
                            return True
                    else:
                        self.collisionNormal = False
                if item[6]:
                    self.ang_wall_max_x = item[0] + item[5] / 2
                    self.ang_wall_min_x = item[0] - item[5] / 2
                    self.ang_wall_max_z = item[2] + item[3] / 2
                    self.ang_wall_min_z = item[2] - item[3] / 2
                    if self.ang_wall_min_x-0.05 <= self.view_matrix.eye.x <= self.ang_wall_max_x+0.05:
                        if self.ang_wall_min_z-0.05 <= self.view_matrix.eye.z <= self.ang_wall_max_z+0.05:
                            self.collisionAngle = True

                            return True
                    else:
                        self.collisionAngle = False





    def load_texture(self, image):
        """ Loads a texture into the buffer """
        texture_surface = pygame.image.load(image)
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        # glEnable(GL_TEXTURE_2D)
        texid = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        return texid

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
            self.view_matrix.yaw(-90*delta_time)
        if self.D_key_down:
            #self.view_matrix.slide(1 * delta_time, 0, 0)
            #self.view_matrix.roll(-pi * delta_time)
            self.view_matrix.yaw(90 * delta_time)
        if self.T_key_down:
            self.fov -= 0.25 * delta_time
        if self.G_key_down:
            self.fov += 0.25 * delta_time
        if self.UP_key_down and not self.collisionNormal and not self.collisionAngle:
            self.view_matrix.slide(0, 0, -1.5 * delta_time)
        if self.DOWN_key_down:
            self.view_matrix.slide(0, 0, 3 * delta_time)
        if self.RIGHT_key_down:
            self.view_matrix.slide(3 * delta_time, 0, 0)
        if self.LEFT_key_down:
            self.view_matrix.slide(-3 * delta_time, 0, 0)
        if self.falling:
            pygame.mixer.Sound.play(self.crash_sound)
            self.view_matrix.eye.y -= 3 * delta_time
        if self.collisionNormal and self.UP_key_down:
            self.view_matrix.slide(0, 0, 0)
        if self.collisionAngle and self.UP_key_down:
            self.view_matrix.slide(0, 0, 0)
        if self.view_matrix.eye.y <= -4:
            pygame.quit()
            quit()
        else:
            self.white_background = False
        #if self.lvl == 1:
            #pygame.mixer.Sound.play(self.soundtrack_sound)
        self.check_if_won()
        self.check_if_died()
        self.collison_check()

    def display(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FRAMEBUFFER_SRGB)
        #glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.01, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())


        #textSurface = self.font.render(str(self.t), True, (255, 255, 66, 255), (0, 66, 0, 255))
        #textData = pygame.image.tostring(textSurface, "RGBA", True)
        #glWindowPos2d(self.textX1, self.textY1)
        #glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)

        '''glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_player)
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        # self.shader.set_solid_color(0.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y-0.1, self.view_matrix.eye.z+0.4)
        self.model_matrix.add_scale(0.2, 0.2, 0.2)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)'''

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_left)
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        # self.shader.set_solid_color(0.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0.0, 1.0, 2.0)
        self.model_matrix.add_rotate_y(pi / 2)
        self.model_matrix.add_scale(20.0, 30.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_mountains)
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        # self.shader.set_solid_color(0.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.1, 1.0, -10.0)
        self.model_matrix.add_scale(25.0, 30.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_right)
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        # self.shader.set_solid_color(0.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(20.0, 1.0, 2.0)
        self.model_matrix.add_rotate_y(pi/2)
        self.model_matrix.add_scale(20.0, 30.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_back)
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        # self.shader.set_solid_color(0.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.1, 1.0, 10.0)
        self.model_matrix.add_rotate_y(pi)
        self.model_matrix.add_scale(20.0, 30.0, 1.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)


        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_skybox)
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)
        # self.shader.set_solid_color(0.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.1, 25.0, 1.0)
        self.model_matrix.add_scale(50.0, 0.5, 50.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)




        #self.shader.set_solid_color(1.0, 0.0, 0.0)
        glEnable(GL_TEXTURE_2D)
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_wall_diffuse)
        if self.lvl == 2:
            for index in self.wall_list:
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(index[0], index[1], index[2])
                if index[6]:
                    self.model_matrix.add_rotate_y(pi / 2)
                self.model_matrix.add_scale(index[3], index[4], index[5])
                self.shader.set_model_matrix(self.model_matrix.matrix)

                self.cube.draw()
                self.model_matrix.pop_matrix()

        if self.lvl == 1:
            for index in self.wall_list2:
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(index[0], index[1], index[2])
                if index[6]:
                    self.model_matrix.add_rotate_y(pi / 2)
                self.model_matrix.add_scale(index[3], index[4], index[5])
                self.shader.set_model_matrix(self.model_matrix.matrix)

                self.cube.draw()
                self.model_matrix.pop_matrix()

        glDisable(GL_TEXTURE_2D)

        glDisable(GL_BLEND)
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

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import pygame
from pygame.locals import *

import sys
import time
from Base3DObjects import *
from Shaders import *
from Matrices import *
import os

class GraphicsProgram3D:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)
        pygame.font.init()

        self.shader = Shader3D()
        self.shader.use()
        self.lvl = 1
        self.model_matrix = ModelMatrix()
        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(7, 1, 3.5), Point(10, 1.0, 0), Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        """Sounds"""
        self.crash_sound = pygame.mixer.Sound("sounds/scream.wav")
        self.lvlup_sound = pygame.mixer.Sound("sounds/lvlcomplete.wav")
        self.soundtrack_sound = pygame.mixer.Sound("sounds/soundtrack.wav")
        self.flashlight_click = pygame.mixer.Sound("sounds/flashlight.wav")


        #Textures

        self.tex_id_wall_diffuse = self.load_texture("./textures/wall1.png")
        self.tex_id_wall_specular = self.load_texture("./textures/wall1.png")

        self.tex_id_floorandceiling = self.load_texture("./textures/bruh.png")
        self.projection_matrix = ProjectionMatrix()
        self.fov = pi / 2
        self.projection_matrix.set_perspective(pi / 2, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.cube = Cube()
        self.scale = Point(1, 1, 1)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('./fonts/BubbleShine.ttf', 70)

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
            [6.8, 1.0, 3.0, 1.0, 1.0, 0.2, False],
            [9.0, 1.0, 3.0, 2.0, 1.0, 0.2, False],
            [7.2, 1.0, -1.0, 2.0, 1, 0.2, False],
            [9.5, 1.0, -1.0, 1.0, 1, 0.2, False],
            [9.3, 1.0, -0.0, 0.5, 1.0, 0.2, False],
            [7.2, 1.0, -0.0, 2.0, 1, 0.2, False],
            [9.0, 1.0, -0.5, 0.2, 1, 0.8, False],
            [8.75, 1.0, 1.0, 1.3, 1.0, 0.2, False],
            [8.1, 1.0, 0.6, 0.2, 1, 1.0, False],
            [6.8, 1.0, 2.0, 1.0, 1.0, 0.2, False],
            [7.2, 1.0, 1.5, 0.2, 1, 1.0, False],
            [8.65, 1.0, 2.0, 1.3, 1.0, 0.2, False],
            [8.1, 1.0, 2.6, 0.2, 1, 1.0, False],

        ]

        self.ceilingandfloorlvl1 = [
            [8.1, 0.0, 0.0, 4.0, 1.0, 7.0, False],
            [8.1, 2.0, 0.0, 4.0, 1.0, 7.0, False],
        ]
        self.angle = 0
        self.collisionNormal = False
        self.collisionAngle = False
        self.A_key_down = False
        self.D_key_down = False
        self.T_key_down = False
        self.G_key_down = False
        self.UP_key_down = False
        self.DOWN_key_down = False
        self.falling = False
        self.check_if_won()
        self.check_if_died()
        self.collison_check()
        self.wall_min_x = None
        self.wall_max_x = None
        self.wall_max_z = None
        self.wall_min_z = None
        self.ang_wall_min_x = None
        self.ang_wall_max_x = None
        self.ang_wall_max_z = None
        self.ang_wall_min_z = None
        self.right_collision = False
        self.left_collision = False
        self.SPACE_key_down = False

        #Player is the view
        self.player_pos = self.view_matrix.eye
        self.radius = 0.02

        self.textX1 = 30
        self.textY1 = 500

        #DIRECTIONS
        self.SOUTH_WEST = self.view_matrix.n.z >= 0 and self.view_matrix.n.x <= 0
        self.NORTH_WEST = self.view_matrix.n.z <= 0 and self.view_matrix.n.x <= 0
        self.SOUTH_EAST = self.view_matrix.n.z >= 0 and self.view_matrix.n.x >= 0
        self.NORTH_EAST = self.view_matrix.n.z >= 0 and self.view_matrix.n.x >= 0


    def check_if_won(self):
        if 8.0 <= self.view_matrix.eye.x <= 9 and -0.9 >= self.view_matrix.eye.z >= -1.1 and self.lvl ==1:
            self.lvl = 2
            pygame.mixer.Sound.play(self.lvlup_sound)
            self.view_matrix.look(Point(8, 1, 5.5), Point(0, 1.0, 0), Vector(0, 1, 0))
            print("You solved the maze!")


        if self.view_matrix.eye.x >= 6.0 and self.view_matrix.eye.x <= 8 and self.view_matrix.eye.z <= -2.5 and self.view_matrix.eye.z >= -4.0 and self.lvl == 2:
            pygame.quit()
            quit()

    def check_if_died(self):
        if (self.view_matrix.eye.x >= 10.0 and self.lvl == 1) or self.view_matrix.eye.x <= 6 and 4 >= self.view_matrix.eye.z >= -3 and self.lvl == 1:
            self.falling = True
        if self.view_matrix.eye.z >= 5.0 and self.lvl == 1:
            self.falling = True
        if (self.view_matrix.eye.x >= 30.0 and self.lvl == 2) or self.view_matrix.eye.x <= 5.0 and 10 >= self.view_matrix.eye.z >= -10 and self.lvl == 2:
            self.falling = True
        if self.view_matrix.eye.z >= 7.3 and self.lvl == 2:
            self.falling = True


    def collison_check(self):
        if self.lvl == 1:
            for item in self.wall_list2:
                if not item[6]:
                    self.wall_min_x = item[0] - item[3] / 2
                    self.wall_max_x = item[0] + item[3] / 2
                    self.wall_min_z = item[2] - item[5] / 2
                    self.wall_max_z = item[2] + item[5] / 2
                    #V1 = Vector([self.view_matrix.eye.x, self.view_matrix.eye.z])
                    #V2 = Vector([item[0], item[2]])  # Use a coordinate that you know is on the line
                    #n = Vector([self])  # The n value of the sloped line
                    if self.wall_min_x-0.05 <= self.view_matrix.eye.x <= self.wall_max_x+0.05:
                        if self.wall_min_z-0.05 <= self.view_matrix.eye.z <= self.wall_max_z+0.05:
                            self.collisionNormal = True
                            return True
                    else:
                        self.collisionNormal = False
                """if item[6]:
                    self.ang_wall_max_x = item[0] + item[5] / 2
                    self.ang_wall_min_x = item[0] - item[5] / 2
                    self.ang_wall_max_z = item[2] + item[3] / 2
                    self.ang_wall_min_z = item[2] - item[3] / 2
                    player_min_x = self.player_pos.x - self.radius
                    player_max_x = self.player_pos.x + self.radius
                    player_min_z = self.player_pos.z - self.radius
                    player_max_z = self.player_pos.z + self.radius
                    scale_player = self.radius * 2
                    if self.ang_wall_min_x-0.05 <= self.view_matrix.eye.x <= self.ang_wall_max_x+0.05:
                        if self.ang_wall_min_z-0.05 <= self.view_matrix.eye.z <= self.ang_wall_max_z+0.05:
                            if self.wall_min_x -0.1 >= self.view_matrix.eye.x >= self.wall_min_x:
                                self.collisionNormal = True
                            else:
                                self.collisionAngle = True
                            return True
                    else:
                        self.collisionAngle = False"""
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

        if self.A_key_down:
            self.view_matrix.yaw(-120*delta_time)
        if self.D_key_down:
            self.view_matrix.yaw(120 * delta_time)
        if self.T_key_down:
            self.fov -= 0.25 * delta_time
        if self.G_key_down:
            self.fov += 0.25 * delta_time
        if self.UP_key_down and not self.collisionNormal and not self.collisionAngle:
            self.view_matrix.slide(0, 0, -1.5 * delta_time)
        if self.DOWN_key_down and self.collisionNormal and self.collisionAngle:
            self.view_matrix.slide(0, 0, 3 * delta_time)
        if self.falling:
            pygame.mixer.Sound.play(self.crash_sound)
            self.view_matrix.eye.y -= 3 * delta_time

            """check for direction of player and make him slide accordingly"""
        if self.UP_key_down:
            if self.collisionNormal and self.NORTH_EAST:
                if self.wall_min_x >= self.view_matrix.eye.x >= self.wall_min_x-0.2:
                    self.view_matrix.slide(1.5 * delta_time, 0, 0)

            if self.collisionNormal and self.NORTH_WEST:
                if self.wall_max_x <= self.view_matrix.eye.x <= self.wall_max_x+0.2:
                    self.view_matrix.slide(-1.5 * delta_time, 0, 0)
                else:
                    self.view_matrix.slide(1.5 * delta_time, 0, 0)
            if self.collisionNormal and self.SOUTH_EAST:
                if self.wall_min_x >= self.view_matrix.eye.x >= self.wall_min_x - 0.2:
                    self.view_matrix.slide(1.5 * delta_time, 0, 0)
                else:
                    self.view_matrix.slide(-1.5 * delta_time, 0, 0)
            if self.collisionNormal and self.SOUTH_WEST:
                if self.wall_max_x >= self.view_matrix.eye.x >= self.wall_max_x + 0.2:
                    self.view_matrix.slide(1.5 * delta_time, 0, 0)
                else:
                    self.view_matrix.slide(-1.5 * delta_time, 0, 0)


            """If player is falling, the game ends"""
        if self.view_matrix.eye.y <= -4:
            pygame.quit()
            quit()
            print("You died")
        #if self.lvl == 1:
            #pygame.mixer.Sound.play(self.soundtrack_sound)
        self.check_if_won()
        self.check_if_died()
        self.collison_check()

    def display(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FRAMEBUFFER_SRGB)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.01, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        textSurface = self.font.render(str("Hallo"), True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(self.textX1, self.textY1)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)

        """"LIGHTS"""
        self.shader.set_global_light_direction(Point(-0.3, -1.0, -0.4))
        self.shader.set_global_light_color(Color(0.01, 0.01, 0.01))

        if self.SPACE_key_down:
            self.shader.set_active_flashlight(1.0)
            self.shader.set_flashlight_direction(self.view_matrix.n)
            self.shader.set_flashlight_color(Color(1.0, 209/255, 178/255))
            self.shader.set_flashlight_position(Point(self.view_matrix.eye.x, self.view_matrix.eye.y * 0.5, self.view_matrix.eye.z))
            self.shader.set_flashlight_cutoff(cos((40 + 6.5) * pi/180))
            self.shader.set_flashlight_outer_cutoff(cos((40 + 11.5) * pi/180))
            self.shader.set_flashlight_constant(1.0)
            self.shader.set_flashlight_linear(0.14)
            self.shader.set_flashlight_quad(0.07)


        if not self.SPACE_key_down:
            self.shader.set_active_flashlight(0.0)

        self.shader.set_light_direction(self.view_matrix.v)
        self.shader.set_light_color(Color(1.0, 209 / 255, 178 / 255))
        self.shader.set_light_position(
        Point(self.view_matrix.eye.x, self.view_matrix.eye.y+0.5, self.view_matrix.eye.z))
        self.shader.set_light_cutoff(cos((40 + 6.5) * pi / 180))
        self.shader.set_light_outer_cutoff(cos((40 + 11.5) * pi / 180))
        self.shader.set_light_constant(1.0)
        self.shader.set_light_linear(0.14)
        self.shader.set_light_quad(0.07)


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
        """glEnable(GL_TEXTURE_2D)
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_floorandceiling)
        if self.lvl == 1:
            for index in self.ceilingandfloorlvl1:
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(index[0], index[1], index[2])
                if index[6]:
                    self.model_matrix.add_rotate_y(pi / 2)
                self.model_matrix.add_scale(index[3], index[4], index[5])
                self.shader.set_model_matrix(self.model_matrix.matrix)

                self.cube.draw()
                self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)"""

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_wall_diffuse)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_wall_specular)
        self.shader.set_material_diffuse(Color(0.7, 0.7, 0.7))
        self.shader.set_material_specular(Color(0.5, 0.5, 0.5))
        self.shader.set_material_shiny(10)
        self.shader.set_material_emit(0.0)
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

                    if event.key == K_a:
                        self.A_key_down = True

                    if event.key == K_d:
                        self.D_key_down = True

                    if event.key == K_t:
                        self.T_key_down = True

                    if event.key == K_g:
                        self.G_key_down = True

                    if event.key == K_SPACE:
                        pygame.mixer.Sound.play(self.flashlight_click)
                        self.SPACE_key_down = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False

                    if event.key == K_DOWN:
                        self.DOWN_key_down = False

                    if event.key == K_a:
                        self.A_key_down = False

                    if event.key == K_d:
                        self.D_key_down = False

                    if event.key == K_t:
                        self.T_key_down = False

                    if event.key == K_g:
                        self.G_key_down = False

                    if event.key == K_SPACE:
                        self.SPACE_key_down = False

            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()


    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()
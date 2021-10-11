from OpenGL.GL import *
from OpenGL.GLUT import *
from math import *
import pygame
from pygame.locals import *
import sys
from objloader import *
from Base3DObjects import *
from Shaders import *
from Matrices import *
from Control3DBase import objloader


class GraphicsProgram3D:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)
        self.shader = Shader3D()
        self.shader.use()
        self.lvl = 1
        self.model_matrix = ModelMatrix()
        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(7, 1, 5), Point(7, 1.0, 0.0), Vector(0, 1, 0))
        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        """Sounds"""
        self.crash_sound = pygame.mixer.Sound("sounds/scream.wav")
        self.lvlup_sound = pygame.mixer.Sound("sounds/lvlcomplete.wav")
        self.flashlight_click = pygame.mixer.Sound("sounds/flashlight.wav")
        self.jumpscare = pygame.mixer.Sound("sounds/jumpscare.wav")


        self.flashlight_angle = 0 #To calculate flashlight yaw

        """Textures"""
        self.shader.set_diffuse_texture(0)
        self.tex_id_wall_diffuse = self.load_texture("./textures/gravel.jpeg")
        self.shader.set_specular_texture(1)
        self.tex_id_wall_specular = self.load_texture("./textures/gravel.jpeg")

        self.tex_id_vurdulak_diffuse = self.load_texture("./textures/vurdalak_Base_Color.jpg")
        self.tex_id_vurdulak_specular = self.load_texture("./textures/vurdalak_Base_Color.jpg")
        self.tex_id_flashlight_diffuse = self.load_texture("./textures/black.jpeg")
        self.tex_id_flashlight_specular = self.load_texture("./textures/black.jpeg")

        self.tex_id_floorandceiling = self.load_texture("./textures/gravel.jpeg")
        self.tex_id_floorandceiling_specular = self.load_texture("./textures/gravel.jpeg")

        """Ignore the name this is the start  up screen"""
        self.tex_id_jumpscare_diffuse = self.load_texture("./textures/screen.png")
        self.tex_id_jumpscare_specular = self.load_texture("./textures/screen.png")

        self.tex_id_win_screen_diffuse = self.load_texture("./textures/winscreen.png")
        self.tex_id_win_screen_specular = self.load_texture("./textures/winscreen.png")

        self.projection_matrix = ProjectionMatrix()
        self.fov = pi / 2
        self.projection_matrix.set_perspective(pi / 2, 800 / 600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.cube = Cube()
        self.scale = Point(1, 1, 1)
        self.clock = pygame.time.Clock()

        """Obj models"""
        self.obj_model = objloader.load_obj_file(sys.path[0] + '/objects/', 'vurdalak_low.obj')
        self.obj_model_flashlight = objloader.load_obj_file(sys.path[0] + '/objects/', 'FlashlightOBJ.obj')

        """Walls: x, y, z positions, and x, y, z scale"""
        self.wall_list = [
            [15.0, 1.0, 1.0, 0.2, 1.0, 8.0],
            [5.0, 1.0, 1.0, 0.2, 1.0, 8.0],
            [8.9, 1.0, 5.0, 8.0, 1.0, 0.2],
            [14.5, 1.0, 5.0, 1.2, 1.0, 0.2],
            [11.1, 1.0, -3.1, 8.0, 1, 0.2],
            [5.4, 1.0, -3.1, 1.0, 1.0, 0.2],
            [8.0, 1.0, -1.5, 6.0, 1.0, 0.2],
            [6.0, 1.0, 1.4, 0.2, 1.0, 4.0],
            [5.8, 1.0, 4.0, 1.5, 1.0, 0.2],
            [7.4, 1.0, 4.0, 0.2, 1.0, 2.0],
            [10.5, 1.0, 3.1, 6.5, 1.0, 0.2],
            [11.2, 1.0, 4.1, 5.5, 1.0, 0.2],
            [14.0, 1.0, 4.5, 0.2, 1.0, 1.0],
            [13.2, 1.0, -0.8, 0.2, 1.0, 4.5],
            [10.2, 1.0, 1.4, 6.0, 1.0, 0.2],
            [12.0, 1.0, -0.2, 0.2, 1.0, 3.0],
            [7.3, 1.0, 0.4, 0.2, 1.0, 1.9],
            [8.3, 1.0, -0.6, 0.2, 1.0, 2.0],
            [10.9, 1.0, -0.6, 0.2, 1.0, 2.0],
            [6.7, 1.0, -0.5, 1.4, 1.0, 0.2],
            [9.6, 1.0, 0.5, 2.8, 1.0, 0.2],
            [14.0, 1.0, 0.2, 0.2, 1.0, 4.3],
            [13.0, 1.0, 2.3, 3.8, 1.0, 0.2],
            [10.0, 1.0, 2.7, 0.2, 1.0, 1.0],
            [8.7, 1.0, 2.3, 2.5, 1.0, 0.2],
        ]
        self.wall_list2 = [
            [10.0, 1.0, 1.0, 0.2, 1.0, 4.0],
            [6.2, 1.0, 1.0, 0.2, 1.0, 4.0],
            [6.8, 1.0, 3.0, 1.0, 1.0, 0.2],
            [9.0, 1.0, 3.0, 2.0, 1.0, 0.2],
            [7.2, 1.0, -1.0, 2.0, 1, 0.2],
            [9.5, 1.0, -1.0, 1.0, 1, 0.2],
            [9.15, 1.0, -0.0, 0.5, 1.0, 0.2],
            [7.2, 1.0, -0.0, 2.0, 1, 0.2],
            [9.0, 1.0, -0.5, 0.2, 1, 0.8],
            [8.75, 1.0, 1.0, 1.3, 1.0, 0.2],
            [8.1, 1.0, 0.6, 0.2, 1, 1.0],
            [6.8, 1.0, 2.0, 1.0, 1.0, 0.2],
            [7.2, 1.0, 1.5, 0.2, 1, 1.0],
            [8.65, 1.0, 2.0, 1.3, 1.0, 0.2],
            [8.1, 1.0, 2.6, 0.2, 1, 1.0]
        ]

        self.ceilingandfloorlvl1 = [
            [8.1, 0.0, 1.0, 4.0, 1.0, 8.0],
            [8.1, 2.0, 1.0, 4.0, 1.0, 8.0]
        ]
        self.floor_lvl2 = [
            [10, 0.0, 1.0, 10, 1.0, 10.0]
        ]

        self.monster_pos_locations = [
            [8.8, 0.6, 2.4, pi/2],
            [6.8, 0.6, 1.4, pi],
        ]
        self.monster_pos_locations_lvl_2 = [
            [14.5, 0.6, 0.6, pi],
            [5.5, 0.4, 4.5, pi/2],
            [12.5, 0.4, 0.8, pi]
        ]

        """A lot of stuff we need"""
        self.JUMPSCARE = False
        self.JUMPSCARE_other = False

        self.collisionLeftWall = False
        self.collisionRightWall = False
        self.collisionTopWall = False
        self.collisionBottomWall = False
        self.A_key_down = False
        self.D_key_down = False
        self.T_key_down = False
        self.G_key_down = False
        self.UP_key_down = False
        self.falling = False
        self.check_if_won()
        self.check_if_died()
        self.collison_check()
        self.SPACE_key_down = False
        self.p_key_down = False

        """Used to calculate how long the player looks at the monster"""
        self.looking_at_monster_count = 1
        self.looking_at_monster_count_other = 1

        self.won = False

        self.ENTER_key_down = True

    def check_if_won(self):
        if 8.0 <= self.view_matrix.eye.x <= 9 and -0.9 >= self.view_matrix.eye.z >= -1.1 and self.lvl == 1:
            self.lvl = 2
            pygame.mixer.Sound.play(self.lvlup_sound)
            self.view_matrix.look(Point(13.5, 1, 5.5), Point(13.5, 1.0, 0), Vector(0, 1, 0))
            self.looking_at_monster_count = 1
            self.looking_at_monster_count_other = 1
            print("You solved the maze!")

        if 7 >= self.view_matrix.eye.x >= 6.0 and -3.0 >= self.view_matrix.eye.z >= -4.0 and self.lvl == 2:
            self.won = True


    def check_if_died(self):
        if (self.view_matrix.eye.x >= 10.0 and self.lvl == 1) or self.view_matrix.eye.x <= 6 and 5 >= self.view_matrix.eye.z >= -3 and self.lvl == 1:
            self.falling = True
        if self.view_matrix.eye.z >= 5.2 and self.lvl == 1:
            self.falling = True
        if (self.view_matrix.eye.x >= 30.0 and self.lvl == 2) or self.view_matrix.eye.x <= 5.0 and 10 >= self.view_matrix.eye.z >= -10 and self.lvl == 2:
            self.falling = True
        if self.view_matrix.eye.z >= 7.3 and self.lvl == 2:
            self.falling = True

    def check_distance_from_monster(self):
        if self.lvl == 1:
            look_x_min = 6.1
            look_x_max = 7.7
            look_z_min = 0.0
            look_z_max = 1.0
            other_x_min = 8.9
            other_x_max = 10.0
            other_z_min = 2.0
            other_z_max = 3.0
            if self.view_matrix.n.z <= 0 and -0.40 <= self.view_matrix.n.x <= 0.80:
                if look_x_min <= self.view_matrix.eye.x <= look_x_max:
                    if look_z_min <= self.view_matrix.eye.z <= look_z_max:
                        self.looking_at_monster_count += 1
            if self.view_matrix.n.x >= 0 and -0.60 <= self.view_matrix.n.z <= 0.40:
                if other_x_min <= self.view_matrix.eye.x <= other_x_max:
                    if other_z_min <= self.view_matrix.eye.z <= other_z_max:
                        self.looking_at_monster_count_other += 1
        if self.lvl == 2:
            look_x_min_2 = 13.7
            look_x_max_2 = 14.8
            look_z_min_2 = -2.7
            look_z_max_2 = 0.5
            other_x_min_2 = 12.0
            other_x_max_2 = 13.0
            other_z_min_2 = -2.5
            other_z_max_2 = 0.5
            third_x_min = 6.5
            third_x_max = 7.5
            third_z_min = 4.0
            third_z_max = 5.0
            if self.view_matrix.n.z <= 0 and -0.40 <= self.view_matrix.n.x <= 0.40:
                if look_x_min_2 <= self.view_matrix.eye.x <= look_x_max_2:
                    if look_z_min_2 <= self.view_matrix.eye.z <= look_z_max_2:
                        self.looking_at_monster_count += 1
            if self.view_matrix.n.z <= 0 and -0.40 <= self.view_matrix.n.x <= 0.40:
                if other_x_min_2 <= self.view_matrix.eye.x <= other_x_max_2:
                    if other_z_min_2 <= self.view_matrix.eye.z <= other_z_max_2:
                        self.looking_at_monster_count += 1
            if self.view_matrix.n.x >= 0 and -0.60 <= self.view_matrix.n.z <= 0.40:
                if third_x_min <= self.view_matrix.eye.x <= third_x_max:
                    if third_z_min <= self.view_matrix.eye.z <= third_z_max:
                        self.looking_at_monster_count_other += 1

    def collison_check(self):
        if self.lvl == 1:
            for item in self.wall_list2:
                wall_min_x = item[0] - item[3] / 2
                wall_max_x = item[0] + item[3] / 2
                wall_min_z = item[2] - item[5] / 2
                wall_max_z = item[2] + item[5] / 2
                if wall_max_x+0.2 >= self.view_matrix.eye.x >= wall_max_x+0.1:
                    if wall_min_z-0.1 <= self.view_matrix.eye.z <= wall_max_z+0.1:
                        self.collisionRightWall = True
                        return True
                else:
                    self.collisionRightWall = False

                if wall_min_x-0.2 <= self.view_matrix.eye.x <= wall_min_x-0.1:
                    if wall_min_z-0.2 <= self.view_matrix.eye.z <= wall_max_z+0.1:
                        self.collisionLeftWall = True
                        return True
                else:
                    self.collisionLeftWall = False

                if wall_min_z-0.2 <= self.view_matrix.eye.z <= wall_min_z-0.1:
                    if wall_min_x-0.1 <= self.view_matrix.eye.x <= wall_max_x+0.1:
                        self.collisionTopWall = True
                        return True
                else:
                    self.collisionTopWall = False

                if wall_max_z+0.2 >= self.view_matrix.eye.z >= wall_max_z+0.1:
                    if wall_min_x-0.1 <= self.view_matrix.eye.x <= wall_max_x+0.1:
                        self.collisionBottomWall = True
                        return True
                else:
                    self.collisionBottomWall = False

        if self.lvl == 2:
            for item in self.wall_list:
                wall_min_x = item[0] - item[3] / 2
                wall_max_x = item[0] + item[3] / 2
                wall_min_z = item[2] - item[5] / 2
                wall_max_z = item[2] + item[5] / 2
                if wall_max_x + 0.2 >= self.view_matrix.eye.x >= wall_max_x + 0.1:
                    if wall_min_z - 0.1 <= self.view_matrix.eye.z <= wall_max_z + 0.1:
                        self.collisionRightWall = True
                        return True
                else:
                    self.collisionRightWall = False

                if wall_min_x - 0.2 <= self.view_matrix.eye.x <= wall_min_x - 0.1:
                    if wall_min_z - 0.2 <= self.view_matrix.eye.z <= wall_max_z + 0.1:
                        self.collisionLeftWall = True
                        return True
                else:
                    self.collisionLeftWall = False

                if wall_min_z - 0.2 <= self.view_matrix.eye.z <= wall_min_z - 0.1:
                    if wall_min_x - 0.1 <= self.view_matrix.eye.x <= wall_max_x + 0.1:
                        self.collisionTopWall = True
                        return True
                else:
                    self.collisionTopWall = False

                if wall_max_z + 0.2 >= self.view_matrix.eye.z >= wall_max_z + 0.1:
                    if wall_min_x - 0.1 <= self.view_matrix.eye.x <= wall_max_x + 0.1:
                        self.collisionBottomWall = True
                        return True
                else:
                    self.collisionBottomWall = False

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

        if self.A_key_down:
            self.view_matrix.yaw(-120*delta_time)
            self.flashlight_angle += -((2*pi)/3) * delta_time
        if self.D_key_down:
            self.view_matrix.yaw(120 * delta_time)
            self.flashlight_angle += ((2*pi)/3) * delta_time
        if self.T_key_down:
            self.fov -= 0.25 * delta_time
        if self.G_key_down:
            self.fov += 0.25 * delta_time
        if self.UP_key_down and not self.collisionLeftWall and not self.collisionRightWall and not self.collisionTopWall and not self.collisionBottomWall and not self.ENTER_key_down and not self.won:
            self.view_matrix.slide(0, 0, -1.5 * delta_time)

        if self.falling:
            pygame.mixer.Sound.play(self.crash_sound)
            self.view_matrix.eye.y -= 3 * delta_time
        """
        Check for direction of player and make him slide accordingly, we also check what part of the wall
        the player is hitting. If the player is looking away from the wall that he is colliding with he can walk freely
        this fixes the bug that the player can get stuck to the wall. The collisions are very smooth in our program.
        """
        if self.UP_key_down:
            """Right side of wall"""
            if self.collisionRightWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(1 * delta_time, 0, 0)

            if self.collisionRightWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            if self.collisionRightWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(-1 * delta_time, 0, 0)

            if self.collisionRightWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            """Left side of wall"""

            if self.collisionLeftWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(1 * delta_time, 0, 0)

            if self.collisionLeftWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            if self.collisionLeftWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(-1 * delta_time, 0, 0)

            if self.collisionLeftWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            """Bottom side of wall"""

            if self.collisionBottomWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(-1 * delta_time, 0, 0)

            if self.collisionBottomWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            if self.collisionBottomWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(1 * delta_time, 0, 0)

            if self.collisionBottomWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            """Top side of wall"""

            if self.collisionTopWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(1 * delta_time, 0, 0)

            if self.collisionTopWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

            if self.collisionTopWall and self.view_matrix.n.z <= 0 and self.view_matrix.n.x <= 0:
                self.view_matrix.slide(-1 * delta_time, 0, 0)

            if self.collisionTopWall and self.view_matrix.n.z >= 0 and self.view_matrix.n.x >= 0:
                self.view_matrix.slide(0, 0, -1 * delta_time)

        """If player is falling, the game ends"""
        if self.view_matrix.eye.y <= -4:
            pygame.quit()
            quit()
            print("You died, don't walk away from the area")

        """Basically just a lot of checks for the monster and the player and accounting for death and win"""
        if self.looking_at_monster_count >= 350:
            self.JUMPSCARE = True
            pygame.mixer.Sound.play(self.jumpscare)
        if self.looking_at_monster_count >= 400:
            self.ENTER_key_down = True
            if self.lvl == 1:
                self.view_matrix.look(Point(7, 1, 5), Point(7, 1.0, 0.0), Vector(0, 1, 0))
            if self.lvl == 2:
                self.view_matrix.look(Point(13.5, 1, 5.5), Point(13.5, 1.0, 0), Vector(0, 1, 0))
            self.looking_at_monster_count = 1
            self.JUMPSCARE = False
            self.flashlight_angle = 0
        if self.looking_at_monster_count_other >= 350:
            self.JUMPSCARE_other = True
            pygame.mixer.Sound.play(self.jumpscare)
        if self.looking_at_monster_count_other >= 400:
            self.ENTER_key_down = True
            if self.lvl == 1:
                self.view_matrix.look(Point(7, 1, 5), Point(7, 1.0, 0.0), Vector(0, 1, 0))
            if self.lvl == 2:
                self.view_matrix.look(Point(13.5, 1, 5.5), Point(13.5, 1.0, 0), Vector(0, 1, 0))
            self.looking_at_monster_count_other = 1
            self.JUMPSCARE_other = False
            self.flashlight_angle = 0
        if self.p_key_down and self.won:
            self.ENTER_key_down = True
            self.flashlight_angle = 0
            self.lvl = 1
            self.view_matrix.look(Point(7, 1, 5), Point(7, 1.0, 0.0), Vector(0, 1, 0))
            self.looking_at_monster_count_other = 1
            self.looking_at_monster_count = 1
            self.won = False
            self.p_key_down = False
            """Our functions must be called here in the update"""
        self.check_if_won()
        self.check_if_died()
        self.collison_check()
        self.check_distance_from_monster()

    def display(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_FRAMEBUFFER_SRGB)
        glShadeModel(GL_SMOOTH)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.projection_matrix.set_perspective(self.fov, 800 / 600, 0.01, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.model_matrix.load_identity()
        self.cube.set_verticies(self.shader)

        """"LIGHTS"""
        self.shader.set_normal_light_direction(Point(-0.3, -1.0, -0.4))
        self.shader.set_normal_light_color(Color(0.01, 0.01, 0.01))

        if self.SPACE_key_down:
            """
            We need the spotlight's position vector 
            (to calculate the fragment-to-light's direction vector), 
            the spotlight's direction vector, and the cutoff angle are the parameters we'll need for the fragment shader.
            To implement attenuation we'll be needing 3 extra values in the fragment shader:
             namely the constant, linear and quadratic terms of the equation.
             """
            self.shader.set_active_flashlight(1.0)
            self.shader.set_flashlight_direction(self.view_matrix.n)
            self.shader.set_flashlight_color(Color(0.9725, 0.7647, 0.4667))
            self.shader.set_flashlight_position(Point(self.view_matrix.eye.x, self.view_matrix.eye.y - 0.1, self.view_matrix.eye.z-0.2))
            """cut off: calculate the cosine value based on an angle and pass the cosine result to the fragment shader."""
            self.shader.set_flashlight_cutoff(cos((40 + 6.5) * pi/180))
            self.shader.set_flashlight_outer_cutoff(cos((40 + 11.5) * pi/180))
            self.shader.set_flashlight_constant(1.0)
            self.shader.set_flashlight_linear(0.14)
            self.shader.set_flashlight_quad(0.07)


        if not self.SPACE_key_down:
            self.shader.set_active_flashlight(0.0)

        """
        This is almost exactly like the flashlight except we need to point the vector down on the player,
        so he get's a nice lantern like lighting around him
        """
        self.shader.set_light_direction(self.view_matrix.v)
        self.shader.set_light_color(Color(0.9725, 0.7647, 0.4667))
        self.shader.set_light_position(
        Point(self.view_matrix.eye.x, self.view_matrix.eye.y+0.7, self.view_matrix.eye.z))
        self.shader.set_light_cutoff(cos((40 + 6.5) * pi / 180))
        self.shader.set_light_outer_cutoff(cos((40 + 11.5) * pi / 180))
        self.shader.set_light_constant(1.0)
        self.shader.set_light_linear(0.14)
        self.shader.set_light_quad(0.07)

        """Drawing and some more drawing....."""
        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_floorandceiling)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_floorandceiling_specular)
        if self.lvl == 1:
            for index in self.ceilingandfloorlvl1:
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(index[0], index[1], index[2])
                self.model_matrix.add_scale(index[3], index[4], index[5])
                self.shader.set_model_matrix(self.model_matrix.matrix)

                self.cube.draw()
                self.model_matrix.pop_matrix()
        if self.lvl == 2:
            for index in self.floor_lvl2:
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(index[0], index[1], index[2])
                self.model_matrix.add_scale(index[3], index[4], index[5])
                self.shader.set_model_matrix(self.model_matrix.matrix)
                self.cube.draw()
                self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)


        if self.ENTER_key_down:
            glEnable(GL_TEXTURE_2D)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.tex_id_jumpscare_diffuse)
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.tex_id_jumpscare_specular)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y-0.07, self.view_matrix.eye.z-0.5)
            self.model_matrix.add_scale(1.0, 0.5, 0.5)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw()
            self.model_matrix.pop_matrix()
            glDisable(GL_TEXTURE_2D)

        if self.won:
            glEnable(GL_TEXTURE_2D)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.tex_id_win_screen_diffuse)
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.tex_id_win_screen_specular)
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y-0.07, self.view_matrix.eye.z-0.5)
            self.model_matrix.add_scale(1.0, 0.5, 0.5)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.cube.draw()
            self.model_matrix.pop_matrix()
            glDisable(GL_TEXTURE_2D)


        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_wall_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_wall_specular)
        self.shader.set_material_diffuse(Color(0.7, 0.7, 0.7))
        self.shader.set_material_specular(Color(0.5, 0.5, 0.5))
        self.shader.set_material_shiny(10)
        self.shader.set_material_emit(0.0)
        if self.lvl == 2:
            for index in self.wall_list:
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(index[0], index[1], index[2])
                self.model_matrix.add_scale(index[3], index[4], index[5])
                self.shader.set_model_matrix(self.model_matrix.matrix)

                self.cube.draw()
                self.model_matrix.pop_matrix()

        if self.lvl == 1:
            for index in self.wall_list2:
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(index[0], index[1], index[2])
                self.model_matrix.add_scale(index[3], index[4], index[5])
                self.shader.set_model_matrix(self.model_matrix.matrix)
                self.cube.draw()
                self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_flashlight_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_flashlight_specular)
        self.shader.set_material_diffuse(Color(0.7, 0.7, 0.7))
        self.shader.set_material_specular(Color(0.5, 0.5, 0.5))
        self.shader.set_material_shiny(10)
        self.shader.set_material_emit(0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y-0.2, self.view_matrix.eye.z-0.2)
        self.model_matrix.add_rotate_x(pi/2)
        self.model_matrix.add_rotate_z(self.flashlight_angle)
        self.model_matrix.add_scale(0.1, 0.1, 0.7)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.obj_model_flashlight.draw(self.shader)
        self.model_matrix.pop_matrix()
        glDisable(GL_TEXTURE_2D)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_vurdulak_diffuse)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_vurdulak_specular)
        if self.lvl == 1:
            self.model_matrix.load_identity()
            self.cube.set_verticies(self.shader)
            for item in self.monster_pos_locations:
                self.model_matrix.push_matrix()
                if not self.JUMPSCARE and not self.JUMPSCARE_other:
                    self.model_matrix.add_translation(item[0], item[1], item[2])
                if self.JUMPSCARE:
                    self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y-0.6, self.view_matrix.eye.z+0.5)
                if self.JUMPSCARE_other:
                    self.model_matrix.add_translation(self.view_matrix.eye.x-0.35, self.view_matrix.eye.y-0.6, self.view_matrix.eye.z)
                self.model_matrix.add_rotate_y(item[3])
                self.model_matrix.add_scale(0.4, 0.4, 0.4)
                self.shader.set_model_matrix(self.model_matrix.matrix)
                self.obj_model.draw(self.shader)
                self.model_matrix.pop_matrix()

        if self.lvl == 2:
            self.model_matrix.load_identity()
            self.cube.set_verticies(self.shader)
            for item in self.monster_pos_locations_lvl_2:
                self.model_matrix.push_matrix()
                if not self.JUMPSCARE and not self.JUMPSCARE_other:
                    self.model_matrix.add_translation(item[0], item[1], item[2])
                if self.JUMPSCARE:
                    self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y-0.6, self.view_matrix.eye.z+0.5)
                if self.JUMPSCARE_other:
                    self.model_matrix.add_translation(self.view_matrix.eye.x-0.35, self.view_matrix.eye.y-0.6, self.view_matrix.eye.z)
                self.model_matrix.add_rotate_y(item[3])
                self.model_matrix.add_scale(0.7, 0.7, 0.7)
                self.shader.set_model_matrix(self.model_matrix.matrix)
                self.obj_model.draw(self.shader)
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

                    if event.key == K_w:
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

                    if event.key == K_RETURN:
                        self.ENTER_key_down = False

                    if event.key == K_p and self.won:
                        self.p_key_down = True

                    if event.key == K_q:
                        pygame.quit()
                        quit()

                elif event.type == pygame.KEYUP:
                    if event.key == K_w:
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


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from pygame.locals import *
import math
import sys

# VARIÁVEIS GLOBAIS DE ANIMAÇÃO
animation_running = False
wheel_rotation = 0.0
steer_angle = 0.0
drs_open = 0.0
track_line_offset = 0.0
camera_angle_y = 25.0
camera_angle_x = 15.0
camera_distance = 8.0

# FUNÇÕES AUXILIARES DE DESENHO
def draw_solid_cube(size=1.0):
    h = size / 2.0
    
    glBegin(GL_QUADS)
    
    glNormal3f(0, 0, 1)
    glVertex3f(-h, -h, h)
    glVertex3f(h, -h, h)
    glVertex3f(h, h, h)
    glVertex3f(-h, h, h)
    
    glNormal3f(0, 0, -1)
    glVertex3f(h, -h, -h)
    glVertex3f(-h, -h, -h)
    glVertex3f(-h, h, -h)
    glVertex3f(h, h, -h)
    
    glNormal3f(0, 1, 0)
    glVertex3f(-h, h, -h)
    glVertex3f(-h, h, h)
    glVertex3f(h, h, h)
    glVertex3f(h, h, -h)
    
    glNormal3f(0, -1, 0)
    glVertex3f(-h, -h, -h)
    glVertex3f(h, -h, -h)
    glVertex3f(h, -h, h)
    glVertex3f(-h, -h, h)
    
    glNormal3f(1, 0, 0)
    glVertex3f(h, -h, -h)
    glVertex3f(h, h, -h)
    glVertex3f(h, h, h)
    glVertex3f(h, -h, h)
    
    glNormal3f(-1, 0, 0)
    glVertex3f(-h, -h, h)
    glVertex3f(-h, h, h)
    glVertex3f(-h, h, -h)
    glVertex3f(-h, -h, -h)
    
    glEnd()

# FUNÇÕES AUXILIARES DE DESENHO
def draw_quad(v1, v2, v3, v4, normal=None):
    if normal:
        glNormal3f(*normal)
    glBegin(GL_QUADS)
    glVertex3f(*v1)
    glVertex3f(*v2)
    glVertex3f(*v3)
    glVertex3f(*v4)
    glEnd()

def draw_polygon(vertices, normal=None):
    if normal:
        glNormal3f(*normal)
    glBegin(GL_POLYGON)
    for v in vertices:
        glVertex3f(*v)
    glEnd()

def draw_extruded_shape(profile_left, profile_right, close_ends=True):
    n = len(profile_left)
    glBegin(GL_QUAD_STRIP)
    for i in range(n):
        glVertex3f(*profile_left[i])
        glVertex3f(*profile_right[i])
    glVertex3f(*profile_left[0])
    glVertex3f(*profile_right[0])
    glEnd()
    
    if close_ends:
        glBegin(GL_POLYGON)
        for v in profile_left:
            glVertex3f(*v)
        glEnd()
        glBegin(GL_POLYGON)
        for v in reversed(profile_right):
            glVertex3f(*v)
        glEnd()

# MONOCOQUE / CHASSI PRINCIPAL
def draw_monocoque():
    glColor3f(0.08, 0.08, 0.08)  # Preto carbono

    y_top = 0.12
    y_bottom = -0.22
    
    profile_top_right = [
        (1.5, 0.28),   # Frente (conexão com bico)
        (0.8, 0.32),   # Cockpit (mais largo)
        (0.2, 0.30),   # Atrás do cockpit
        (-0.3, 0.25),  # Início sidepods
        (-0.8, 0.22),  # Meio
        (-1.4, 0.18),  # Afunilando
        (-1.8, 0.12),  # Traseira estreita
    ]
    
    top_left = [(x, y_top, -z) for x, z in profile_top_right]
    top_right = [(x, y_top, z) for x, z in profile_top_right]
    bottom_left = [(x, y_bottom, -z * 0.9) for x, z in profile_top_right]
    bottom_right = [(x, y_bottom, z * 0.9) for x, z in profile_top_right]
    
    glNormal3f(0, 1, 0)
    glBegin(GL_QUAD_STRIP)
    for i in range(len(top_left)):
        glVertex3f(*top_left[i])
        glVertex3f(*top_right[i])
    glEnd()
    
    glNormal3f(0, -1, 0)
    glBegin(GL_QUAD_STRIP)
    for i in range(len(bottom_left)):
        glVertex3f(*bottom_right[i])
        glVertex3f(*bottom_left[i])
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    for i in range(len(top_right)):
        glVertex3f(*top_right[i])
        glVertex3f(*bottom_right[i])
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    for i in range(len(top_left)):
        glVertex3f(*bottom_left[i])
        glVertex3f(*top_left[i])
    glEnd()

def draw_engine_cover():
    glColor3f(0.08, 0.08, 0.08)

    profile_side = [
        (0.2, 0.15),    # Início (atrás do cockpit)
        (0.0, 0.28),    # Subindo
        (-0.15, 0.42),  # Subindo mais (base do airbox)
        (-0.3, 0.52),   # Pico máximo (topo do airbox)
        (-0.5, 0.48),   # Começando a descer
        (-0.7, 0.40),   # Descendo
        (-0.9, 0.32),   # Descendo mais
        (-1.1, 0.24),   # Continuando
        (-1.3, 0.18),   # Quase no fim
        (-1.5, 0.14),   # Baixo
        (-1.7, 0.10),   # Mais baixo
        (-1.9, 0.06),   # Traseira
    ]
    
    widths = [
        0.28,   # Início
        0.26,   # 
        0.22,   # Base airbox
        0.18,   # Topo airbox (mais estreito)
        0.16,   #
        0.15,   #
        0.14,   #
        0.13,   #
        0.12,   #
        0.11,   #
        0.10,   #
        0.08,   # Traseira (bem estreito)
    ]
    
    glBegin(GL_QUAD_STRIP)
    for i in range(len(profile_side)):
        x, y = profile_side[i]
        w = widths[i]
        glNormal3f(0, 1, 0)
        glVertex3f(x, y, -w)
        glVertex3f(x, y, w)
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    for i in range(len(profile_side)):
        x, y = profile_side[i]
        w = widths[i]
        y_base = 0.12 if x > -0.5 else 0.10 - (x + 0.5) * 0.05
        glNormal3f(0, 0, 1)
        glVertex3f(x, y, w)
        glVertex3f(x, y_base, w)
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    for i in range(len(profile_side)):
        x, y = profile_side[i]
        w = widths[i]
        y_base = 0.12 if x > -0.5 else 0.10 - (x + 0.5) * 0.05
        glNormal3f(0, 0, -1)
        glVertex3f(x, y_base, -w)
        glVertex3f(x, y, -w)
    glEnd()
    
    glColor3f(0.06, 0.06, 0.06)
    x_back = profile_side[-1][0]
    y_back = profile_side[-1][1]
    w_back = widths[-1]
    glBegin(GL_QUADS)
    glNormal3f(-1, 0, 0)
    glVertex3f(x_back, y_back, -w_back)
    glVertex3f(x_back, y_back, w_back)
    glVertex3f(x_back, -0.05, w_back)
    glVertex3f(x_back, -0.05, -w_back)
    glEnd()

def draw_nose():
    glColor3f(0.08, 0.08, 0.08)

    sections = [
        (1.5,   0.22,  0.20,  0.08,  -0.20),  # Base (conexão com chassi)
        (1.8,   0.18,  0.17,  0.04,  -0.20),  # Transição
        (2.1,   0.15,  0.14,  0.00,  -0.19),  # 
        (2.4,   0.12,  0.11, -0.04,  -0.18),  # Meio do bico
        (2.7,   0.09,  0.08, -0.06,  -0.17),  # Afunilando
        (3.0,   0.06,  0.05, -0.08,  -0.16),  # Mais fino
        (3.2,   0.04,  0.03, -0.10,  -0.15),  # Quase na ponta
        (3.4,   0.02,  0.015, -0.12,  -0.14),  # Ponta
    ]
    
    for i in range(len(sections) - 1):
        x1, wt1, wb1, yt1, yb1 = sections[i]
        x2, wt2, wb2, yt2, yb2 = sections[i + 1]
        
        glColor3f(0.08, 0.08, 0.08)
        glNormal3f(0, 1, 0)
        glBegin(GL_QUADS)
        glVertex3f(x1, yt1, -wt1)
        glVertex3f(x1, yt1, wt1)
        glVertex3f(x2, yt2, wt2)
        glVertex3f(x2, yt2, -wt2)
        glEnd()
        
        glNormal3f(0, -1, 0)
        glBegin(GL_QUADS)
        glVertex3f(x1, yb1, wt1)
        glVertex3f(x1, yb1, -wt1)
        glVertex3f(x2, yb2, -wt2)
        glVertex3f(x2, yb2, wt2)
        glEnd()
        
        glNormal3f(0, 0, 1)
        glBegin(GL_QUADS)
        glVertex3f(x1, yt1, wt1)
        glVertex3f(x1, yb1, wb1)
        glVertex3f(x2, yb2, wb2)
        glVertex3f(x2, yt2, wt2)
        glEnd()
        
        glNormal3f(0, 0, -1)
        glBegin(GL_QUADS)
        glVertex3f(x1, yt1, -wt1)
        glVertex3f(x2, yt2, -wt2)
        glVertex3f(x2, yb2, -wb2)
        glVertex3f(x1, yb1, -wb1)
        glEnd()
    
    x_tip = sections[-1][0]
    wt_tip = sections[-1][1]
    yt_tip = sections[-1][3]
    yb_tip = sections[-1][4]
    
    glColor3f(0.06, 0.06, 0.06)
    glNormal3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex3f(x_tip, yt_tip, -wt_tip)
    glVertex3f(x_tip, yt_tip, wt_tip)
    glVertex3f(x_tip, yb_tip, wt_tip)
    glVertex3f(x_tip, yb_tip, -wt_tip)
    glEnd()

# SIDEPODS
def draw_sidepod(side):
    glColor3f(0.10, 0.10, 0.10)
    
    z_offset = side * 0.22

    widths = [
        (0.8, 0.55),    # Frente - largo
        (0.5, 0.60),    # Máxima largura
        (0.0, 0.55),    # Meio
        (-0.4, 0.45),   # Começando undercut
        (-0.8, 0.30),   # Undercut forte
        (-1.2, 0.18),   # Traseira estreita
    ]
    
    y_top = 0.18
    y_bottom = -0.20
    
    for i in range(len(widths) - 1):
        x1, w1 = widths[i]
        x2, w2 = widths[i + 1]
        
        h1 = y_top * (1.0 if i < 2 else 0.85)
        h2 = y_top * (1.0 if i + 1 < 2 else 0.85)
        
        z_inner = z_offset
        z_outer1 = z_offset + side * w1
        z_outer2 = z_offset + side * w2
        
        glNormal3f(0, 1, 0)
        draw_quad(
            (x1, h1, z_inner),
            (x1, h1, z_outer1),
            (x2, h2, z_outer2),
            (x2, h2, z_inner)
        )
        
        nx = 0
        nz = side
        glNormal3f(nx, 0, nz)
        draw_quad(
            (x1, h1, z_outer1),
            (x1, y_bottom, z_outer1),
            (x2, y_bottom, z_outer2),
            (x2, h2, z_outer2)
        )
        
        glNormal3f(0, -1, 0)
        draw_quad(
            (x1, y_bottom, z_outer1),
            (x1, y_bottom, z_inner),
            (x2, y_bottom, z_inner),
            (x2, y_bottom, z_outer2)
        )
    
    x_front, w_front = widths[0]
    h_front = y_top
    z_inner_front = z_offset
    z_outer_front = z_offset + side * w_front
    
    glNormal3f(1, 0, 0)
    draw_quad(
        (x_front, h_front, z_inner_front),
        (x_front, h_front, z_outer_front),
        (x_front, y_bottom, z_outer_front),
        (x_front, y_bottom, z_inner_front)
    )
    
    x_back, w_back = widths[-1]
    h_back = y_top * 0.85 
    z_inner_back = z_offset
    z_outer_back = z_offset + side * w_back
    
    glNormal3f(-1, 0, 0)
    draw_quad(
        (x_back, h_back, z_outer_back),
        (x_back, h_back, z_inner_back),
        (x_back, y_bottom, z_inner_back),
        (x_back, y_bottom, z_outer_back)
    )

def draw_sidepods():
    draw_sidepod(1)
    draw_sidepod(-1)

# COCKPIT E HALO
def draw_cockpit():
    pass

def draw_halo():
    glColor3f(0.08, 0.08, 0.08)
    
    cockpit_x = 0.55
    cockpit_y = 0.12
    
    front_base_x = 1.05
    front_base_y = 0.02
    front_top_x = 0.70
    front_top_y = 0.38
    pillar_width_base = 0.06
    pillar_width_top = 0.04
    pillar_depth = 0.035
    
    glBegin(GL_QUADS)
    glNormal3f(0.7, 0.7, 0)
    glVertex3f(front_base_x, front_base_y, -pillar_width_base)
    glVertex3f(front_base_x, front_base_y, pillar_width_base)
    glVertex3f(front_top_x, front_top_y, pillar_width_top)
    glVertex3f(front_top_x, front_top_y, -pillar_width_top)
    glEnd()
    
    glBegin(GL_QUADS)
    glNormal3f(-0.7, -0.7, 0)
    glVertex3f(front_base_x - pillar_depth, front_base_y, pillar_width_base)
    glVertex3f(front_base_x - pillar_depth, front_base_y, -pillar_width_base)
    glVertex3f(front_top_x - pillar_depth * 0.7, front_top_y, -pillar_width_top)
    glVertex3f(front_top_x - pillar_depth * 0.7, front_top_y, pillar_width_top)
    glEnd()
    
    for side in [-1, 1]:
        glBegin(GL_QUADS)
        glNormal3f(0, 0, side)
        glVertex3f(front_base_x, front_base_y, side * pillar_width_base)
        glVertex3f(front_base_x - pillar_depth, front_base_y, side * pillar_width_base)
        glVertex3f(front_top_x - pillar_depth * 0.7, front_top_y, side * pillar_width_top)
        glVertex3f(front_top_x, front_top_y, side * pillar_width_top)
        glEnd()
    
    arc_center_x = 0.35
    arc_center_y = 0.38
    arc_radius_x = 0.38
    arc_radius_z = 0.28
    arc_thickness = 0.032
    arc_height = 0.025
    num_segments = 32
    
    for i in range(num_segments):
        angle1 = 2 * math.pi * i / num_segments
        angle2 = 2 * math.pi * (i + 1) / num_segments
        
        x1 = arc_center_x + math.cos(angle1) * arc_radius_x
        z1 = math.sin(angle1) * arc_radius_z
        x2 = arc_center_x + math.cos(angle2) * arc_radius_x
        z2 = math.sin(angle2) * arc_radius_z
        
        height_var1 = 0.015 * abs(math.sin(angle1))
        height_var2 = 0.015 * abs(math.sin(angle2))
        y1 = arc_center_y + height_var1
        y2 = arc_center_y + height_var2
        
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(x1, y1 + arc_height, z1 - arc_thickness * 0.5)
        glVertex3f(x1, y1 + arc_height, z1 + arc_thickness * 0.5)
        glVertex3f(x2, y2 + arc_height, z2 + arc_thickness * 0.5)
        glVertex3f(x2, y2 + arc_height, z2 - arc_thickness * 0.5)
        glEnd()
        
        glBegin(GL_QUADS)
        glNormal3f(0, -1, 0)
        glVertex3f(x1, y1, z1 + arc_thickness * 0.5)
        glVertex3f(x1, y1, z1 - arc_thickness * 0.5)
        glVertex3f(x2, y2, z2 - arc_thickness * 0.5)
        glVertex3f(x2, y2, z2 + arc_thickness * 0.5)
        glEnd()
        
        glBegin(GL_QUADS)
        nx1 = math.cos(angle1)
        nz1 = math.sin(angle1)
        nx2 = math.cos(angle2)
        nz2 = math.sin(angle2)
        glNormal3f((nx1 + nx2) * 0.5, 0, (nz1 + nz2) * 0.5)
        glVertex3f(x1, y1, z1 + arc_thickness * 0.5)
        glVertex3f(x1, y1 + arc_height, z1 + arc_thickness * 0.5)
        glVertex3f(x2, y2 + arc_height, z2 + arc_thickness * 0.5)
        glVertex3f(x2, y2, z2 + arc_thickness * 0.5)
        glEnd()
        
        glBegin(GL_QUADS)
        glNormal3f(-(nx1 + nx2) * 0.5, 0, -(nz1 + nz2) * 0.5)
        glVertex3f(x1, y1 + arc_height, z1 - arc_thickness * 0.5)
        glVertex3f(x1, y1, z1 - arc_thickness * 0.5)
        glVertex3f(x2, y2, z2 - arc_thickness * 0.5)
        glVertex3f(x2, y2 + arc_height, z2 - arc_thickness * 0.5)
        glEnd()
    
    for side in [-1, 1]:
        back_base_x = 0.05
        back_base_y = 0.12
        back_base_z = side * 0.22
        back_top_x = arc_center_x - arc_radius_x * 0.95
        back_top_y = arc_center_y
        back_top_z = side * arc_radius_z * 0.95
        back_width = 0.025
        back_depth = 0.030

        glBegin(GL_QUADS)
        glNormal3f(0, 0, side)
        glVertex3f(back_base_x, back_base_y, back_base_z)
        glVertex3f(back_base_x - back_depth, back_base_y, back_base_z)
        glVertex3f(back_top_x - back_depth * 0.8, back_top_y, back_top_z)
        glVertex3f(back_top_x, back_top_y, back_top_z)
        glEnd()
        
        glBegin(GL_QUADS)
        glNormal3f(0, 0, -side)
        glVertex3f(back_base_x - back_depth, back_base_y, back_base_z - side * back_width)
        glVertex3f(back_base_x, back_base_y, back_base_z - side * back_width)
        glVertex3f(back_top_x, back_top_y, back_top_z - side * back_width * 0.8)
        glVertex3f(back_top_x - back_depth * 0.8, back_top_y, back_top_z - side * back_width * 0.8)
        glEnd()
        
        glBegin(GL_QUADS)
        glNormal3f(1, 0, 0)
        glVertex3f(back_base_x, back_base_y, back_base_z - side * back_width)
        glVertex3f(back_base_x, back_base_y, back_base_z)
        glVertex3f(back_top_x, back_top_y, back_top_z)
        glVertex3f(back_top_x, back_top_y, back_top_z - side * back_width * 0.8)
        glEnd()
        
        glBegin(GL_QUADS)
        glNormal3f(-1, 0, 0)
        glVertex3f(back_base_x - back_depth, back_base_y, back_base_z)
        glVertex3f(back_base_x - back_depth, back_base_y, back_base_z - side * back_width)
        glVertex3f(back_top_x - back_depth * 0.8, back_top_y, back_top_z - side * back_width * 0.8)
        glVertex3f(back_top_x - back_depth * 0.8, back_top_y, back_top_z)
        glEnd()

# ASA DIANTEIRA
def draw_front_wing():
    x_base = 3.2
    y_base = -0.16
    wing_half_width = 0.95
    
    def draw_wing_element(y_offset, thickness, chord_front, chord_back, angle, color):
        glColor3f(*color)
        
        num_sections = 12
        
        glBegin(GL_QUAD_STRIP)
        for i in range(num_sections + 1):
            t = i / num_sections
            z = -wing_half_width + t * 2 * wing_half_width
            t_center = abs(t - 0.5) * 2
            arch = -0.06 * (1 - t_center ** 1.2)
            x_trailing = x_base + chord_back
            x_leading = x_base - chord_front * (1 + t_center * 0.4)
            y_top = y_base + y_offset + arch
            y_leading_adj = y_top + math.sin(math.radians(angle)) * chord_front
            glNormal3f(0, 1, 0)
            glVertex3f(x_trailing, y_top, z)
            glVertex3f(x_leading, y_leading_adj, z)
        glEnd()
        
        glBegin(GL_QUAD_STRIP)
        for i in range(num_sections + 1):
            t = i / num_sections
            z = -wing_half_width + t * 2 * wing_half_width
            
            t_center = abs(t - 0.5) * 2
            arch = -0.06 * (1 - t_center ** 1.2)
            
            x_trailing = x_base + chord_back
            x_leading = x_base - chord_front * (1 + t_center * 0.4)
            
            y_top = y_base + y_offset + arch
            y_bot = y_top - thickness
            y_leading_adj = y_bot + math.sin(math.radians(angle)) * chord_front
            
            glNormal3f(0, -1, 0)
            glVertex3f(x_leading, y_leading_adj, z)
            glVertex3f(x_trailing, y_bot, z)
        glEnd()
    
    draw_wing_element(0, 0.025, 0.25, 0.35, 5, (0.08, 0.08, 0.08))
    draw_wing_element(0.045, 0.02, 0.18, 0.28, 12, (0.08, 0.08, 0.08))
    draw_wing_element(0.085, 0.018, 0.12, 0.22, 20, (0.08, 0.08, 0.08))
    draw_wing_element(0.12, 0.015, 0.08, 0.15, 28, (0.08, 0.08, 0.08))
    
    for side in [-1, 1]:
        glColor3f(0.06, 0.06, 0.06)
        z_pos = side * wing_half_width
        
        glPushMatrix()
        glTranslatef(x_base - 0.05, y_base + 0.08, z_pos)
        
        glBegin(GL_QUADS)
        glNormal3f(0, 0, side)
        glVertex3f(0.35, 0.12, 0)
        glVertex3f(0.35, -0.08, 0)
        glVertex3f(-0.40, -0.08, 0)
        glVertex3f(-0.40, 0.18, 0)
        glEnd()
        
        glBegin(GL_QUADS)
        glNormal3f(0, 0, -side)
        glVertex3f(-0.40, 0.18, -side * 0.02)
        glVertex3f(-0.40, -0.08, -side * 0.02)
        glVertex3f(0.35, -0.08, -side * 0.02)
        glVertex3f(0.35, 0.12, -side * 0.02)
        glEnd()
        
        glColor3f(0.10, 0.10, 0.10)
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(0.35, 0.12, 0)
        glVertex3f(-0.40, 0.18, 0)
        glVertex3f(-0.40, 0.18, -side * 0.02)
        glVertex3f(0.35, 0.12, -side * 0.02)
        glEnd()
        
        glBegin(GL_QUADS)
        glNormal3f(1, 0, 0)
        glVertex3f(0.35, 0.12, 0)
        glVertex3f(0.35, 0.12, -side * 0.02)
        glVertex3f(0.35, -0.08, -side * 0.02)
        glVertex3f(0.35, -0.08, 0)
        glEnd()
        
        glPopMatrix()
        
        glColor3f(0, 0.85, 0.80)
        glPushMatrix()
        glTranslatef(x_base - 0.05, y_base + 0.22, z_pos - side * 0.01)
        glScalef(0.70, 0.02, 0.025)
        draw_solid_cube(1)
        glPopMatrix()
    
    glColor3f(0.08, 0.08, 0.08)
    
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(x_base - 0.15, y_base + 0.02, side * 0.06)
        glScalef(0.08, 0.06, 0.03)
        draw_solid_cube(1)
        glPopMatrix()
    
    glPushMatrix()
    glTranslatef(x_base - 0.1, y_base + 0.02, 0)
    glScalef(0.12, 0.06, 0.04)
    draw_solid_cube(1)
    glPopMatrix()
    
    glColor3f(0, 0.85, 0.80)
    glPushMatrix()
    glTranslatef(x_base - 0.05, y_base + 0.005, 0)
    glScalef(0.50, 0.008, 0.30)
    draw_solid_cube(1)
    glPopMatrix()

# ASSOALHO E DIFUSOR
def draw_floor():
    glColor3f(0.06, 0.06, 0.06)
    y = -0.22
    
    glNormal3f(0, -1, 0)
    glBegin(GL_QUADS)
    glVertex3f(2.0, y, -0.55)
    glVertex3f(2.0, y, 0.55)
    glVertex3f(-1.5, y, 0.55)
    glVertex3f(-1.5, y, -0.55)
    glEnd()
    
    glColor3f(0.08, 0.08, 0.08)
    for side in [-1, 1]:
        glBegin(GL_QUADS)
        glVertex3f(1.8, y, side * 0.55)
        glVertex3f(1.8, y, side * 0.75)
        glVertex3f(-0.5, y, side * 0.75)
        glVertex3f(-0.5, y, side * 0.55)
        glEnd()

def draw_diffuser():
    glColor3f(0.05, 0.05, 0.05)
    
    for i in range(7):
        offset = (i - 3) * 0.12
        glPushMatrix()
        glTranslatef(-1.6, -0.15, offset)
        glRotatef(25, 0, 0, 1)
        glScalef(0.35, 0.02, 0.08)
        draw_solid_cube(1)
        glPopMatrix()

# DETALHES VISUAIS
def draw_turquoise_accents():
    glColor3f(0, 0.85, 0.80)
    
    glPushMatrix()
    glTranslatef(2.5, -0.02, 0)
    glScalef(0.6, 0.02, 0.12)
    draw_solid_cube(1)
    glPopMatrix()
    
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0.2, 0.10, side * 0.52)
        glScalef(1.2, 0.015, 0.02)
        draw_solid_cube(1)
        glPopMatrix()

def draw_airbox():
    glColor3f(0.10, 0.10, 0.10)
    
    glPushMatrix()
    glTranslatef(-0.1, 0.30, 0)
    
    glBegin(GL_QUADS)
    glVertex3f(0.15, 0, -0.12)
    glVertex3f(0.15, 0, 0.12)
    glVertex3f(0.15, 0.25, 0.08)
    glVertex3f(0.15, 0.25, -0.08)
    glVertex3f(-0.15, 0, 0.12)
    glVertex3f(-0.15, 0, -0.12)
    glVertex3f(-0.15, 0.18, -0.06)
    glVertex3f(-0.15, 0.18, 0.06)
    glEnd()
    
    glBegin(GL_QUADS)
    glVertex3f(0.15, 0.25, -0.08)
    glVertex3f(0.15, 0.25, 0.08)
    glVertex3f(-0.15, 0.18, 0.06)
    glVertex3f(-0.15, 0.18, -0.06)
    glEnd()
    
    for side in [-1, 1]:
        z1 = side * 0.12
        z2 = side * 0.08
        z3 = side * 0.06
        glBegin(GL_POLYGON)
        glVertex3f(0.15, 0, z1)
        glVertex3f(-0.15, 0, z1)
        glVertex3f(-0.15, 0.18, z3)
        glVertex3f(0.15, 0.25, z2)
        glEnd()
    
    glColor3f(0.02, 0.02, 0.02)
    glPushMatrix()
    glTranslatef(0.16, 0.12, 0)
    glScalef(0.02, 0.12, 0.10)
    draw_solid_cube(1)
    glPopMatrix()
    
    glPopMatrix()

def draw_mirrors():
    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0.9, 0.22, side * 0.42)
        
        glColor3f(0.15, 0.15, 0.15)
        glRotatef(side * 35, 0, 1, 0)
        glRotatef(-15, 0, 0, 1)
        
        quadric = gluNewQuadric()
        gluCylinder(quadric, 0.012, 0.012, 0.12, 8, 1)
        gluDeleteQuadric(quadric)
        
        # Espelho
        glTranslatef(0, 0, 0.12)
        glColor3f(0.5, 0.5, 0.55)
        glScalef(0.06, 0.04, 0.015)
        draw_solid_cube(1)
        
        glPopMatrix()

# ASA TRASEIRA
def draw_rear_wing(drs_open=0):
    x_base = -1.90
    y_base = 0.42
    wing_half_width = 0.48
    main_plane_chord = 0.35
    flap_chord = 0.12
    drs_angle = drs_open * 25
    
    glColor3f(0.06, 0.06, 0.06)
    num_sections = 16
    main_thickness = 0.025
    
    glBegin(GL_QUAD_STRIP)
    for i in range(num_sections + 1):
        t = i / num_sections
        z = -wing_half_width + t * 2 * wing_half_width
        t_center = abs(t - 0.5) * 2
        arch = 0.02 * t_center * t_center
        x_front = x_base + main_plane_chord * 0.3
        x_back = x_base - main_plane_chord * 0.7
        y_pos = y_base + arch
        y_front = y_pos + 0.08
        y_back = y_pos
        glNormal3f(0, 1, 0)
        glVertex3f(x_front, y_front, z)
        glVertex3f(x_back, y_back, z)
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    for i in range(num_sections + 1):
        t = i / num_sections
        z = -wing_half_width + t * 2 * wing_half_width
        t_center = abs(t - 0.5) * 2
        arch = 0.02 * t_center * t_center
        x_front = x_base + main_plane_chord * 0.3
        x_back = x_base - main_plane_chord * 0.7
        y_pos = y_base + arch - main_thickness
        y_front = y_pos + 0.08
        y_back = y_pos
        glNormal3f(0, -1, 0)
        glVertex3f(x_back, y_back, z)
        glVertex3f(x_front, y_front, z)
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    for i in range(num_sections + 1):
        t = i / num_sections
        z = -wing_half_width + t * 2 * wing_half_width
        t_center = abs(t - 0.5) * 2
        arch = 0.02 * t_center * t_center
        x_front = x_base + main_plane_chord * 0.3
        y_top = y_base + arch + 0.08
        y_bot = y_top - main_thickness
        glNormal3f(1, 0, 0)
        glVertex3f(x_front, y_top, z)
        glVertex3f(x_front, y_bot, z)
    glEnd()
    
    glPushMatrix()
    pivot_x = x_base - main_plane_chord * 0.5
    pivot_y = y_base + 0.04
    glTranslatef(pivot_x, pivot_y, 0)
    glRotatef(-drs_angle, 0, 0, 1)
    glTranslatef(-pivot_x, -pivot_y, 0)
    
    flap_y_offset = 0.06
    flap_thickness = 0.018
    
    glBegin(GL_QUAD_STRIP)
    for i in range(num_sections + 1):
        t = i / num_sections
        z = -wing_half_width + t * 2 * wing_half_width
        t_center = abs(t - 0.5) * 2
        arch = 0.02 * t_center * t_center
        x_front = x_base - main_plane_chord * 0.4
        x_back = x_base - main_plane_chord * 0.4 - flap_chord
        y_pos = y_base + flap_y_offset + arch
        y_front = y_pos + 0.03
        y_back = y_pos
        glNormal3f(0, 1, 0)
        glVertex3f(x_front, y_front, z)
        glVertex3f(x_back, y_back, z)
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    for i in range(num_sections + 1):
        t = i / num_sections
        z = -wing_half_width + t * 2 * wing_half_width
        t_center = abs(t - 0.5) * 2
        arch = 0.02 * t_center * t_center
        x_front = x_base - main_plane_chord * 0.4
        x_back = x_base - main_plane_chord * 0.4 - flap_chord
        y_pos = y_base + flap_y_offset + arch - flap_thickness
        y_front = y_pos + 0.03
        y_back = y_pos
        glNormal3f(0, -1, 0)
        glVertex3f(x_back, y_back, z)
        glVertex3f(x_front, y_front, z)
    glEnd()
    glPopMatrix()
    
    for side in [-1, 1]:
        glColor3f(0.06, 0.06, 0.06)
        z_pos = side * wing_half_width
        
        glPushMatrix()
        glTranslatef(x_base, y_base, z_pos)
        
        glBegin(GL_POLYGON)
        glNormal3f(0, 0, side)
        glVertex3f(0.15, 0.15, 0)
        glVertex3f(0.15, -0.10, 0)
        glVertex3f(-0.10, -0.35, 0)
        glVertex3f(-0.30, -0.35, 0)
        glVertex3f(-0.35, -0.20, 0)
        glVertex3f(-0.35, 0.08, 0)
        glVertex3f(-0.20, 0.12, 0)
        glEnd()
        
        glBegin(GL_POLYGON)
        glNormal3f(0, 0, -side)
        glVertex3f(-0.20, 0.12, -side * 0.03)
        glVertex3f(-0.35, 0.08, -side * 0.03)
        glVertex3f(-0.35, -0.20, -side * 0.03)
        glVertex3f(-0.30, -0.35, -side * 0.03)
        glVertex3f(-0.10, -0.35, -side * 0.03)
        glVertex3f(0.15, -0.10, -side * 0.03)
        glVertex3f(0.15, 0.15, -side * 0.03)
        glEnd()
        
        glColor3f(0.08, 0.08, 0.08)
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(0.15, 0.15, 0)
        glVertex3f(-0.20, 0.12, 0)
        glVertex3f(-0.20, 0.12, -side * 0.03)
        glVertex3f(0.15, 0.15, -side * 0.03)
        glEnd()
        
        glPopMatrix()
        
        glColor3f(0, 0.85, 0.80)
        glPushMatrix()
        glTranslatef(x_base - 0.02, y_base + 0.14, z_pos - side * 0.015)
        glScalef(0.32, 0.015, 0.02)
        draw_solid_cube(1)
        glPopMatrix()
    
    glColor3f(0.08, 0.08, 0.08)
    
    for side in [-1, 1]:
        glPushMatrix()
        base_x = -1.7
        base_y = 0.10
        base_z = side * 0.08
        top_x = x_base - 0.05
        top_y = y_base - 0.02
        top_z = side * 0.15
        dx = top_x - base_x
        dy = top_y - base_y
        dz = top_z - base_z
        length = math.sqrt(dx*dx + dy*dy + dz*dz)
        glTranslatef(base_x, base_y, base_z)
        angle_y = math.degrees(math.atan2(dx, dy))
        angle_horiz = math.degrees(math.atan2(dz, math.sqrt(dx*dx + dy*dy)))
        glRotatef(angle_y, 0, 0, -1)
        glRotatef(angle_horiz * side, 1, 0, 0)
        quadric = gluNewQuadric()
        gluCylinder(quadric, 0.025, 0.02, length, 12, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
    
    glColor3f(0.06, 0.06, 0.06)
    beam_y = y_base - 0.32
    beam_width = wing_half_width * 0.9
    
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(x_base + 0.05, beam_y, -beam_width)
    glVertex3f(x_base + 0.05, beam_y, beam_width)
    glVertex3f(x_base - 0.15, beam_y, beam_width)
    glVertex3f(x_base - 0.15, beam_y, -beam_width)
    glEnd()
    
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glVertex3f(x_base - 0.15, beam_y - 0.015, -beam_width)
    glVertex3f(x_base - 0.15, beam_y - 0.015, beam_width)
    glVertex3f(x_base + 0.05, beam_y - 0.015, beam_width)
    glVertex3f(x_base + 0.05, beam_y - 0.015, -beam_width)
    glEnd()
    
    glColor3f(0.3, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(x_base - 0.36, y_base - 0.05, 0)
    glScalef(0.02, 0.04, 0.12)
    draw_solid_cube(1)
    glPopMatrix()

# SUSPENSÃO
def draw_suspension_bar(start, end, thickness=0.02):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dz = end[2] - start[2]
    length = math.sqrt(dx*dx + dy*dy + dz*dz)
    
    if length < 0.001:
        return
    
    dirx, diry, dirz = dx/length, dy/length, dz/length

    perpx = diry * 0 - dirz * 1
    perpy = dirz * 0 - dirx * 0  
    perpz = dirx * 1 - diry * 0
    perp_len = math.sqrt(perpx*perpx + perpy*perpy + perpz*perpz)
    
    if perp_len < 0.001:
        perpx, perpy, perpz = 1, 0, 0
    else:
        perpx, perpy, perpz = perpx/perp_len, perpy/perp_len, perpz/perp_len
    
    t = thickness / 2
    
    glBegin(GL_QUADS)
    
    glNormal3f(0, 1, 0)
    glVertex3f(start[0] - perpx*t, start[1] + t, start[2] - perpz*t)
    glVertex3f(start[0] + perpx*t, start[1] + t, start[2] + perpz*t)
    glVertex3f(end[0] + perpx*t, end[1] + t, end[2] + perpz*t)
    glVertex3f(end[0] - perpx*t, end[1] + t, end[2] - perpz*t)
    
    glNormal3f(0, -1, 0)
    glVertex3f(start[0] + perpx*t, start[1] - t, start[2] + perpz*t)
    glVertex3f(start[0] - perpx*t, start[1] - t, start[2] - perpz*t)
    glVertex3f(end[0] - perpx*t, end[1] - t, end[2] - perpz*t)
    glVertex3f(end[0] + perpx*t, end[1] - t, end[2] + perpz*t)
    
    glVertex3f(start[0] + perpx*t, start[1] - t, start[2] + perpz*t)
    glVertex3f(start[0] + perpx*t, start[1] + t, start[2] + perpz*t)
    glVertex3f(end[0] + perpx*t, end[1] + t, end[2] + perpz*t)
    glVertex3f(end[0] + perpx*t, end[1] - t, end[2] + perpz*t)
    
    glVertex3f(start[0] - perpx*t, start[1] + t, start[2] - perpz*t)
    glVertex3f(start[0] - perpx*t, start[1] - t, start[2] - perpz*t)
    glVertex3f(end[0] - perpx*t, end[1] - t, end[2] - perpz*t)
    glVertex3f(end[0] - perpx*t, end[1] + t, end[2] - perpz*t)
    
    glEnd()

def draw_front_suspension():
    glColor3f(0.15, 0.15, 0.15)
    
    for side in [-1, 1]:
        upright_x = 1.9
        upright_y = -0.08
        upright_z = side * 0.70
        
        chassis_upper_front = (1.5, 0.05, side * 0.32)
        chassis_upper_rear = (1.0, 0.03, side * 0.32)
        upright_upper = (upright_x, upright_y + 0.08, upright_z)
        glColor3f(0.12, 0.12, 0.12)
        draw_suspension_bar(chassis_upper_front, upright_upper, 0.025)
        draw_suspension_bar(chassis_upper_rear, upright_upper, 0.025)
        
        chassis_lower_front = (1.5, -0.18, side * 0.32)
        chassis_lower_rear = (1.0, -0.18, side * 0.32)
        upright_lower = (upright_x, upright_y - 0.10, upright_z)
        
        glColor3f(0.10, 0.10, 0.10)
        draw_suspension_bar(chassis_lower_front, upright_lower, 0.028)
        draw_suspension_bar(chassis_lower_rear, upright_lower, 0.028)
        
        pushrod_bottom = (upright_x - 0.1, upright_y - 0.05, upright_z - side * 0.02)
        pushrod_top = (1.3, 0.08, side * 0.34)
        glColor3f(0.08, 0.08, 0.08)
        draw_suspension_bar(pushrod_bottom, pushrod_top, 0.018)
        
        glColor3f(0.18, 0.18, 0.18)
        tie_rod_inner = (1.4, -0.05, side * 0.30)
        tie_rod_outer = (upright_x, upright_y, upright_z - side * 0.02)
        draw_suspension_bar(tie_rod_inner, tie_rod_outer, 0.015)
        
        glColor3f(0.08, 0.08, 0.08)
        glPushMatrix()
        glTranslatef(upright_x, upright_y, upright_z)
        glScalef(0.05, 0.22, 0.04)
        draw_solid_cube(1)
        glPopMatrix()

def draw_rear_suspension():
    glColor3f(0.15, 0.15, 0.15)
    
    for side in [-1, 1]:
        upright_x = -1.5
        upright_y = -0.05
        upright_z = side * 0.65
        
        gearbox_upper_front = (-1.0, 0.02, side * 0.22)
        gearbox_upper_rear = (-1.6, 0.00, side * 0.18)
        upright_upper = (upright_x, upright_y + 0.08, upright_z)
        glColor3f(0.12, 0.12, 0.12)
        draw_suspension_bar(gearbox_upper_front, upright_upper, 0.025)
        draw_suspension_bar(gearbox_upper_rear, upright_upper, 0.025)
        
        gearbox_lower_front = (-1.0, -0.15, side * 0.22)
        gearbox_lower_rear = (-1.6, -0.15, side * 0.18)
        upright_lower = (upright_x, upright_y - 0.10, upright_z)
        glColor3f(0.10, 0.10, 0.10)
        draw_suspension_bar(gearbox_lower_front, upright_lower, 0.028)
        draw_suspension_bar(gearbox_lower_rear, upright_lower, 0.028)
        
        pullrod_wheel = (upright_x + 0.08, upright_y + 0.06, upright_z - side * 0.02)
        pullrod_gearbox = (-1.2, -0.12, side * 0.24)
        glColor3f(0.08, 0.08, 0.08)
        draw_suspension_bar(pullrod_wheel, pullrod_gearbox, 0.018)
        
        glColor3f(0.18, 0.18, 0.18)
        toe_inner = (-1.4, -0.08, side * 0.20)
        toe_outer = (upright_x, upright_y - 0.02, upright_z - side * 0.02)
        draw_suspension_bar(toe_inner, toe_outer, 0.015)
        
        glColor3f(0.22, 0.22, 0.25)
        shaft_inner = (-1.3, -0.05, side * 0.18)
        shaft_outer = (upright_x, upright_y, upright_z - side * 0.03)
        draw_suspension_bar(shaft_inner, shaft_outer, 0.035)
        
        glColor3f(0.08, 0.08, 0.08)
        glPushMatrix()
        glTranslatef(upright_x, upright_y, upright_z)
        glScalef(0.05, 0.22, 0.05)
        draw_solid_cube(1)
        glPopMatrix()

def draw_suspension():
    draw_front_suspension()
    draw_rear_suspension()

# RODAS
def draw_wheel(x, y, z, rotation=0, is_front=False, steer_angle=0, side=1):
    glPushMatrix()
    glTranslatef(x, y, z)

    if is_front:
        glRotatef(steer_angle, 0, 1, 0)
    glRotatef(rotation, 0, 0, 1)

    tire_radius = 0.33
    tire_width = 0.28 if is_front else 0.34
    rim_radius = 0.23
    
    if side == -1:
        glRotatef(180, 0, 1, 0)

    num_segments = 48

    glColor3f(0.06, 0.06, 0.06)
    glPushMatrix()
    glTranslatef(0, 0, -tire_width * 0.5)
    quadric = gluNewQuadric()
    gluCylinder(quadric, tire_radius, tire_radius, tire_width, 48, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    glColor3f(0.08, 0.08, 0.08)
    
    for z_side in [-1, 1]:
        z_pos = z_side * tire_width * 0.5
        glBegin(GL_QUAD_STRIP)
        for i in range(num_segments + 1):
            angle = (2 * math.pi * i) / num_segments
            x_outer = tire_radius * math.cos(angle)
            y_outer = tire_radius * math.sin(angle)
            x_inner = rim_radius * math.cos(angle)
            y_inner = rim_radius * math.sin(angle)
            glNormal3f(0, 0, z_side)
            glVertex3f(x_outer, y_outer, z_pos)
            glVertex3f(x_inner, y_inner, z_pos * 0.7)
        glEnd()

    glColor3f(0.95, 0.85, 0.0)
    stripe_inner_radius = tire_radius * 0.88
    stripe_outer_radius = tire_radius * 0.96
    
    for z_side in [-1, 1]:
        z_pos = z_side * tire_width * 0.48
        glBegin(GL_QUAD_STRIP)
        for i in range(num_segments + 1):
            angle = (2 * math.pi * i) / num_segments
            x_outer = stripe_outer_radius * math.cos(angle)
            y_outer = stripe_outer_radius * math.sin(angle)
            x_inner = stripe_inner_radius * math.cos(angle)
            y_inner = stripe_inner_radius * math.sin(angle)
            glNormal3f(0, 0, z_side)
            glVertex3f(x_outer, y_outer, z_pos)
            glVertex3f(x_inner, y_inner, z_pos)
        glEnd()

    glColor3f(0.95, 0.95, 0.95)
    for z_side in [-1, 1]:
        for i in range(8):
            angle = (math.pi * 0.25) + (i * math.pi * 0.1)
            glPushMatrix()
            glRotatef(math.degrees(angle), 0, 0, 1)
            glTranslatef(tire_radius * 0.75, 0, z_side * tire_width * 0.49)
            glScalef(0.025, 0.008, 0.005)
            draw_solid_cube(1)
            glPopMatrix()

    cover_radius = rim_radius * 0.98
    
    for z_side in [-1, 1]:
        z_offset = z_side * tire_width * 0.35
        
        glColor3f(0.25, 0.25, 0.28)
        glPushMatrix()
        glTranslatef(0, 0, z_offset)
        quadric = gluNewQuadric()
        gluDisk(quadric, 0.03, cover_radius, 32, 3)
        gluDeleteQuadric(quadric)
        glPopMatrix()
        
        glColor3f(0.08, 0.08, 0.08)
        glPushMatrix()
        glTranslatef(0, 0, z_offset * 1.01)
        quadric = gluNewQuadric()
        gluDisk(quadric, cover_radius * 0.7, cover_radius * 0.85, 32, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
        
        glColor3f(0.12, 0.12, 0.12)
        for i in range(5):
            vent_angle = (360 / 5) * i + 36
            glPushMatrix()
            glRotatef(vent_angle, 0, 0, 1)
            glTranslatef(cover_radius * 0.55, 0, z_offset * 1.02)
            glScalef(0.06, 0.025, 0.008)
            draw_solid_cube(1)
            glPopMatrix()

    glColor3f(0.7, 0.7, 0.75)
    for z_side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0, 0, z_side * tire_width * 0.38)
        quadric = gluNewQuadric()
        gluDisk(quadric, 0, 0.035, 6, 1)
        gluDeleteQuadric(quadric)
        glColor3f(0.5, 0.5, 0.55)
        glTranslatef(0, 0, z_side * 0.005)
        quadric = gluNewQuadric()
        gluDisk(quadric, 0, 0.02, 6, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    glColor3f(0.1, 0.1, 0.1)
    for z_side in [-1, 1]:
        glPushMatrix()
        glTranslatef(0, 0, z_side * tire_width * 0.35)
        quadric = gluNewQuadric()
        gluCylinder(quadric, rim_radius, rim_radius * 1.02, tire_width * 0.15 * abs(z_side), 32, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    glPopMatrix()


def draw_wheels_on_suspension(wheel_rotation=0, steer_angle=0):
    front_x = 1.9
    front_y = -0.08
    front_z = 0.70
    
    rear_x = -1.5
    rear_y = -0.05
    rear_z = 0.65
    
    draw_wheel(front_x, front_y, front_z, wheel_rotation, is_front=True, steer_angle=steer_angle, side=1)
    draw_wheel(front_x, front_y, -front_z, wheel_rotation, is_front=True, steer_angle=steer_angle, side=-1)
    
    draw_wheel(rear_x, rear_y, rear_z, wheel_rotation, is_front=False, steer_angle=0, side=1)
    draw_wheel(rear_x, rear_y, -rear_z, wheel_rotation, is_front=False, steer_angle=0, side=-1)


# FUNÇÃO PRINCIPAL
def draw_chassis(wheel_rotation=0, steer_angle=0, drs_open=0, rear_wing_vibration=0):
    draw_monocoque()
    draw_engine_cover()
    draw_nose()
    draw_sidepods()
    draw_cockpit()
    draw_halo()
    draw_floor()
    draw_diffuser()
    draw_airbox()
    draw_front_wing()
    draw_rear_wing(drs_open)
    draw_suspension()
    draw_wheels_on_suspension(wheel_rotation, steer_angle)
    draw_turquoise_accents()
    draw_mirrors()

def draw_chassis_standalone():
    draw_chassis()

# PISTA DE CORRIDA
def draw_track(track_offset=0):
    track_length = 80.0
    track_width = 8.0
    track_y = -0.56
    
    glColor3f(0.15, 0.15, 0.17)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-track_length/2, track_y, -track_width/2)
    glVertex3f(-track_length/2, track_y, track_width/2)
    glVertex3f(track_length/2, track_y, track_width/2)
    glVertex3f(track_length/2, track_y, -track_width/2)
    glEnd()
    
    glColor3f(0.95, 0.95, 0.95)
    line_width = 0.15
    
    for side in [-1, 1]:
        z_pos = side * (track_width/2 - line_width/2)
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(-track_length/2, track_y + 0.01, z_pos - line_width/2)
        glVertex3f(-track_length/2, track_y + 0.01, z_pos + line_width/2)
        glVertex3f(track_length/2, track_y + 0.01, z_pos + line_width/2)
        glVertex3f(track_length/2, track_y + 0.01, z_pos - line_width/2)
        glEnd()
    
    glColor3f(0.9, 0.9, 0.9)
    dash_length = 2.0
    dash_gap = 2.0
    dash_width = 0.12
    
    x = -track_length/2 + (track_offset % (dash_length + dash_gap))
    while x < track_length/2:
        if x + dash_length > -track_length/2:
            glBegin(GL_QUADS)
            glNormal3f(0, 1, 0)
            glVertex3f(x, track_y + 0.01, -dash_width/2)
            glVertex3f(x, track_y + 0.01, dash_width/2)
            glVertex3f(min(x + dash_length, track_length/2), track_y + 0.01, dash_width/2)
            glVertex3f(min(x + dash_length, track_length/2), track_y + 0.01, -dash_width/2)
            glEnd()
        x += dash_length + dash_gap
    
    kerb_width = 0.4
    kerb_segment_length = 1.5
    
    for side in [-1, 1]:
        z_base = side * (track_width/2 + kerb_width/2)
        x = -track_length/2 + (track_offset % (kerb_segment_length * 2))
        color_index = int((track_offset / kerb_segment_length)) % 2
        
        while x < track_length/2:
            if color_index % 2 == 0:
                glColor3f(0.9, 0.1, 0.1)
            else:
                glColor3f(0.95, 0.95, 0.95)
            
            end_x = min(x + kerb_segment_length, track_length/2)
            
            glBegin(GL_QUADS)
            glNormal3f(0, 1, 0)
            glVertex3f(x, track_y + 0.02, z_base - kerb_width/2)
            glVertex3f(x, track_y + 0.02, z_base + kerb_width/2)
            glVertex3f(end_x, track_y + 0.02, z_base + kerb_width/2)
            glVertex3f(end_x, track_y + 0.02, z_base - kerb_width/2)
            glEnd()
            
            x += kerb_segment_length
            color_index += 1
    
    glColor3f(0.15, 0.45, 0.15)
    grass_width = 15.0
    
    for side in [-1, 1]:
        z_base = side * (track_width/2 + kerb_width + grass_width/2)
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(-track_length/2, track_y - 0.01, z_base - grass_width/2)
        glVertex3f(-track_length/2, track_y - 0.01, z_base + grass_width/2)
        glVertex3f(track_length/2, track_y - 0.01, z_base + grass_width/2)
        glVertex3f(track_length/2, track_y - 0.01, z_base - grass_width/2)
        glEnd()
    
    glColor3f(0.95, 0.95, 0.95)
    start_x = -25.0
    start_width = 0.5
    
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(start_x, track_y + 0.02, -track_width/2 + line_width)
    glVertex3f(start_x, track_y + 0.02, track_width/2 - line_width)
    glVertex3f(start_x + start_width, track_y + 0.02, track_width/2 - line_width)
    glVertex3f(start_x + start_width, track_y + 0.02, -track_width/2 + line_width)
    glEnd()
    
    finish_x = 25.0
    checker_size = 0.3
    num_checkers_z = int((track_width - 2*line_width) / checker_size)
    num_checkers_x = 3
    
    for i in range(num_checkers_x):
        for j in range(num_checkers_z):
            if (i + j) % 2 == 0:
                glColor3f(0.1, 0.1, 0.1)
            else:
                glColor3f(0.95, 0.95, 0.95)
            
            x1 = finish_x + i * checker_size
            z1 = -track_width/2 + line_width + j * checker_size
            
            glBegin(GL_QUADS)
            glNormal3f(0, 1, 0)
            glVertex3f(x1, track_y + 0.02, z1)
            glVertex3f(x1, track_y + 0.02, z1 + checker_size)
            glVertex3f(x1 + checker_size, track_y + 0.02, z1 + checker_size)
            glVertex3f(x1 + checker_size, track_y + 0.02, z1)
            glEnd()

def draw_scene():
    global track_line_offset
    
    draw_track(track_line_offset)
    
    draw_chassis(wheel_rotation, steer_angle, drs_open, 0)

# CONTROLES E ANIMAÇÃO
def update_animation(dt):
    global animation_running, wheel_rotation, track_line_offset
    global drs_open, steer_angle
    
    if not animation_running:
        return
    
    car_speed = 15.0
    
    wheel_rotation -= car_speed * 50 * dt
    if wheel_rotation < 0:
        wheel_rotation += 360
    
    track_line_offset -= car_speed * dt
    if track_line_offset < -100:
        track_line_offset += 100
    
    drs_open += (1.0 - drs_open) * 3.0 * dt
    
    steer_angle = math.sin(pygame.time.get_ticks() * 0.015) * 2.0

def toggle_animation():
    global animation_running, drs_open, steer_angle
    
    animation_running = not animation_running
    
    if not animation_running:
        drs_open = 0.0
        steer_angle = 0.0

def draw_text_opengl(x, y, text, color=(1, 1, 1)):
    glColor3f(*color)
    glRasterPos2f(x, y)
    try:
        for char in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    except:
        pass

def draw_hud_opengl(width, height):
    global animation_running, drs_open
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    
    if animation_running:
        status = "CORRENDO! Pressione SPACE para parar"
        color = (0, 1, 0.4)
    else:
        status = "Pressione SPACE para comecar a correr"
        color = (1, 1, 0)
    
    draw_text_opengl(20, height - 30, status, color)
    
    draw_text_opengl(20, height - 60, "SPACE - Correr/Parar | Setas - Camera | ESC - Sair", (0.7, 0.7, 0.7))
    
    if animation_running:
        drs_status = "DRS: ABERTO" if drs_open > 0.5 else "DRS: ABRINDO..."
        drs_color = (0, 1, 0) if drs_open > 0.5 else (1, 0.8, 0)
        draw_text_opengl(width - 180, height - 30, drs_status, drs_color)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

# FUNÇÃO PRINCIPAL
def main():
    global camera_angle_y, camera_angle_x, camera_distance
    global animation_running
    
    glutInit(sys.argv)
    
    pygame.init()
    
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("F1 Mercedes W16 - Animacao na Pista")
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [5, 10, 5, 0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1])
    
    glLightfv(GL_LIGHT1, GL_POSITION, [-5, 8, -5, 0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.6, 0.6, 0.6, 1])
    
    glClearColor(0.4, 0.6, 0.9, 1)  # Céu azul
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, display[0]/display[1], 0.1, 200)
    glMatrixMode(GL_MODELVIEW)
    
    mouse_dragging = False
    last_mouse_pos = (0, 0)
    clock = pygame.time.Clock()
    
    print("\n" + "="*50)
    print("  F1 Mercedes W16 - Simulacao de Corrida")
    print("="*50)
    print("  SPACE - Iniciar/Parar animacao")
    print("  Setas/Mouse - Rotacionar camera")
    print("  +/- ou Scroll - Zoom")
    print("  ESC - Sair")
    print("="*50 + "\n")
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    toggle_animation()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    camera_distance = max(3, camera_distance - 1)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    camera_distance = min(30, camera_distance + 1)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    mouse_dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:  # Scroll up
                    camera_distance = max(3, camera_distance - 0.5)
                elif event.button == 5:  # Scroll down
                    camera_distance = min(30, camera_distance + 0.5)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if mouse_dragging:
                    current_pos = pygame.mouse.get_pos()
                    dx = current_pos[0] - last_mouse_pos[0]
                    dy = current_pos[1] - last_mouse_pos[1]
                    camera_angle_y += dx * 0.5
                    camera_angle_x += dy * 0.3
                    camera_angle_x = max(-80, min(80, camera_angle_x))
                    last_mouse_pos = current_pos
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera_angle_y -= 60 * dt
        if keys[pygame.K_RIGHT]:
            camera_angle_y += 60 * dt
        if keys[pygame.K_UP]:
            camera_angle_x = max(-80, camera_angle_x - 40 * dt)
        if keys[pygame.K_DOWN]:
            camera_angle_x = min(80, camera_angle_x + 40 * dt)
        
        update_animation(dt)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        cam_offset_x = camera_distance * math.cos(math.radians(camera_angle_x)) * math.sin(math.radians(camera_angle_y))
        cam_offset_y = camera_distance * math.sin(math.radians(camera_angle_x))
        cam_offset_z = camera_distance * math.cos(math.radians(camera_angle_x)) * math.cos(math.radians(camera_angle_y))
        
        gluLookAt(
            cam_offset_x, abs(cam_offset_y) + 2, cam_offset_z,
            0, 0, 0,
            0, 1, 0
        )
        
        draw_scene()
        draw_hud_opengl(display[0], display[1])
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

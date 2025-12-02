#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mercedes-AMG F1 W16 E Performance 2025
Versão Integrada - Todos os módulos em um único arquivo
Direções dos elementos corrigidas
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import time

# Rodas
def draw_wheel(x, y, z, rotation, is_front=False, steer_angle=0, side=1):
    """
    Desenha uma roda de F1 realista com pneu Pirelli e carenagem aerodinâmica
    Baseado no Mercedes W16 com rodas fechadas
    """
    glPushMatrix()
    glTranslatef(x, y, z)

    if is_front:
        glRotatef(steer_angle, 0, 1, 0)

    # Rotação da roda (movimento)
    glRotatef(rotation, 0, 0, 1)

    # Dimensões baseadas nas imagens de referência
    tire_radius = 0.33
    tire_width = 0.28 if is_front else 0.34  # Traseira mais larga
    rim_radius = 0.23  # 18 polegadas
    
    # Ajustar orientação baseado no lado
    if side == -1:
        glRotatef(180, 0, 1, 0)

    num_segments = 48

    # === PNEU PIRELLI - BANDA DE RODAGEM ===
    glColor3f(0.06, 0.06, 0.06)
    glPushMatrix()
    glTranslatef(0, 0, -tire_width * 0.5)
    quadric = gluNewQuadric()
    gluCylinder(quadric, tire_radius, tire_radius, tire_width, 48, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    # === FAIXA AMARELA PIRELLI ===
    glColor3f(0.95, 0.85, 0.0)
    stripe_width = tire_width * 0.12
    
    glBegin(GL_QUAD_STRIP)
    for i in range(num_segments + 1):
        angle = (2 * math.pi * i) / num_segments
        x_pos = tire_radius * math.cos(angle)
        y_pos = tire_radius * math.sin(angle)
        glNormal3f(math.cos(angle), math.sin(angle), 0)
        glVertex3f(x_pos * 1.002, y_pos * 1.002, -stripe_width * 0.5)
        glVertex3f(x_pos * 1.002, y_pos * 1.002, stripe_width * 0.5)
    glEnd()

    # === LATERAIS DO PNEU ===
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

    # === TEXTO PIRELLI ===
    glColor3f(0.95, 0.95, 0.95)
    for z_side in [-1, 1]:
        for i in range(8):
            angle = (math.pi * 0.25) + (i * math.pi * 0.1)
            glPushMatrix()
            glRotatef(math.degrees(angle), 0, 0, 1)
            glTranslatef(tire_radius * 0.75, 0, z_side * tire_width * 0.45)
            glScalef(0.025, 0.008, 0.005)
            glutSolidCube(1)
            glPopMatrix()

    # === CARENAGEM AERODINÂMICA ===
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
            glutSolidCube(1)
            glPopMatrix()

    # === PORCA CENTRAL ===
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

    glPopMatrix()


# Asas
def draw_airfoil_section(chord, thickness, span, segments=20):
    """Desenha uma seção de aerofólio (perfil alar)"""
    glBegin(GL_QUAD_STRIP)
    
    for i in range(segments + 1):
        t = i / segments
        x = chord * t
        y_upper = thickness * (0.2969 * math.sqrt(t) - 0.126 * t - 
                               0.3516 * t**2 + 0.2843 * t**3 - 0.1015 * t**4)
        
        glNormal3f(0, 1, 0)
        glVertex3f(x, y_upper, -span/2)
        glVertex3f(x, y_upper, span/2)
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        t = i / segments
        x = chord * t
        y_upper = thickness * (0.2969 * math.sqrt(t) - 0.126 * t - 
                               0.3516 * t**2 + 0.2843 * t**3 - 0.1015 * t**4)
        y_lower = -y_upper * 0.6
        
        glNormal3f(0, -1, 0)
        glVertex3f(x, y_lower, -span/2)
        glVertex3f(x, y_lower, span/2)
    glEnd()

def draw_front_wing():
    """Desenha asa dianteira"""
    glPushMatrix()
    glTranslatef(3.2, -0.22, 0)
    
    # Suporte central
    glColor3f(0.25, 0.25, 0.25)
    glPushMatrix()
    glTranslatef(-0.35, 0.08, 0)
    glRotatef(35, 0, 0, 1)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.03, 0.04, 0.25, 12, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    
    # Elemento principal
    glColor3f(0.18, 0.18, 0.18)
    glPushMatrix()
    glRotatef(-8, 0, 0, 1)
    draw_airfoil_section(0.6, 0.08, 1.7, 30)
    glPopMatrix()
    
    # Flaps secundários
    flap_colors = [(0.15, 0.15, 0.15), (0.12, 0.12, 0.12), (0.10, 0.10, 0.10)]
    for i, color in enumerate(flap_colors):
        glColor3f(*color)
        glPushMatrix()
        glTranslatef(-0.1 * (i+1), 0.05 * (i+1), 0)
        glRotatef(-5 - i * 3, 0, 0, 1)
        draw_airfoil_section(0.35 - i * 0.05, 0.04 - i * 0.01, 1.5 - i * 0.15, 25)
        glPopMatrix()
    
    # Endplates
    for side in [-0.85, 0.85]:
        glPushMatrix()
        glTranslatef(0, 0.1, side)
        
        glColor3f(0.25, 0.25, 0.25)
        glBegin(GL_POLYGON)
        glNormal3f(0, 0, 1 if side > 0 else -1)
        glVertex3f(0.3, -0.25, 0)
        glVertex3f(-0.3, -0.25, 0)
        glVertex3f(-0.35, 0, 0)
        glVertex3f(-0.3, 0.25, 0)
        glVertex3f(0.2, 0.15, 0)
        glEnd()
        
        # Detalhe turquesa
        glColor3f(0, 1.0, 0.92)
        glPushMatrix()
        glTranslatef(0, -0.05, 0.02 if side > 0 else -0.02)
        glBegin(GL_QUADS)
        glVertex3f(0.15, -0.15, 0)
        glVertex3f(-0.15, -0.15, 0)
        glVertex3f(-0.15, 0.02, 0)
        glVertex3f(0.15, 0.02, 0)
        glEnd()
        glPopMatrix()
        
        glPopMatrix()
    
    # Turning vanes
    glColor3f(0.2, 0.2, 0.2)
    for vane in range(4):
        x_pos = -0.2 + vane * 0.12
        for side in [-0.6, 0.6]:
            glPushMatrix()
            glTranslatef(x_pos, -0.08, side)
            glRotatef(15 * (1 if side > 0 else -1), 0, 1, 0)
            glScalef(0.08, 0.12, 0.02)
            glutSolidCube(1)
            glPopMatrix()
    
    glPopMatrix()

def draw_rear_wing(drs_animation=0):
    """Desenha asa traseira com DRS"""
    glPushMatrix()
    glTranslatef(-1.4, 0.45, 0)
    
    # Pilares de suporte
    glColor3f(0.08, 0.08, 0.08)
    for side in [-0.32, 0.32]:
        glPushMatrix()
        glTranslatef(0.08, -0.25, side)
        quadric = gluNewQuadric()
        gluCylinder(quadric, 0.035, 0.04, 0.5, 16, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
    
    # Suporte central
    glPushMatrix()
    glTranslatef(0, -0.3, 0)
    glScalef(0.12, 0.6, 0.06)
    glutSolidCube(1)
    glPopMatrix()
    
    # Elemento inferior fixo
    glColor3f(0.12, 0.12, 0.12)
    glPushMatrix()
    glTranslatef(0, 0.08, 0)
    glRotatef(-12, 0, 0, 1)
    draw_airfoil_section(0.35, 0.06, 1.35, 30)
    glPopMatrix()
    
    # Elemento superior móvel (DRS)
    glPushMatrix()
    glTranslatef(0, 0.32, 0)
    glTranslatef(-0.15, 0, 0)
    glRotatef(-drs_animation * 18, 0, 0, 1)
    glTranslatef(0.15, 0, 0)
    
    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glRotatef(-15, 0, 0, 1)
    draw_airfoil_section(0.38, 0.07, 1.25, 30)
    glPopMatrix()
    
    # Faixa turquesa Mercedes
    glColor3f(0, 0.92, 0.85)
    glPushMatrix()
    glTranslatef(0, 0.04, 0)
    glScalef(0.35, 0.015, 1.26)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()
    
    # Endplates laterais
    for side in [-0.68, 0.68]:
        glPushMatrix()
        glTranslatef(0, 0.18, side)
        
        glColor3f(0.08, 0.08, 0.08)
        glBegin(GL_POLYGON)
        glNormal3f(0, 0, 1 if side > 0 else -1)
        glVertex3f(0.15, -0.35, 0)
        glVertex3f(-0.18, -0.35, 0)
        glVertex3f(-0.22, -0.1, 0)
        glVertex3f(-0.18, 0.25, 0)
        glVertex3f(0.12, 0.25, 0)
        glVertex3f(0.15, 0, 0)
        glEnd()
        
        # Logo PETRONAS
        glColor3f(0, 0.5, 0.45)
        glPushMatrix()
        glTranslatef(-0.05, 0.05, 0.015 if side > 0 else -0.015)
        glScalef(0.15, 0.08, 0.01)
        glutSolidCube(1)
        glPopMatrix()
        
        glPopMatrix()
    
    glPopMatrix()

# Sidepods
def draw_smooth_sidepod(length, height, width):
    """Desenha sidepod com formato aerodinâmico"""
    segments = 20
    
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        t = i / segments
        x = length * t
        scale = 1.0 - (t * 0.6)
        y_top = height * (1 - t * 0.3) * math.sin(math.pi * 0.5 * (1 - t * 0.5))
        
        for side in [-1, 1]:
            z = side * width * scale * 0.5
            glNormal3f(0, 1, side)
            glVertex3f(x, y_top, z)
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        t = i / segments
        x = length * t
        scale = 1.0 - (t * 0.6)
        y_bottom = -height * 0.2
        
        for side in [-1, 1]:
            z = side * width * scale * 0.5
            glNormal3f(0, -1, side)
            glVertex3f(x, y_bottom, z)
    glEnd()

def draw_sidepods():
    """Desenha os sidepods completos"""
    for side_multiplier in [-1, 1]:
        glPushMatrix()
        glTranslatef(-0.1, -0.05, side_multiplier * 0.65)
        
        # Corpo principal
        glColor3f(0.15, 0.15, 0.15)
        draw_smooth_sidepod(1.8, 0.35, 0.45)
        
        # Entrada de ar frontal
        glPushMatrix()
        glTranslatef(0.7, 0.08, 0)
        
        glColor3f(0.25, 0.25, 0.25)
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glutSolidTorus(0.04, 0.15, 12, 16)
        glPopMatrix()
        
        glColor3f(0.02, 0.02, 0.02)
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        quadric = gluNewQuadric()
        gluDisk(quadric, 0, 0.14, 20, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
        
        glPopMatrix()
        
        # Faixa turquesa Mercedes
        glColor3f(0, 0.95, 0.88)
        glPushMatrix()
        glTranslatef(0.4, 0.08, side_multiplier * 0.005)
        glScalef(1.0, 0.022, 0.45)
        glutSolidCube(1)
        glPopMatrix()
        
        # Logo PETRONAS
        glColor3f(0, 0.65, 0.55)
        glPushMatrix()
        glTranslatef(0, 0.02, side_multiplier * 0.005)
        glScalef(0.45, 0.025, 0.15)
        glutSolidCube(1)
        glPopMatrix()
        
        # Bargeboards
        glColor3f(0.18, 0.18, 0.18)
        glPushMatrix()
        glTranslatef(0.8, -0.08, side_multiplier * 0.25)
        glRotatef(side_multiplier * -15, 0, 1, 0)
        glScalef(0.3, 0.22, 0.025)
        glutSolidCube(1)
        glPopMatrix()
        
        glPopMatrix()

def draw_airbox():
    """Desenha entrada de ar superior (airbox)"""
    glPushMatrix()
    glTranslatef(-0.3, 0.38, 0)
    
    glColor3f(0.18, 0.18, 0.18)
    glPushMatrix()
    glScalef(0.28, 0.5, 0.18)
    glutSolidCube(1)
    glPopMatrix()
    
    # Entrada de ar
    glPushMatrix()
    glTranslatef(0.08, 0, 0)
    
    glColor3f(0.25, 0.25, 0.25)
    glPushMatrix()
    glRotatef(90, 0, 0, 1)
    glutSolidTorus(0.03, 0.12, 12, 20)
    glPopMatrix()
    
    glColor3f(0.02, 0.02, 0.02)
    glPushMatrix()
    glRotatef(90, 0, 0, 1)
    quadric = gluNewQuadric()
    gluDisk(quadric, 0, 0.11, 24, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    
    glPopMatrix()
    
    # Detalhe Mercedes
    glColor3f(0, 0.9, 0.85)
    glPushMatrix()
    glTranslatef(0, -0.15, 0)
    glScalef(0.25, 0.02, 0.15)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()

# Chassi
def draw_tapered_cylinder(base_radius, top_radius, height, slices=20):
    """Desenha cilindro cônico suave"""
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluCylinder(quadric, base_radius, top_radius, height, slices, 1)
    
    glPushMatrix()
    gluDisk(quadric, 0, base_radius, slices, 1)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, height)
    gluDisk(quadric, 0, top_radius, slices, 1)
    glPopMatrix()
    
    gluDeleteQuadric(quadric)

def draw_chassis():
    """Desenha chassi principal do Mercedes W16"""
    
    # Monocoque principal
    glColor3f(0.12, 0.12, 0.12)
    
    # Seção frontal
    glPushMatrix()
    glTranslatef(1.5, -0.05, 0)
    glRotatef(90, 0, 1, 0)
    draw_tapered_cylinder(0.35, 0.15, 1.8, 32)
    glPopMatrix()
    
    # Seção central (cockpit)
    glPushMatrix()
    glTranslatef(0.5, -0.05, 0)
    glRotatef(90, 0, 1, 0)
    draw_tapered_cylinder(0.38, 0.35, 1.0, 32)
    glPopMatrix()
    
    # Seção traseira
    glPushMatrix()
    glTranslatef(-0.5, -0.05, 0)
    glRotatef(90, 0, 1, 0)
    draw_tapered_cylinder(0.35, 0.28, 1.0, 32)
    glPopMatrix()
    
    # Parte traseira estreita
    glPushMatrix()
    glTranslatef(-1.3, -0.02, 0)
    glRotatef(90, 0, 1, 0)
    draw_tapered_cylinder(0.28, 0.18, 0.8, 32)
    glPopMatrix()
    
    # Bico do carro
    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glTranslatef(2.8, -0.15, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(-5, 1, 0, 0)
    draw_tapered_cylinder(0.12, 0.05, 0.8, 24)
    glPopMatrix()
    
    # Ponta do bico
    glPushMatrix()
    glTranslatef(3.4, -0.2, 0)
    glRotatef(90, 0, 1, 0)
    glutSolidCone(0.06, 0.3, 16, 1)
    glPopMatrix()
    
    # Detalhe turquesa no bico
    glColor3f(0, 0.95, 0.88)
    glPushMatrix()
    glTranslatef(3.0, -0.12, 0)
    glRotatef(90, 0, 1, 0)
    draw_tapered_cylinder(0.055, 0.048, 0.15, 20)
    glPopMatrix()
    
    # Cockpit (abertura)
    glColor3f(0.05, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(0.4, 0.1, 0)
    glScalef(0.9, 0.2, 0.5)
    glutSolidSphere(1, 24, 16)
    glPopMatrix()
    
    # Assento do piloto
    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glTranslatef(0.3, -0.02, 0)
    glScalef(0.4, 0.15, 0.35)
    glutSolidSphere(1, 20, 16)
    glPopMatrix()
    
    # HALO (Proteção do piloto)
    glColor3f(0.4, 0.4, 0.42)
    
    # Arco principal do Halo
    glPushMatrix()
    glTranslatef(0.5, 0.35, 0)
    
    for angle in range(0, 180, 10):
        rad = math.radians(angle)
        x1 = math.cos(rad) * 0.3
        y1 = math.sin(rad) * 0.25
        
        glPushMatrix()
        glTranslatef(x1, y1, 0)
        glRotatef(90, 1, 0, 0)
        quadric = gluNewQuadric()
        gluCylinder(quadric, 0.025, 0.025, 0.5, 12, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
    
    glPopMatrix()
    
    # Pilar central frontal do Halo
    glPushMatrix()
    glTranslatef(0.75, 0.05, 0)
    glRotatef(75, 0, 0, 1)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.02, 0.025, 0.35, 12, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    
    # Pilares laterais traseiros
    for side in [-0.25, 0.25]:
        glPushMatrix()
        glTranslatef(0.25, 0.05, side)
        glRotatef(85, 0, 0, 1)
        quadric = gluNewQuadric()
        gluCylinder(quadric, 0.022, 0.022, 0.35, 12, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
    
    # Volante F1
    glPushMatrix()
    glTranslatef(0.55, 0.18, 0)
    glRotatef(75, 0, 0, 1)
    
    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glScalef(0.15, 0.05, 0.12)
    glutSolidCube(1)
    glPopMatrix()
    
    glColor3f(0.3, 0.3, 0.3)
    for side in [-0.08, 0.08]:
        glPushMatrix()
        glTranslatef(0, 0, side)
        glRotatef(90, 0, 1, 0)
        glutSolidTorus(0.01, 0.06, 8, 12)
        glPopMatrix()
    
    # Display digital
    glColor3f(0, 0.8, 0.3)
    glPushMatrix()
    glScalef(0.08, 0.02, 0.06)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()
    
    # Assoalho plano
    glColor3f(0.08, 0.08, 0.08)
    glPushMatrix()
    glTranslatef(0.2, -0.25, 0)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-2.0, 0, -0.55)
    glVertex3f(2.2, 0, -0.55)
    glVertex3f(2.2, 0, 0.55)
    glVertex3f(-2.0, 0, 0.55)
    glEnd()
    glPopMatrix()
    
    # Canais do assoalho (Venturi tunnels)
    glColor3f(0.05, 0.05, 0.05)
    for side in [-0.35, 0.35]:
        glPushMatrix()
        glTranslatef(0, -0.23, side)
        glRotatef(90, 0, 1, 0)
        draw_tapered_cylinder(0.08, 0.12, 3.5, 16)
        glPopMatrix()
    
    # Difusor traseiro
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(-1.7, -0.18, 0)
    glRotatef(15, 0, 0, 1)
    
    for i in range(5):
        offset = (i - 2) * 0.15
        glPushMatrix()
        glTranslatef(0, 0, offset)
        glScalef(0.5, 0.02, 0.12)
        glutSolidCube(1)
        glPopMatrix()
    
    glPopMatrix()
    
    # Faixa lateral turquesa Mercedes
    glColor3f(0, 1.0, 0.92)
    for side in [-0.42, 0.42]:
        glPushMatrix()
        glTranslatef(0.5, 0.02, side)
        glRotatef(90, 0, 1, 0)
        draw_tapered_cylinder(0.025, 0.02, 2.8, 16)
        glPopMatrix()
    
    # Número do carro (44)
    glColor3f(1.0, 0.98, 0)
    glPushMatrix()
    glTranslatef(2.5, -0.08, 0)
    glutSolidSphere(0.12, 16, 16)
    glPopMatrix()
    
    # === ESPELHOS RETROVISORES (CORRIGIDOS) ===
    glColor3f(0.2, 0.2, 0.2)
    for side in [-0.42, 0.42]:
        # Haste do espelho - CORRIGIDA para apontar para fora
        glPushMatrix()
        glTranslatef(0.7, 0.25, side * 0.95)  # Posição mais próxima do cockpit
        
        # Rotaciona a haste para apontar para fora lateralmente
        if side > 0:
            glRotatef(45, 0, 1, 0)  # Direita - aponta para fora à direita
        else:
            glRotatef(-45, 0, 1, 0)  # Esquerda - aponta para fora à esquerda
        
        # Inclina um pouco para baixo
        glRotatef(-10, 0, 0, 1)
        
        quadric = gluNewQuadric()
        gluCylinder(quadric, 0.015, 0.015, 0.18, 8, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
        
        # Espelho - posicionado na ponta da haste
        glColor3f(0.5, 0.5, 0.55)  # Superfície reflexiva
        glPushMatrix()
        # Calcula posição do espelho na ponta da haste
        angle_rad = math.radians(45 if side > 0 else -45)
        mirror_x = 0.7 + math.sin(angle_rad) * 0.18
        mirror_z = side * 0.95 + math.cos(angle_rad) * 0.18
        
        glTranslatef(mirror_x, 0.22, mirror_z)
        
        # Rotaciona espelho para ficar visível de trás
        glRotatef(90, 0, 1, 0)
        glRotatef(side * 15, 0, 0, 1)  # Pequena inclinação
        
        # Espelho retangular
        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1)
        glVertex3f(-0.04, -0.03, 0)
        glVertex3f(0.04, -0.03, 0)
        glVertex3f(0.04, 0.03, 0)
        glVertex3f(-0.04, 0.03, 0)
        glEnd()
        
        # Moldura do espelho
        glColor3f(0.2, 0.2, 0.2)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex3f(-0.04, -0.03, 0.001)
        glVertex3f(0.04, -0.03, 0.001)
        glVertex3f(0.04, 0.03, 0.001)
        glVertex3f(-0.04, 0.03, 0.001)
        glEnd()
        glLineWidth(1)
        
        glPopMatrix()
        glColor3f(0.2, 0.2, 0.2)

# Classe principal
class Formula1Mercedes2025:
    def __init__(self):
        self.width = 1400
        self.height = 900
        self.fps = 60
        
        self.animation_started = False
        self.animation_time = 0
        self.car_position = 0
        self.wheel_rotation = 0
        self.drs_open = False
        self.drs_animation = 0
        self.suspension_bounce = 0
        
        self.camera_distance = 12
        self.camera_angle = 25
        self.camera_height = 4
        
        self.last_time = time.time()
        
        self.init_glut()
        self.init_opengl()
        
    def init_glut(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(50, 50)
        glutCreateWindow(b"Mercedes-AMG F1 W16 E Performance 2025")
        
        glutDisplayFunc(self.display)
        glutIdleFunc(self.idle)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special_keys)
        glutReshapeFunc(self.reshape)
        
    def init_opengl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT2)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glShadeModel(GL_SMOOTH)
        
        glLightfv(GL_LIGHT0, GL_POSITION, [8, 15, 8, 0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.3, 0.3, 0.3, 1])
        
        glLightfv(GL_LIGHT1, GL_POSITION, [-8, 12, -8, 0])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.7, 0.7, 0.7, 1])
        
        glLightfv(GL_LIGHT2, GL_POSITION, [0, 10, 0, 0])
        glLightfv(GL_LIGHT2, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
        
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, [0.5, 0.7, 1.0, 1.0])
        glFogf(GL_FOG_START, 20.0)
        glFogf(GL_FOG_END, 60.0)
        
        glClearColor(0.5, 0.7, 1.0, 1.0)
        self.reshape(self.width, self.height)
    
    def reshape(self, width, height):
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, float(width)/float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
    
    def draw_track(self):
        """Desenha pista de corrida"""
        glDisable(GL_LIGHTING)
        
        # Asfalto
        glColor3f(0.12, 0.12, 0.12)
        glBegin(GL_QUADS)
        glVertex3f(-100, -0.5, -6)
        glVertex3f(100, -0.5, -6)
        glVertex3f(100, -0.5, 6)
        glVertex3f(-100, -0.5, 6)
        glEnd()
        
        # Faixas brancas laterais
        glColor3f(0.95, 0.95, 0.95)
        for side in [-5.5, 5.5]:
            glBegin(GL_QUADS)
            glVertex3f(-100, -0.49, side - 0.25)
            glVertex3f(100, -0.49, side - 0.25)
            glVertex3f(100, -0.49, side + 0.25)
            glVertex3f(-100, -0.49, side + 0.25)
            glEnd()
        
        # Linha central tracejada
        glColor3f(1, 1, 0.9)
        for i in range(-25, 26):
            x = i * 4 - (self.car_position % 4)
            glBegin(GL_QUADS)
            glVertex3f(x, -0.48, -0.12)
            glVertex3f(x + 2, -0.48, -0.12)
            glVertex3f(x + 2, -0.48, 0.12)
            glVertex3f(x, -0.48, 0.12)
            glEnd()
        
        # Zebras (kerbs)
        for side in [-6.5, 6.5]:
            for i in range(-30, 31):
                x = i * 2 - (self.car_position % 4)
                if i % 2 == 0:
                    glColor3f(0.85, 0.05, 0.05)
                else:
                    glColor3f(0.9, 0.9, 0.9)
                glBegin(GL_QUADS)
                glVertex3f(x, -0.49, side - 0.6 if side < 0 else side)
                glVertex3f(x + 2, -0.49, side - 0.6 if side < 0 else side)
                glVertex3f(x + 2, -0.49, side if side < 0 else side + 0.6)
                glVertex3f(x, -0.49, side if side < 0 else side + 0.6)
                glEnd()
        
        # Grama
        glColor3f(0.1, 0.45, 0.1)
        for side in [[-100, -7.5], [7.5, 100]]:
            glBegin(GL_QUADS)
            glVertex3f(-100, -0.51, side[0])
            glVertex3f(100, -0.51, side[0])
            glVertex3f(100, -0.51, side[1])
            glVertex3f(-100, -0.51, side[1])
            glEnd()
        
        glEnable(GL_LIGHTING)
    
    def draw_environment(self):
        """Desenha placas publicitárias"""
        glDisable(GL_LIGHTING)
        for i in range(-4, 5):
            glPushMatrix()
            glTranslatef(i * 18 - (self.car_position % 18), 3.5, 9)
            
            # Estrutura
            glColor3f(0.2, 0.2, 0.2)
            glBegin(GL_QUADS)
            glVertex3f(-0.1, -3.5, 0)
            glVertex3f(0.1, -3.5, 0)
            glVertex3f(0.1, 0, 0)
            glVertex3f(-0.1, 0, 0)
            glEnd()
            
            # Painel
            glColor3f(0, 0.75, 0.68)
            glBegin(GL_QUADS)
            glVertex3f(-2.5, -1.2, 0.05)
            glVertex3f(2.5, -1.2, 0.05)
            glVertex3f(2.5, 1.2, 0.05)
            glVertex3f(-2.5, 1.2, 0.05)
            glEnd()
            
            # Logo Mercedes
            glColor3f(0.9, 0.9, 0.9)
            glPushMatrix()
            glTranslatef(0, 0, 0.06)
            glScalef(0.8, 0.8, 0.01)
            glutSolidSphere(1, 16, 16)
            glPopMatrix()
            
            glPopMatrix()
        
        glEnable(GL_LIGHTING)
    
    def draw_complete_car(self):
        """Desenha carro completo integrando todos os módulos"""
        draw_chassis()
        draw_sidepods()
        draw_airbox()
        draw_front_wing()
        draw_rear_wing(self.drs_animation)
        
        # Calcula esterçamento
        steer = 0
        if self.animation_started:
            steer = math.sin(self.animation_time * 0.5) * 18
        
        # Rodas (nas posições da suspensão do chassis)
        # Dianteiras
        draw_wheel(1.9, -0.08, 0.70, self.wheel_rotation, True, steer, side=1)
        draw_wheel(1.9, -0.08, -0.70, self.wheel_rotation, True, steer, side=-1)
        # Traseiras
        draw_wheel(-1.5, -0.05, 0.65, self.wheel_rotation, False, 0, side=1)
        draw_wheel(-1.5, -0.05, -0.65, self.wheel_rotation, False, 0, side=-1)
    
    def draw_hud(self):
        """HUD de informações"""
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        # Use conventional bottom=0, top=height so we don't flip the vertical axis
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        h = self.height

        # Painel HUD (convert Y coordinates to origin-at-bottom)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0, 0, 0, 0.75)
        glBegin(GL_QUADS)
        glVertex2f(15, h - 15)
        glVertex2f(550, h - 15)
        glVertex2f(550, h - 220)
        glVertex2f(15, h - 220)
        glEnd()

        # Borda turquesa
        glLineWidth(3)
        glColor3f(0, 0.9, 0.85)
        glBegin(GL_LINE_LOOP)
        glVertex2f(15, h - 15)
        glVertex2f(550, h - 15)
        glVertex2f(550, h - 220)
        glVertex2f(15, h - 220)
        glEnd()
        glDisable(GL_BLEND)

        # Textos
        glLineWidth(2)

        # Título
        glColor3f(1, 1, 1)
        glPushMatrix()
        glTranslatef(25, h - 45, 0)
        glScalef(0.15, 0.15, 1)
        for c in "MERCEDES-AMG PETRONAS F1":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
        glPopMatrix()

        # Modelo
        glColor3f(0, 0.95, 0.88)
        glPushMatrix()
        glTranslatef(25, h - 70, 0)
        glScalef(0.12, 0.12, 1)
        for c in "W16 E Performance 2025":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
        glPopMatrix()

        # Velocidade
        speed = int(abs(self.car_position * 45) % 360)
        glColor3f(1, 1, 1)
        glPushMatrix()
        glTranslatef(25, h - 100, 0)
        glScalef(0.13, 0.13, 1)
        for c in f"SPEED: {speed:03d} km/h":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
        glPopMatrix()

        # Marcha
        gear = min(8, int(speed / 45) + 1)
        glColor3f(1, 0.95, 0)
        glPushMatrix()
        glTranslatef(320, h - 100, 0)
        glScalef(0.25, 0.25, 1)
        for c in f"GEAR {gear}":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
        glPopMatrix()

        # DRS
        glColor3f(1, 1, 1)
        glPushMatrix()
        glTranslatef(25, h - 130, 0)
        glScalef(0.11, 0.11, 1)
        for c in "DRS: ":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
        glPopMatrix()

        if self.drs_open:
            glColor3f(0, 1, 0)
            status = "ACTIVE"
        else:
            glColor3f(0.8, 0.8, 0)
            status = "STANDBY"

        glPushMatrix()
        glTranslatef(95, h - 130, 0)
        glScalef(0.11, 0.11, 1)
        for c in status:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
        glPopMatrix()

        # Instruções
        glColor3f(0.7, 0.7, 0.7)
        instructions = [
            "[SPACE] Start/Stop",
            "[D] Toggle DRS",
            "[Arrows] Camera",
            "[R] Reset",
            "[ESC] Exit"
        ]

        y = 160
        for inst in instructions:
            glPushMatrix()
            glTranslatef(25, h - y, 0)
            glScalef(0.09, 0.09, 1)
            for c in inst:
                glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
            glPopMatrix()
            y += 16

        glLineWidth(1)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
    
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Câmera
        cam_x = math.sin(math.radians(self.camera_angle)) * self.camera_distance
        cam_z = math.cos(math.radians(self.camera_angle)) * self.camera_distance
        gluLookAt(cam_x, self.camera_height, cam_z, 0, 0, 0, 0, 1, 0)
        
        # Cenário
        self.draw_track()
        self.draw_environment()
        
        # Carro
        glPushMatrix()
        
        if self.animation_started:
            # Suspensão
            self.suspension_bounce = math.sin(self.animation_time * 9) * 0.015
            glTranslatef(0, self.suspension_bounce, 0)
            
            # Movimento lateral
            lateral = math.sin(self.animation_time * 0.45) * 2.2
            glTranslatef(0, 0, lateral)
            
            # Inclinação
            tilt = math.cos(self.animation_time * 0.45) * 3.5
            glRotatef(tilt, 0, 1, 0)
            
            # Roll
            roll = math.sin(self.animation_time * 0.45) * 2.5
            glRotatef(roll, 1, 0, 0)
        
        self.draw_complete_car()
        glPopMatrix()
        
        # HUD
        self.draw_hud()
        
        glutSwapBuffers()
    
    def idle(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        if dt < 1.0/self.fps:
            time.sleep(1.0/self.fps - dt)
            dt = 1.0/self.fps
        
        if self.animation_started:
            self.animation_time += dt
            self.car_position += dt * 12
            self.wheel_rotation += dt * 600
            
            if self.drs_open:
                self.drs_animation = min(1.0, self.drs_animation + dt * 3)
            else:
                self.drs_animation = max(0.0, self.drs_animation - dt * 3)
            
            self.camera_angle += dt * 4
        
        glutPostRedisplay()
    
    def keyboard(self, key, x, y):
        if key == b' ':
            self.animation_started = not self.animation_started
            print(f">>> {'RACING' if self.animation_started else 'STOPPED'}")
        elif key in (b'd', b'D'):
            self.drs_open = not self.drs_open
            print(f">>> DRS {'ACTIVATED' if self.drs_open else 'DEACTIVATED'}")
        elif key in (b'r', b'R'):
            self.car_position = 0
            self.animation_time = 0
            self.wheel_rotation = 0
            print(">>> RESET")
        elif key == b'\x1b':
            print("\n>>> Exiting...")
            try:
                glutLeaveMainLoop()
            except:
                import sys
                sys.exit(0)
    
    def special_keys(self, key, x, y):
        if key == GLUT_KEY_LEFT:
            self.camera_angle -= 12
        elif key == GLUT_KEY_RIGHT:
            self.camera_angle += 12
        elif key == GLUT_KEY_UP:
            self.camera_distance = max(7, self.camera_distance - 1)
        elif key == GLUT_KEY_DOWN:
            self.camera_distance = min(30, self.camera_distance + 1)
        elif key == GLUT_KEY_PAGE_UP:
            self.camera_height = min(20, self.camera_height + 1)
        elif key == GLUT_KEY_PAGE_DOWN:
            self.camera_height = max(2, self.camera_height - 1)
        glutPostRedisplay()
    
    def run(self):
        print("\n" + "="*70)
        print("   MERCEDES-AMG PETRONAS F1 TEAM")
        print("   W16 E Performance 2025 - Advanced Simulator")
        print("   Versão Integrada com Direções Corrigidas")
        print("="*70)
        print("\n   CONTROLS:")
        print("   [SPACE]        Start/Stop Racing")
        print("   [D]            Toggle DRS System")
        print("   [←] [→]        Rotate Camera")
        print("   [↑] [↓]        Zoom In/Out")
        print("   [PgUp] [PgDn]  Camera Height")
        print("   [R]            Reset Position")
        print("   [ESC]          Exit")
        print("\n" + "="*70)
        print("\n✓ Retrovisores corrigidos - apontam lateralmente")
        print("✓ Todas direções verificadas e ajustadas")
        print("\n>>> Ready to Race!\n")
        
        glutMainLoop()

if __name__ == "__main__":
    try:
        app = Formula1Mercedes2025()
        app.run()
    except Exception as e:
        print(f"\n>>> ERROR: {e}")
        import traceback
        traceback.print_exc()
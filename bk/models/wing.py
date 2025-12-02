#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: Asas Aerodinâmicas F1
Asa dianteira e traseira com DRS
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

def draw_airfoil_section(chord, thickness, span, segments=20):
    """Desenha uma seção de aerofólio (perfil alar)"""
    glBegin(GL_QUAD_STRIP)
    
    for i in range(segments + 1):
        t = i / segments
        
        # Perfil NACA simplificado
        x = chord * t
        
        # Parte superior (curva)
        y_upper = thickness * (0.2969 * math.sqrt(t) - 0.126 * t - 
                               0.3516 * t**2 + 0.2843 * t**3 - 0.1015 * t**4)
        
        # Parte inferior
        y_lower = -y_upper * 0.6
        
        # Vertices superior e inferior
        glNormal3f(0, 1, 0)
        glVertex3f(x, y_upper, -span/2)
        glVertex3f(x, y_upper, span/2)
        
    glEnd()
    
    # Fechar com a parte inferior
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
    """Desenha asa dianteira complexa e realista"""
    glPushMatrix()
    glTranslatef(3.6, -0.22, 0)  # mais avançada para sair do chassi
    
    # === SUPORTE CENTRAL (conecta ao bico) ===
    glColor3f(0.25, 0.25, 0.25)
    glPushMatrix()
    glTranslatef(-0.35, 0.08, 0)
    glRotatef(35, 0, 0, 1)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.03, 0.04, 0.25, 12, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    
    # === ELEMENTO PRINCIPAL (Main Plane) ===
    glColor3f(0.18, 0.18, 0.18)
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glRotatef(-8, 0, 0, 1)  # Ângulo de ataque
    draw_airfoil_section(0.6, 0.08, 1.7, 30)
    glPopMatrix()
    
    # === ELEMENTOS SECUNDÁRIOS (Flaps) ===
    flap_colors = [
        (0.15, 0.15, 0.15),
        (0.12, 0.12, 0.12),
        (0.10, 0.10, 0.10)
    ]
    
    for i, color in enumerate(flap_colors):
        glColor3f(*color)
        glPushMatrix()
        glTranslatef(-0.1 * (i+1), 0.05 * (i+1), 0)
        glRotatef(-5 - i * 3, 0, 0, 1)
        draw_airfoil_section(0.35 - i * 0.05, 0.04 - i * 0.01, 
                            1.5 - i * 0.15, 25)
        glPopMatrix()
    
    # === ENDPLATES (Placas laterais) ===
    for side in [-0.85, 0.85]:
        glPushMatrix()
        glTranslatef(0, 0.1, side)
        
        # Endplate principal
        glColor3f(0.25, 0.25, 0.25)
        glBegin(GL_POLYGON)
        glNormal3f(0, 0, 1 if side > 0 else -1)
        glVertex3f(0.3, -0.25, 0)
        glVertex3f(-0.3, -0.25, 0)
        glVertex3f(-0.35, 0, 0)
        glVertex3f(-0.3, 0.25, 0)
        glVertex3f(0.2, 0.15, 0)
        glEnd()
        
        # Detalhe turquesa no endplate
        glColor3f(0, 1.0, 0.92)
        glPushMatrix()
        glTranslatef(0, -0.05, side > 0 and 0.02 or -0.02)
        glBegin(GL_QUADS)
        glVertex3f(0.15, -0.15, 0)
        glVertex3f(-0.15, -0.15, 0)
        glVertex3f(-0.15, 0.02, 0)
        glVertex3f(0.15, 0.02, 0)
        glEnd()
        glPopMatrix()
        
        # Slots aerodinâmicos
        glColor3f(0.05, 0.05, 0.05)
        for slot in range(3):
            glPushMatrix()
            glTranslatef(-0.15 + slot * 0.1, -0.08 + slot * 0.05, 
                        side > 0 and 0.015 or -0.015)
            glScalef(0.06, 0.15, 0.01)
            glutSolidCube(1)
            glPopMatrix()
        
        glPopMatrix()
    
    # === TURNING VANES (Defletores de fluxo) ===
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
    """
    Desenha asa traseira com sistema DRS
    
    Args:
        drs_animation: 0-1, controla abertura do DRS
    """
    glPushMatrix()
    glTranslatef(-1.55, 0.55, 0)  # avança e sobe para conectar melhor ao chassi
    
    # === PILARES DE SUPORTE ===
    glColor3f(0.08, 0.08, 0.08)
    
    # Pilares principais (conectam ao chassi)
    for side in [-0.32, 0.32]:
        glPushMatrix()
        glTranslatef(0.08, -0.25, side)
        quadric = gluNewQuadric()
        gluCylinder(quadric, 0.035, 0.04, 0.5, 16, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
    
    # Suporte central vertical
    glPushMatrix()
    glTranslatef(0, -0.3, 0)
    glScalef(0.12, 0.6, 0.06)
    glutSolidCube(1)
    glPopMatrix()
    
    # === ELEMENTO INFERIOR FIXO ===
    glColor3f(0.12, 0.12, 0.12)
    glPushMatrix()
    glTranslatef(0, 0.08, 0)
    glRotatef(-12, 0, 0, 1)
    draw_airfoil_section(0.35, 0.06, 1.35, 30)
    glPopMatrix()
    
    # === ELEMENTO SUPERIOR MÓVEL (DRS) ===
    glPushMatrix()
    glTranslatef(0, 0.32, 0)
    
    # Eixo de rotação do DRS
    glTranslatef(-0.15, 0, 0)
    glRotatef(-drs_animation * 18, 0, 0, 1)  # Abre até 18 graus
    glTranslatef(0.15, 0, 0)
    
    # Aerofólio principal
    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glRotatef(-15, 0, 0, 1)
    draw_airfoil_section(0.38, 0.07, 1.25, 30)
    glPopMatrix()
    
    # Faixa turquesa característica Mercedes
    glColor3f(0, 0.92, 0.85)
    glPushMatrix()
    glTranslatef(0, 0.04, 0)
    glScalef(0.35, 0.015, 1.26)
    glutSolidCube(1)
    glPopMatrix()
    
    # Pequenos flaps no DRS
    glColor3f(0.18, 0.18, 0.18)
    glPushMatrix()
    glTranslatef(0.15, 0.01, 0)
    glRotatef(-8, 0, 0, 1)
    glScalef(0.08, 0.02, 1.2)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()
    
    # === ENDPLATES LATERAIS ===
    for side in [-0.68, 0.68]:
        glPushMatrix()
        glTranslatef(0, 0.18, side)
        
        # Endplate principal (formato complexo)
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
        
        # Logo PETRONAS no endplate
        glColor3f(0, 0.5, 0.45)
        glPushMatrix()
        glTranslatef(-0.05, 0.05, side > 0 and 0.015 or -0.015)
        glScalef(0.15, 0.08, 0.01)
        glutSolidCube(1)
        glPopMatrix()
        
        # Texto "PETRONAS" simulado
        glColor3f(1, 1, 1)
        for i in range(3):
            glPushMatrix()
            glTranslatef(-0.08 + i * 0.04, 0.05, side > 0 and 0.02 or -0.02)
            glScalef(0.02, 0.04, 0.005)
            glutSolidCube(1)
            glPopMatrix()
        
        # Slots de ventilação
        glColor3f(0.05, 0.05, 0.05)
        for slot in range(5):
            glPushMatrix()
            glTranslatef(-0.1, -0.25 + slot * 0.1, side > 0 and 0.01 or -0.01)
            glScalef(0.15, 0.02, 0.008)
            glutSolidCube(1)
            glPopMatrix()
        
        glPopMatrix()
    
    # === SUPORTES DO DRS (atuadores) ===
    glColor3f(0.3, 0.3, 0.3)
    for side in [-0.15, 0.15]:
        glPushMatrix()
        glTranslatef(-0.05, 0.25, side)
        glRotatef(90, 0, 1, 0)
        quadric = gluNewQuadric()
        gluCylinder(quadric, 0.012, 0.012, 0.08, 8, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
    
    glPopMatrix()

def draw_wings_standalone():
    """Versão standalone para visualização das duas asas"""
    # Asa dianteira
    glPushMatrix()
    glTranslatef(0, 0, 2)
    draw_front_wing()
    glPopMatrix()
    
    # Asa traseira
    glPushMatrix()
    glTranslatef(0, 0, -2)
    draw_rear_wing(0.5)  # DRS meio aberto
    glPopMatrix()

# Teste standalone
if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1200, 700)
    glutCreateWindow(b"F1 Wings - Front & Rear with DRS")
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [5, 10, 5, 0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.6, 0.6, 0.6, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1])
    
    glLightfv(GL_LIGHT1, GL_POSITION, [-5, 8, -5, 0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.6, 0.6, 0.6, 1])
    
    glClearColor(0.5, 0.7, 1.0, 1)
    
    angle = [0]
    drs = [0]
    drs_dir = [0.01]
    
    def display():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(6, 2, 6, 0, 0, 0, 0, 1, 0)
        
        glRotatef(angle[0], 0, 1, 0)
        
        # Asa dianteira
        glPushMatrix()
        glTranslatef(0, 0, 3.5)
        draw_front_wing()
        glPopMatrix()
        
        # Asa traseira com DRS animado
        glPushMatrix()
        glTranslatef(0, 0, -2)
        draw_rear_wing(drs[0])
        glPopMatrix()
        
        glutSwapBuffers()
    
    def idle():
        angle[0] += 0.3
        
        # Anima DRS
        drs[0] += drs_dir[0]
        if drs[0] >= 1.0 or drs[0] <= 0:
            drs_dir[0] *= -1
        
        glutPostRedisplay()
    
    def reshape(w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
    
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    
    print("\n=== F1 WINGS TEST ===")
    print("Visualizando asas dianteira e traseira")
    print("DRS animando automaticamente")
    print("Pressione ESC para sair\n")
    
    glutMainLoop()

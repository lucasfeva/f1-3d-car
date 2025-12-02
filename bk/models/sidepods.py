#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: Sidepods e Entradas de Ar
Sidepods aerodinâmicos com entradas de ar e radiadores
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

def draw_smooth_sidepod(length, height, width):
    """Desenha um sidepod com formato aerodinâmico suave"""
    segments = 20
    
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        t = i / segments
        
        # Perfil do sidepod (afunila na traseira)
        x = length * t
        scale = 1.0 - (t * 0.6)  # Afunilamento
        
        # Curva superior
        y_top = height * (1 - t * 0.3) * math.sin(math.pi * 0.5 * (1 - t * 0.5))
        
        for side in [-1, 1]:
            z = side * width * scale * 0.5
            glNormal3f(0, 1, side)
            glVertex3f(x, y_top, z)
    glEnd()
    
    # Parte inferior
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
    """Desenha os sidepods completos (esquerdo e direito)"""
    
    for side_multiplier in [-1, 1]:
        glPushMatrix()
        glTranslatef(-0.1, -0.05, side_multiplier * 0.65)
        
        # === CORPO PRINCIPAL DO SIDEPOD ===
        glColor3f(0.15, 0.15, 0.15)
        draw_smooth_sidepod(1.8, 0.35, 0.45)
        
        # === ENTRADA DE AR FRONTAL (Air Intake) ===
        glPushMatrix()
        glTranslatef(0.7, 0.08, 0)
        
        # Moldura da entrada
        glColor3f(0.25, 0.25, 0.25)
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glutSolidTorus(0.04, 0.15, 12, 16)
        glPopMatrix()
        
        # Interior escuro (radiador)
        glColor3f(0.02, 0.02, 0.02)
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        quadric = gluNewQuadric()
        gluDisk(quadric, 0, 0.14, 20, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
        
        # Grade do radiador (simulada)
        glColor3f(0.15, 0.15, 0.15)
        for row in range(5):
            for col in range(5):
                glPushMatrix()
                y_offset = -0.08 + row * 0.04
                z_offset = -0.08 + col * 0.04
                glTranslatef(0, y_offset, z_offset)
                glScalef(0.02, 0.015, 0.015)
                glutSolidCube(1)
                glPopMatrix()
        
        glPopMatrix()
        
        # === UNDERCUT (Parte inferior escavada) ===
        glColor3f(0.08, 0.08, 0.08)
        glPushMatrix()
        glTranslatef(0.5, -0.15, 0)
        glScalef(0.8, 0.12, 0.35)
        glutSolidCube(1)
        glPopMatrix()
        
        # === DETALHE AERODINÂMICO SUPERIOR ===
        glColor3f(0.2, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(0.3, 0.15, 0)
        glScalef(1.2, 0.03, 0.38)
        glutSolidCube(1)
        glPopMatrix()
        
        # === FAIXA TURQUESA MERCEDES ===
        glColor3f(0, 0.95, 0.88)
        
        # Faixa horizontal principal
        glPushMatrix()
        glTranslatef(0.4, 0.08, side_multiplier * 0.005)
        glScalef(1.0, 0.022, 0.45)
        glutSolidCube(1)
        glPopMatrix()
        
        # Detalhe vertical
        glPushMatrix()
        glTranslatef(0.1, 0, side_multiplier * 0.005)
        glScalef(0.025, 0.25, 0.42)
        glutSolidCube(1)
        glPopMatrix()
        
        # === LOGO PETRONAS ===
        glColor3f(0, 0.65, 0.55)
        glPushMatrix()
        glTranslatef(0, 0.02, side_multiplier * 0.005)
        glScalef(0.45, 0.025, 0.15)
        glutSolidCube(1)
        glPopMatrix()
        
        # Texto "PETRONAS" simulado
        glColor3f(1, 1, 1)
        for i in range(5):
            glPushMatrix()
            glTranslatef(-0.15 + i * 0.08, 0.02, side_multiplier * 0.01)
            glScalef(0.04, 0.08, 0.01)
            glutSolidCube(1)
            glPopMatrix()
        
        # === DEFLECTORES LATERAIS (Bargeboard region) ===
        glColor3f(0.18, 0.18, 0.18)
        
        # Defletor principal
        glPushMatrix()
        glTranslatef(0.8, -0.08, side_multiplier * 0.25)
        glRotatef(side_multiplier * -15, 0, 1, 0)
        glScalef(0.3, 0.22, 0.025)
        glutSolidCube(1)
        glPopMatrix()
        
        # Defletor secundário
        glPushMatrix()
        glTranslatef(0.65, -0.12, side_multiplier * 0.28)
        glRotatef(side_multiplier * -20, 0, 1, 0)
        glScalef(0.2, 0.15, 0.02)
        glutSolidCube(1)
        glPopMatrix()
        
        # === SAÍDA DE AR SUPERIOR (Chimney) ===
        glColor3f(0.12, 0.12, 0.12)
        glPushMatrix()
        glTranslatef(-0.3, 0.18, side_multiplier * 0.05)
        glRotatef(25, 1, 0, 0)
        glScalef(0.15, 0.08, 0.12)
        glutSolidCube(1)
        glPopMatrix()
        
        # Interior escuro da saída
        glColor3f(0.02, 0.02, 0.02)
        glPushMatrix()
        glTranslatef(-0.3, 0.2, side_multiplier * 0.05)
        glRotatef(25, 1, 0, 0)
        glScalef(0.12, 0.05, 0.1)
        glutSolidCube(1)
        glPopMatrix()
        
        # === ELEMENTO AERODINÂMICO TRASEIRO ===
        glColor3f(0.15, 0.15, 0.15)
        glPushMatrix()
        glTranslatef(-0.7, 0.05, 0)
        glScalef(0.25, 0.18, 0.38)
        glutSolidCube(1)
        glPopMatrix()
        
        # === SLOTS DE VENTILAÇÃO ===
        glColor3f(0.05, 0.05, 0.05)
        for slot in range(4):
            glPushMatrix()
            glTranslatef(0.2 + slot * 0.15, 0.12, side_multiplier * 0.005)
            glScalef(0.08, 0.015, 0.4)
            glutSolidCube(1)
            glPopMatrix()
        
        glPopMatrix()

def draw_airbox():
    """Desenha a entrada de ar superior (airbox) acima do cockpit"""
    glPushMatrix()
    glTranslatef(-0.3, 0.38, 0)
    
    # === ESTRUTURA PRINCIPAL DO AIRBOX ===
    glColor3f(0.18, 0.18, 0.18)
    
    # Base do airbox
    glPushMatrix()
    glScalef(0.28, 0.5, 0.18)
    glutSolidCube(1)
    glPopMatrix()
    
    # === ENTRADA DE AR (Roll Hoop Intake) ===
    glPushMatrix()
    glTranslatef(0.08, 0, 0)
    
    # Moldura
    glColor3f(0.25, 0.25, 0.25)
    glPushMatrix()
    glRotatef(90, 0, 0, 1)
    glutSolidTorus(0.03, 0.12, 12, 20)
    glPopMatrix()
    
    # Interior (motor visível)
    glColor3f(0.02, 0.02, 0.02)
    glPushMatrix()
    glRotatef(90, 0, 0, 1)
    quadric = gluNewQuadric()
    gluDisk(quadric, 0, 0.11, 24, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    
    glPopMatrix()
    
    # === DUTOS INTERNOS (visíveis) ===
    glColor3f(0.12, 0.12, 0.12)
    for angle in [-15, 15]:
        glPushMatrix()
        glRotatef(angle, 0, 0, 1)
        glTranslatef(0, -0.15, 0)
        quadric = gluNewQuadric()
        gluCylinder(quadric, 0.04, 0.06, 0.2, 12, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()
    
    # === CAMERA MOUNT (suporte de câmera) ===
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0, 0.3, 0)
    
    # Haste
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.015, 0.015, 0.08, 8, 1)
    gluDeleteQuadric(quadric)
    
    # Câmera
    glTranslatef(0, 0, 0.08)
    glColor3f(0.1, 0.1, 0.1)
    glScalef(0.04, 0.03, 0.05)
    glutSolidCube(1)
    
    # Lente
    glColor3f(0.2, 0.2, 0.3)
    glPushMatrix()
    glTranslatef(0, 0, 0.6)
    glScalef(0.5, 0.5, 0.2)
    glutSolidSphere(1, 12, 12)
    glPopMatrix()
    
    glPopMatrix()
    
    # === DETALHE MERCEDES ===
    glColor3f(0, 0.9, 0.85)
    glPushMatrix()
    glTranslatef(0, -0.15, 0)
    glScalef(0.25, 0.02, 0.15)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()

def draw_sidepods_standalone():
    """Versão standalone para visualização"""
    draw_sidepods()
    draw_airbox()

# Teste standalone
if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1200, 700)
    glutCreateWindow(b"F1 Sidepods & Airbox")
    
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
    
    def display():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(4, 2, 4, 0, 0, 0, 0, 1, 0)
        
        glRotatef(angle[0], 0, 1, 0)
        draw_sidepods()
        draw_airbox()
        
        glutSwapBuffers()
    
    def idle():
        angle[0] += 0.4
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
    
    print("\n=== F1 SIDEPODS & AIRBOX TEST ===")
    print("Visualizando sidepods e entrada de ar superior")
    print("Pressione ESC para sair\n")
    
    glutMainLoop()
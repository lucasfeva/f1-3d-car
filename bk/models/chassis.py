#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: Chassi F1 Mercedes
Chassi principal do carro com formas suavizadas e realistas
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

def draw_smooth_box(width, height, depth, segments=8):
    """Desenha uma caixa com bordas arredondadas"""
    w, h, d = width/2, height/2, depth/2
    r = min(width, height, depth) * 0.1  # Raio do arredondamento
    
    glBegin(GL_QUADS)
    
    # Face frontal
    glNormal3f(0, 0, 1)
    glVertex3f(-w+r, -h+r, d)
    glVertex3f(w-r, -h+r, d)
    glVertex3f(w-r, h-r, d)
    glVertex3f(-w+r, h-r, d)
    
    # Face traseira
    glNormal3f(0, 0, -1)
    glVertex3f(-w+r, -h+r, -d)
    glVertex3f(-w+r, h-r, -d)
    glVertex3f(w-r, h-r, -d)
    glVertex3f(w-r, -h+r, -d)
    
    # Face superior
    glNormal3f(0, 1, 0)
    glVertex3f(-w+r, h, -d+r)
    glVertex3f(-w+r, h, d-r)
    glVertex3f(w-r, h, d-r)
    glVertex3f(w-r, h, -d+r)
    
    # Face inferior
    glNormal3f(0, -1, 0)
    glVertex3f(-w+r, -h, -d+r)
    glVertex3f(w-r, -h, -d+r)
    glVertex3f(w-r, -h, d-r)
    glVertex3f(-w+r, -h, d-r)
    
    # Face direita
    glNormal3f(1, 0, 0)
    glVertex3f(w, -h+r, -d+r)
    glVertex3f(w, -h+r, d-r)
    glVertex3f(w, h-r, d-r)
    glVertex3f(w, h-r, -d+r)
    
    # Face esquerda
    glNormal3f(-1, 0, 0)
    glVertex3f(-w, -h+r, -d+r)
    glVertex3f(-w, h-r, -d+r)
    glVertex3f(-w, h-r, d-r)
    glVertex3f(-w, -h+r, d-r)
    
    glEnd()

def draw_tapered_cylinder(base_radius, top_radius, height, slices=20):
    """Desenha um cilindro cônico suave"""
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluCylinder(quadric, base_radius, top_radius, height, slices, 1)
    
    # Tampas
    glPushMatrix()
    gluDisk(quadric, 0, base_radius, slices, 1)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, height)
    gluDisk(quadric, 0, top_radius, slices, 1)
    glPopMatrix()
    
    gluDeleteQuadric(quadric)

def draw_chassis():
    """Desenha o chassi principal do Mercedes W16"""
    
    # === MONOCOQUE PRINCIPAL (Forma aerodinâmica) ===
    glColor3f(0.12, 0.12, 0.12)  # Preto carbono
    
    # Seção frontal do monocoque (afunilando para o bico)
    glPushMatrix()
    glTranslatef(1.5, -0.05, 0)
    glRotatef(90, 0, 1, 0)
    draw_tapered_cylinder(0.35, 0.15, 1.8, 32)
    glPopMatrix()
    
    # Seção central do monocoque (cockpit)
    glPushMatrix()
    glTranslatef(0.5, -0.05, 0)
    glRotatef(90, 0, 1, 0)
    draw_tapered_cylinder(0.38, 0.35, 1.0, 32)
    glPopMatrix()
    
    # Seção traseira (afunilando novamente)
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
    
    # === BICO DO CARRO (Nose) ===
    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glTranslatef(2.8, -0.15, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(-5, 1, 0, 0)  # Inclinação do bico
    draw_tapered_cylinder(0.12, 0.05, 0.8, 24)
    glPopMatrix()
    
    # Ponta do bico (bem afilada)
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
    
    # === COCKPIT (Abertura) ===
    glColor3f(0.05, 0.05, 0.05)
    glPushMatrix()
    glTranslatef(0.4, 0.1, 0)
    glScalef(0.9, 0.2, 0.5)
    glutSolidSphere(1, 24, 16)
    glPopMatrix()
    
    # Assento do piloto (visível)
    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glTranslatef(0.3, -0.02, 0)
    glScalef(0.4, 0.15, 0.35)
    glutSolidSphere(1, 20, 16)
    glPopMatrix()
    
    # === HALO (Proteção do piloto) - Mais realista ===
    glColor3f(0.4, 0.4, 0.42)  # Titânio
    
    # Arco principal do Halo (formato anatômico)
    glPushMatrix()
    glTranslatef(0.5, 0.35, 0)
    
    # Desenha arco com múltiplos segmentos para suavizar
    for angle in range(0, 180, 10):
        rad = math.radians(angle)
        x1 = math.cos(rad) * 0.3
        y1 = math.sin(rad) * 0.25
        
        rad2 = math.radians(angle + 10)
        x2 = math.cos(rad2) * 0.3
        y2 = math.sin(rad2) * 0.25
        
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
    
    # === VOLANTE F1 ===
    glPushMatrix()
    glTranslatef(0.55, 0.18, 0)
    glRotatef(20, 0, 0, 1)  # inclinação leve apontando para o piloto
    
    # Base do volante (retangular)
    glColor3f(0.15, 0.15, 0.15)
    glPushMatrix()
    glScalef(0.15, 0.05, 0.12)
    glutSolidCube(1)
    glPopMatrix()
    
    # Aros laterais
    glColor3f(0.3, 0.3, 0.3)
    for side in [-0.08, 0.08]:
        glPushMatrix()
        glTranslatef(0, 0, side)
        glRotatef(90, 0, 1, 0)
        glutSolidTorus(0.01, 0.06, 8, 12)
        glPopMatrix()
    
    # Display digital (simulado)
    glColor3f(0, 0.8, 0.3)
    glPushMatrix()
    glScalef(0.08, 0.02, 0.06)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()
    
    # === ASSOALHO PLANO ===
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
    
    # === DIFUSOR TRASEIRO ===
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(-1.7, -0.18, 0)
    glRotatef(15, 0, 0, 1)
    
    # Elementos do difusor
    for i in range(5):
        offset = (i - 2) * 0.15
        glPushMatrix()
        glTranslatef(0, 0, offset)
        glScalef(0.5, 0.02, 0.12)
        glutSolidCube(1)
        glPopMatrix()
    
    glPopMatrix()
    
    # === DETALHES TURQUESA MERCEDES ===
    glColor3f(0, 1.0, 0.92)
    
    # Faixa lateral característica
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
    
    # === ESPELHOS RETROVISORES ===
    for side in [-1, 1]:  # -1 = esquerda, +1 = direita
        glPushMatrix()
        # ancora no lado do cockpit
        glTranslatef(0.7, 0.25, side * 0.55)

        # Haste levemente inclinada para cima e para fora
        glRotatef(10, 0, 0, 1)          # sobe um pouco
        glRotatef(18 * side, 0, 1, 0)   # abre para fora

        # Haste
        glColor3f(0.2, 0.2, 0.2)
        quadric = gluNewQuadric()
        # cilindro ao longo de +Z no sistema local
        gluCylinder(quadric, 0.015, 0.015, 0.18, 8, 1)
        gluDeleteQuadric(quadric)

        # ponta da haste
        glTranslatef(0, 0, 0.18)

        # Espelho olhando para trás (-X do carro)
        glRotatef(-90, 0, 1, 0)         # normal +Z -> -X
        glColor3f(0.6, 0.6, 0.65)
        glPushMatrix()
        glScalef(0.10, 0.06, 0.02)
        glutSolidCube(1)
        glPopMatrix()

        glPopMatrix()

def draw_chassis_standalone():
    """Versão standalone para visualização"""
    draw_chassis()

# Teste standalone
if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 700)
    glutCreateWindow(b"F1 Chassis - Mercedes W16")
    
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
    
    glLightfv(GL_LIGHT1, GL_POSITION, [-5, 10, -5, 0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.6, 0.6, 0.6, 1])
    
    glClearColor(0.5, 0.7, 1.0, 1)
    
    angle = [0]
    
    def display():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(8, 3, 8, 0, 0, 0, 0, 1, 0)
        
        glRotatef(angle[0], 0, 1, 0)
        draw_chassis()
        
        glutSwapBuffers()
    
    def idle():
        angle[0] += 0.5
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
    
    print("\n=== F1 CHASSIS TEST ===")
    print("Visualizando chassi Mercedes W16")
    print("Pressione ESC para sair\n")
    
    glutMainLoop()

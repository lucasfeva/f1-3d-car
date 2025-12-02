#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modulo: Rodas F1 Pirelli
Roda realista de Formula 1 com pneus Pirelli
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math


def draw_wheel(x, y, z, rotation, is_front=False, steer_angle=0):
    """
    Desenha uma roda de F1 realista com pneu Pirelli

    Args:
        x, y, z: Posicao da roda
        rotation: Angulo de rotacao (movimento)
        is_front: Se e roda dianteira (aplica estercoamento)
        steer_angle: Angulo de estercoamento
    """
    glPushMatrix()
    glTranslatef(x, y, z)

    if is_front:
        glRotatef(steer_angle, 0, 1, 0)

    # Roda rola ao redor do eixo Z (mantem alinhada ao movimento do carro)
    glRotatef(rotation, 0, 0, 1)

    # Dimensoes principais (mais largas e retas para lembrar um pneu de F1)
    tire_radius = 0.34
    tire_width = 0.34
    rim_radius = 0.18
    rim_width = 0.22

    # === PNEU PIRELLI ===
    glColor3f(0.08, 0.08, 0.08)  # Banda de rodagem
    glPushMatrix()
    glTranslatef(0, 0, -tire_width * 0.5)
    quadric = gluNewQuadric()
    gluCylinder(quadric, tire_radius, tire_radius, tire_width, 32, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    # Laterais (um pouco mais retas)
    glColor3f(0.12, 0.12, 0.12)
    for side in [-tire_width * 0.5, tire_width * 0.5]:
        glPushMatrix()
        glTranslatef(0, 0, side)
        quadric = gluNewQuadric()
        gluDisk(quadric, rim_radius + 0.02, tire_radius, 28, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    # === ARO DA RODA (Magnesio) ===
    glColor3f(0.45, 0.45, 0.5)
    glPushMatrix()
    glTranslatef(0, 0, -rim_width * 0.5)
    quadric = gluNewQuadric()
    gluCylinder(quadric, rim_radius, rim_radius, rim_width, 32, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    for side in [-rim_width * 0.5, rim_width * 0.5]:
        glPushMatrix()
        glTranslatef(0, 0, side)
        quadric = gluNewQuadric()
        gluDisk(quadric, 0.05, rim_radius, 28, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    # === RAIOS DA RODA (Design aerodinamico) ===
    glColor3f(0.35, 0.35, 0.38)
    num_spokes = 10
    for i in range(num_spokes):
        angle = (360 / num_spokes) * i
        glPushMatrix()
        glRotatef(angle, 0, 0, 1)

        glBegin(GL_QUAD_STRIP)
        for j in range(8):
            t = j / 7.0
            radius = 0.05 + t * 0.11
            width = 0.01 if j < 3 else 0.015

            glVertex3f(radius * math.cos(math.radians(width * 50)),
                      radius * math.sin(math.radians(width * 50)), -rim_width * 0.45)
            glVertex3f(radius * math.cos(math.radians(-width * 50)),
                      radius * math.sin(math.radians(-width * 50)), -rim_width * 0.45)
            glVertex3f(radius * math.cos(math.radians(width * 50)),
                      radius * math.sin(math.radians(width * 50)), rim_width * 0.45)
            glVertex3f(radius * math.cos(math.radians(-width * 50)),
                      radius * math.sin(math.radians(-width * 50)), rim_width * 0.45)
        glEnd()

        glPopMatrix()

    # === CENTRO DA RODA (Porca) ===
    glColor3f(0.6, 0.6, 0.65)
    glPushMatrix()
    glTranslatef(0, 0, -rim_width * 0.55)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.05, 0.05, rim_width * 1.1, 16, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    glColor3f(0.5, 0.5, 0.55)
    for side in [-rim_width * 0.55, rim_width * 0.55]:
        glPushMatrix()
        glTranslatef(0, 0, side)
        quadric = gluNewQuadric()
        gluDisk(quadric, 0, 0.05, 6, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    # === DETALHES ADICIONAIS ===
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0.22, 0, 0.02)
    glRotatef(90, 1, 0, 0)
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.008, 0.008, 0.03, 8, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    # Listras coloridas no pneu (indicador de composto Pirelli)
    glColor3f(1.0, 0.9, 0.0)  # Amarelo (soft)
    for i in range(3):
        glPushMatrix()
        glRotatef(i * 120, 0, 0, 1)
        glTranslatef(tire_radius - 0.02, 0, 0)
        glBegin(GL_QUADS)
        glVertex3f(-0.008, 0, -tire_width * 0.5)
        glVertex3f(0.008, 0, -tire_width * 0.5)
        glVertex3f(0.008, 0, tire_width * 0.5)
        glVertex3f(-0.008, 0, tire_width * 0.5)
        glEnd()
        glPopMatrix()

    glPopMatrix()


# Teste standalone
if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"F1 Wheel - Pirelli Tire")

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])

    glClearColor(0.2, 0.2, 0.2, 1)

    rotation = [0]

    def display():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(1.5, 0.5, 1.5, 0, 0, 0, 0, 1, 0)

        draw_wheel(0, 0, 0, rotation[0])

        glutSwapBuffers()

    def idle():
        rotation[0] += 2
        glutPostRedisplay()

    def reshape(w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)

    print("\n=== F1 PIRELLI WHEEL TEST ===")
    print("Visualizando roda de F1 realista")
    print("Pressione ESC para sair\n")

    glutMainLoop()

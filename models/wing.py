"""Front and rear wing elements built from thin boxes."""
from __future__ import annotations

from typing import Tuple

from OpenGL.GL import (
    GL_QUADS,
    glBegin,
    glColor3f,
    glEnd,
    glNormal3f,
    glPopMatrix,
    glPushMatrix,
    glScalef,
    glTranslatef,
    glVertex3f,
)

Color = Tuple[float, float, float]


def _wing_plate(width: float, depth: float, thickness: float, color: Color) -> None:
    glColor3f(*color)
    glPushMatrix()
    glScalef(width, thickness, depth)
    glBegin(GL_QUADS)

    # Top
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    # Bottom
    glNormal3f(0, -1, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)

    # Sides
    glNormal3f(-1, 0, 0)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glNormal3f(1, 0, 0)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)

    # Leading/trailing edges
    glNormal3f(0, 0, 1)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glNormal3f(0, 0, -1)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    glEnd()
    glPopMatrix()


def draw_front_wing(color: Color) -> None:
    glPushMatrix()
    glTranslatef(0.0, -0.1, 2.6)
    _wing_plate(width=2.2, depth=0.5, thickness=0.05, color=color)

    # Endplates
    glPushMatrix()
    glTranslatef(1.1, 0.0, 0.0)
    _wing_plate(width=0.1, depth=0.5, thickness=0.6, color=color)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-1.1, 0.0, 0.0)
    _wing_plate(width=0.1, depth=0.5, thickness=0.6, color=color)
    glPopMatrix()
    glPopMatrix()


def draw_rear_wing(color: Color, flap_angle: float) -> None:
    glPushMatrix()
    glTranslatef(0.0, 0.8, -1.6)
    _wing_plate(width=1.5, depth=0.4, thickness=0.06, color=color)

    # Movable flap
    glPushMatrix()
    glTranslatef(0.0, 0.2, -0.1)
    glRotatef(flap_angle, 1, 0, 0)
    _wing_plate(width=1.5, depth=0.3, thickness=0.05, color=color)
    glPopMatrix()

    glPopMatrix()

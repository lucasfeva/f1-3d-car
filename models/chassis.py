"""Chassis model built from simple box segments."""
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


def _draw_box(width: float, height: float, depth: float, color: Color) -> None:
    hw, hh, hd = width / 2, height / 2, depth / 2
    glColor3f(*color)
    glBegin(GL_QUADS)

    # Front
    glNormal3f(0, 0, 1)
    glVertex3f(-hw, -hh, hd)
    glVertex3f(hw, -hh, hd)
    glVertex3f(hw, hh, hd)
    glVertex3f(-hw, hh, hd)

    # Back
    glNormal3f(0, 0, -1)
    glVertex3f(-hw, -hh, -hd)
    glVertex3f(-hw, hh, -hd)
    glVertex3f(hw, hh, -hd)
    glVertex3f(hw, -hh, -hd)

    # Left
    glNormal3f(-1, 0, 0)
    glVertex3f(-hw, -hh, -hd)
    glVertex3f(-hw, -hh, hd)
    glVertex3f(-hw, hh, hd)
    glVertex3f(-hw, hh, -hd)

    # Right
    glNormal3f(1, 0, 0)
    glVertex3f(hw, -hh, -hd)
    glVertex3f(hw, hh, -hd)
    glVertex3f(hw, hh, hd)
    glVertex3f(hw, -hh, hd)

    # Top
    glNormal3f(0, 1, 0)
    glVertex3f(-hw, hh, -hd)
    glVertex3f(-hw, hh, hd)
    glVertex3f(hw, hh, hd)
    glVertex3f(hw, hh, -hd)

    # Bottom
    glNormal3f(0, -1, 0)
    glVertex3f(-hw, -hh, -hd)
    glVertex3f(hw, -hh, -hd)
    glVertex3f(hw, -hh, hd)
    glVertex3f(-hw, -hh, hd)

    glEnd()


def draw_chassis(base_color: Color, accent_color: Color) -> None:
    """Draw a simplified single-seater chassis and cockpit."""
    glPushMatrix()

    # Main monocoque
    _draw_box(1.8, 0.4, 3.0, base_color)

    # Nose cone
    glPushMatrix()
    glTranslatef(0.0, -0.05, 1.8)
    glScalef(0.5, 0.35, 1.2)
    _draw_box(1.0, 0.5, 1.0, accent_color)
    glPopMatrix()

    # Cockpit halo
    glPushMatrix()
    glTranslatef(0.0, 0.3, -0.2)
    glScalef(0.8, 0.2, 0.8)
    _draw_box(1.0, 0.5, 1.0, accent_color)
    glPopMatrix()

    # Engine cover
    glPushMatrix()
    glTranslatef(0.0, 0.35, -0.8)
    glScalef(0.7, 0.6, 1.2)
    _draw_box(1.0, 0.5, 1.0, base_color)
    glPopMatrix()

    glPopMatrix()

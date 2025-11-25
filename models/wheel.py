"""Wheel model built with PyOpenGL primitives."""
from __future__ import annotations

import math
from typing import Optional

from OpenGL.GL import (
    GL_TRIANGLE_FAN,
    glBegin,
    glColor3f,
    glEnd,
    glNormal3f,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glScalef,
    glTranslatef,
    glVertex3f,
)
from OpenGL.GLU import gluCylinder, gluDisk, gluNewQuadric


class Wheel:
    """Simple F1 wheel composed of a tire and a rim."""

    def __init__(
        self,
        *,
        radius: float = 0.35,
        width: float = 0.25,
        slices: int = 24,
        loops: int = 4,
        rim_radius: float = 0.22,
    ) -> None:
        self.radius = radius
        self.width = width
        self.slices = slices
        self.loops = loops
        self.rim_radius = rim_radius
        self._quadric = gluNewQuadric()

    def draw(self, rotation_deg: float, tint: Optional[tuple[float, float, float]] = None) -> None:
        """Render the wheel.

        Args:
            rotation_deg: Rotation applied around the wheel's local Z axis.
            tint: Optional RGB multiplier to slightly vary wheel shading.
        """
        glPushMatrix()
        glRotatef(rotation_deg, 0, 0, 1)

        tire_color = tint if tint else (0.1, 0.1, 0.1)
        glColor3f(*tire_color)
        gluCylinder(self._quadric, self.radius, self.radius, self.width, self.slices, self.loops)

        glPushMatrix()
        glRotatef(180, 0, 1, 0)
        gluDisk(self._quadric, 0.0, self.radius, self.slices, 1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, self.width)
        gluDisk(self._quadric, 0.0, self.radius, self.slices, 1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, self.width / 2)
        glScalef(1.0, 1.0, 0.2)
        glColor3f(0.6, 0.6, 0.6)
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, 0, 1)
        glVertex3f(0.0, 0.0, 0.01)
        for i in range(self.slices + 1):
            angle = (i / self.slices) * 360.0
            glVertex3f(
                self.rim_radius * math.cos(math.radians(angle)),
                self.rim_radius * math.sin(math.radians(angle)),
                0.0,
            )
        glEnd()
        glPopMatrix()

        glPopMatrix()

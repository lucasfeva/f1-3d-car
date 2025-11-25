"""Infinite track helper for the F1 scene."""
from __future__ import annotations

from OpenGL.GL import (
    GL_QUADS,
    glBegin,
    glColor3f,
    glEnd,
    glNormal3f,
    glVertex3f,
)


def draw_track(offset: float) -> None:
    """Render a repeating strip to simulate infinite track motion."""
    length = 40.0
    stripe_width = 0.2
    lane_half_width = 3.0

    glBegin(GL_QUADS)
    glColor3f(0.12, 0.12, 0.12)
    glNormal3f(0, 1, 0)

    for i in range(-2, 3):
        start = offset + i * length
        end = start + length
        # Track surface
        glVertex3f(-lane_half_width, -0.5, start)
        glVertex3f(lane_half_width, -0.5, start)
        glVertex3f(lane_half_width, -0.5, end)
        glVertex3f(-lane_half_width, -0.5, end)

        # Center line stripe
        stripe_start = start + length * 0.2
        stripe_end = stripe_start + stripe_width
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(-0.05, -0.49, stripe_start)
        glVertex3f(0.05, -0.49, stripe_start)
        glVertex3f(0.05, -0.49, stripe_end)
        glVertex3f(-0.05, -0.49, stripe_end)
        glColor3f(0.12, 0.12, 0.12)

    glEnd()

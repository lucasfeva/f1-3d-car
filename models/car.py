"""Modular Formula 1 car built purely with PyOpenGL primitives."""
from __future__ import annotations

from dataclasses import dataclass

from OpenGL.GL import glPopMatrix, glPushMatrix, glTranslatef

from .chassis import draw_chassis
from .wheel import Wheel
from .wing import draw_front_wing, draw_rear_wing


@dataclass
class CarColors:
    base: tuple[float, float, float] = (0.75, 0.0, 0.05)
    accent: tuple[float, float, float] = (0.95, 0.95, 0.95)
    wings: tuple[float, float, float] = (0.05, 0.05, 0.05)


class Car:
    """Composable F1 car with animated wheels and rear flap."""

    def __init__(self) -> None:
        self.colors = CarColors()
        self.wheel_rotation = 0.0
        self.rear_wing_flap = 8.0
        self._wheels = {
            "front_left": Wheel(),
            "front_right": Wheel(),
            "rear_left": Wheel(radius=0.36, width=0.28),
            "rear_right": Wheel(radius=0.36, width=0.28),
        }

    def update(self, distance_delta: float) -> None:
        # Convert distance to rotation in degrees (circumference ~ 2 * pi * r)
        rotation_delta = (distance_delta / (2 * 3.14159 * self._wheels["front_left"].radius)) * 360
        self.wheel_rotation = (self.wheel_rotation + rotation_delta) % 360
        # Animate rear flap slightly for visual interest.
        self.rear_wing_flap = 10.0 + 5.0 * (abs((self.wheel_rotation % 60) - 30) / 30)

    def draw(self) -> None:
        glPushMatrix()
        self._draw_wheels()
        self._draw_body()
        glPopMatrix()

    def _draw_wheels(self) -> None:
        offsets = {
            "front_left": (0.8, -0.25, 1.3),
            "front_right": (-0.8, -0.25, 1.3),
            "rear_left": (0.85, -0.25, -1.1),
            "rear_right": (-0.85, -0.25, -1.1),
        }

        for name, (x, y, z) in offsets.items():
            glPushMatrix()
            glTranslatef(x, y, z)
            self._wheels[name].draw(self.wheel_rotation)
            glPopMatrix()

    def _draw_body(self) -> None:
        glPushMatrix()
        draw_chassis(self.colors.base, self.colors.accent)
        draw_front_wing(self.colors.wings)
        draw_rear_wing(self.colors.wings, flap_angle=self.rear_wing_flap)
        glPopMatrix()

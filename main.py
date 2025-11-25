"""Entry point for the PyOpenGL Formula 1 scene built from custom primitives."""
from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Tuple

import pygame
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_COLOR_MATERIAL,
    GL_DEPTH_TEST,
    GL_LIGHT0,
    GL_POSITION,
    GL_LIGHTING,
    GL_MODELVIEW,
    GL_PROJECTION,
    glClear,
    glClearColor,
    glEnable,
    glLightfv,
    glLoadIdentity,
    glMatrixMode,
    glRotatef,
    glTranslatef,
)
from OpenGL.GLU import gluLookAt, gluPerspective

from models.car import Car
from track import draw_track

Vector3 = Tuple[float, float, float]


@dataclass
class Camera:
    eye: Vector3 = (0.0, 1.8, -6.0)
    target: Vector3 = (0.0, 0.2, 6.0)
    up: Vector3 = (0.0, 1.0, 0.0)

    def apply(self) -> None:
        gluLookAt(*self.eye, *self.target, *self.up)


class Scene:
    def __init__(self) -> None:
        self.car = Car()
        self.camera = Camera()
        self.distance = 0.0
        self.running = False

    def update(self, delta: float) -> None:
        if self.running:
            speed = 6.0  # meters per second
            distance_delta = speed * delta
            self.distance += distance_delta
            self.car.update(distance_delta)

    def draw(self) -> None:
        glClearColor(0.25, 0.5, 0.75, 1.0)
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.camera.apply()

        # Tilt the camera slightly for a dynamic angle.
        glRotatef(-10, 1, 0, 0)

        draw_track(-(self.distance % 40.0))

        glPushMatrix()
        glTranslatef(0.0, 0.0, self.distance)
        self.car.draw()
        glPopMatrix()


# pygame/OpenGL bootstrap ----------------------------------------------------

def init_lighting() -> None:
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 1.0))  # GL_POSITION = 0x120


def init_perspective(width: int, height: int) -> None:
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, width / height, 0.1, 100.0)


def main() -> None:
    pygame.init()
    width, height = 1280, 720
    pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("F1 PyOpenGL - Primitive Car")
    clock = pygame.time.Clock()

    glEnable(GL_DEPTH_TEST)
    init_perspective(width, height)
    init_lighting()

    scene = Scene()

    font = pygame.font.SysFont("Arial", 18)

    while True:
        delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_SPACE:
                    scene.running = not scene.running

        scene.update(delta)
        scene.draw()

        # Overlay HUD
        hud = font.render("Press SPACE to toggle animation", True, (255, 255, 255))
        pygame.display.get_surface().blit(hud, (20, 20))
        pygame.display.flip()


if __name__ == "__main__":
    main()

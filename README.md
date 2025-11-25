# F1 3D Car Scene (PyOpenGL primitives)

This project demonstrates a fully hand-modeled Formula 1 car rendered only with PyOpenGL primitives and assembled from modular parts (wheels, chassis, wings). Pygame is used solely for window creation, keyboard handling, and drawing on-screen text.

## Features
- Infinite-style asphalt strip rendered procedurally to simulate constant forward motion.
- Modular car built from immediate-mode boxes and cylinders: separate wheel, chassis, and wing modules assembled in `models/car.py`.
- Animated wheel rotation and a gently moving rear wing flap for the required extra moving element.
- User-controlled animation start/pause with the **Space** key plus HUD instructions.

## Running locally
1. Install dependencies (virtualenv recommended):
   ```bash
   pip install pygame PyOpenGL PyOpenGL_accelerate
   ```
2. Run the scene:
   ```bash
   python main.py
   ```
3. Press **Space** to start or pause the car animation. Use **Esc** or close the window to quit.

## Project layout
```
.
├── main.py           # Pygame/OpenGL bootstrap and render loop
├── models/
│   ├── car.py        # Car assembly and animation logic
│   ├── chassis.py    # Box-based chassis and cockpit
│   ├── wheel.py      # Cylindrical wheel with rim details
│   └── wing.py       # Front wing and movable rear flap
├── track.py          # Infinite track rendering helper
└── scene.gltf        # Reference asset (not used by the running scene)
```

`scene.gltf` remains in the repository only as a visual reference; the running code draws the vehicle exclusively with PyOpenGL.

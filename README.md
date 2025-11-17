Snake Game Test using DearPyGui 2.0

Just a simple Snake game implemented in Python for the purpose of testing and evaluating the DearPyGui 2.0 drawing API.
The goal of the project is to validate how the new version of DearPyGui handles texture rendering, image rotation, drawlists, and real-time frame updates.

⸻

Overview

The game uses a fixed grid where the snake moves continuously in a chosen direction and grows when eating food.
Rendering is handled entirely through DearPyGui’s low-level drawing API.

Key Components

1. Grid Rendering
The grid is drawn using dpg.draw_rectangle, generating a 20x20 board where each cell is 20 pixels.

2. Snake Rendering
The snake is composed of three sprite types:
	•	Head
	•	Body
	•	Tail

Textures are loaded a single time using a texture registry.
The head and tail sprites rotate according to movement direction. Rotation is implemented using draw_image_quad, where the image’s four vertices are rotated manually using trigonometric calculations.

3. Food Rendering
The food uses a static sprite drawn at its grid position.
Each new food location is generated randomly, avoiding collision with the snake.

4. Input Handling
Movement supports both WASD and arrow keys.
Input is captured through DearPyGui’s handler_registry.

5. Game Loop
DearPyGui 2.0 does not include a built-in frame loop.
The game updates through a manual loop using dpg.render_dearpygui_frame() combined with a timed movement interval.

6. Game Logic
	•	The snake grows when eating food
	•	The game ends if the snake collides with itself or a boundary
	•	Resetting the game restores all state and generates new food

⸻

Purpose

This repository is intentionally simple and self-contained.
It serves as a reference for:
	•	Texture loading in DearPyGui 2.0
	•	Rendering images and quads
	•	Manual sprite rotation using quad vertices
	•	Real-time rendering loop integration
	•	Basic input and state management

⸻

Requirements
	•	Python 3.10+
	•	dearpygui 2.0+

Install dependencies

pip install dearpygui

Running

python snake.py

This will open a DearPyGui window containing the Snake game.

⸻

License

Use it however you want.
Just don’t blame me if the snake becomes self-aware and decides to start Skynet on your behalf.
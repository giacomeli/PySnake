# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PySnake is a simple Snake game implementation in Python designed specifically to test and evaluate the DearPyGui 2.0 drawing API. This is a single-file project (`snake.py`) that demonstrates texture rendering, image rotation, drawlists, and real-time frame updates using DearPyGui's low-level drawing capabilities.

## Running the Game

```bash
# Install dependencies
pip install dearpygui

# Run the game
python snake.py
```

## Architecture

### DearPyGui 2.0 Rendering System

The game is built entirely on DearPyGui's low-level drawing API. Key architectural points:

- **No built-in game loop**: DearPyGui 2.0 does not provide a frame loop. The game implements a manual loop at `snake.py:299-305` using `dpg.render_dearpygui_frame()` combined with a timed movement interval (`MOVE_INTERVAL = 0.15`)

- **Texture registry pattern**: All sprites are loaded once during initialization into a texture registry (`snake.py:279`), then referenced by ID throughout the game

- **Manual sprite rotation**: Head and tail sprites rotate based on movement direction. Rotation is implemented using `draw_image_quad` (`snake.py:115-135`) where the image's four vertices are manually rotated using trigonometric calculations (not a built-in rotation API)

### Key Components

**Grid System** (`snake.py:95-106`): Fixed 20x20 grid rendered with `dpg.draw_rectangle`, each cell is 20 pixels

**Sprite Rendering** (`snake.py:109-186`):
- Three snake sprite types: head, body, tail
- `draw_sprite()`: Non-rotated sprite rendering
- `draw_sprite_rotated()`: Manual rotation via quad vertex transformation
- Direction-to-angle conversion: `angle_from_direction()` maps grid directions to radians, assuming base sprites point right (1, 0)

**Game State** (`snake.py:12-25`): Global variables store snake segments (list of tuples), current direction, food position, score, and game-over status

**Input Handling** (`snake.py:259-270`): DearPyGui's `handler_registry` captures both WASD and arrow keys. Direction changes validate against opposite direction to prevent instant self-collision

**Rendering Flow**:
1. `draw()` clears the canvas and redraws everything each frame
2. Called from `update_game()` after movement logic
3. All drawing happens to a single drawlist canvas (`canvas_id`)

### Sprite Assets

Required sprites in `/sprites/` directory:
- `apple.png` - Food sprite
- `snake_head.png` - Head sprite (should face right by default)
- `snake_body.png` - Body segment sprite
- `snake_tail.png` - Tail sprite (should face right by default)

If sprites are missing, `load_texture()` (`snake.py:42-54`) raises `FileNotFoundError` with the missing path.

## Code Structure Notes

- **Single-file design**: All game logic, rendering, and UI are in `snake.py`
- **Global state pattern**: Game state is maintained in global variables (intentional for simplicity)
- **Portuguese error messages**: Error messages in `load_texture()` are in Portuguese
- **Coordinate system**: Grid uses (x, y) tuples where y increases downward (standard screen coordinates)

## DearPyGui 2.0 Specifics

When modifying rendering code:
- Drawing operations (draw_rectangle, draw_image, draw_image_quad) must specify `parent=canvas_id`
- Canvas must be cleared each frame: `dpg.delete_item(canvas_id, children_only=True)`
- Textures are loaded via `dpg.load_image()` returning (width, height, channels, data), then added to registry with `dpg.add_static_texture()`
- The manual game loop pattern is required: `dpg.render_dearpygui_frame()` inside a while loop with time-based updates

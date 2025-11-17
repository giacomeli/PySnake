import os
import math
import random
import time
import dearpygui.dearpygui as dpg

GRID_SIZE = 20
CELL_SIZE = 20
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
MOVE_INTERVAL = 0.15

snake = [(5, 5)]
direction = (1, 0)
food = (10, 10)
score = 0
game_over = False

canvas_id = None
score_text_id = None

texture_registry_id = None
apple_texture_id = None
snake_head_texture_id = None
snake_body_texture_id = None
snake_tail_texture_id = None

# ---------------------
# PATHS
# ---------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPRITES_DIR = os.path.join(SCRIPT_DIR, "sprites")

APPLE_SPRITE_PATH = os.path.join(SPRITES_DIR, "apple.png")
SNAKE_HEAD_SPRITE_PATH = os.path.join(SPRITES_DIR, "snake_head.png")
SNAKE_BODY_SPRITE_PATH = os.path.join(SPRITES_DIR, "snake_body.png")
SNAKE_TAIL_SPRITE_PATH = os.path.join(SPRITES_DIR, "snake_tail.png")


# ---------------------
#  TEXTURE LOADER
# ---------------------
def load_texture(path: str):
    global texture_registry_id

    if not os.path.exists(path):
        raise FileNotFoundError(f"Sprite não encontrado em: {path}")

    result = dpg.load_image(path)
    if result is None:
        raise RuntimeError(f"Falha ao carregar imagem com dpg.load_image: {path}")

    width, height, channels, data = result
    tex_id = dpg.add_static_texture(width, height, data, parent=texture_registry_id)
    return tex_id


# ---------------------
#  DIRECTION -> ANGLE
# ---------------------
def angle_from_direction(dx: int, dy: int) -> float:
    # Assumindo sprite base apontando para a DIREITA (1, 0)
    if dx == 1 and dy == 0:   # direita
        return 0.0
    if dx == -1 and dy == 0:  # esquerda
        return math.pi
    if dx == 0 and dy == -1:  # cima (y decresce)
        return -math.pi / 2
    if dx == 0 and dy == 1:   # baixo (y cresce)
        return math.pi / 2
    return 0.0


# --------------------------------
# GAME LOGIC
# --------------------------------
def spawn_food():
    while True:
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if pos not in snake:
            return pos


def reset_game():
    global snake, direction, food, score, game_over
    snake.clear()
    snake.append((5, 5))
    direction = (1, 0)
    food = spawn_food()
    score = 0
    game_over = False
    dpg.set_value(score_text_id, f"Score: {score}")
    draw()


def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            x1, y1 = x * CELL_SIZE, y * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            dpg.draw_rectangle(
                (x1, y1),
                (x2, y2),
                color=(60, 60, 60, 80),
                thickness=1,
                parent=canvas_id,
            )


def draw_sprite(x, y, texture_id):
    x1, y1 = x * CELL_SIZE, y * CELL_SIZE
    x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
    dpg.draw_image(texture_id, (x1, y1), (x2, y2), parent=canvas_id)


def draw_sprite_rotated(x, y, texture_id, angle_rad: float):
    cx = x * CELL_SIZE + CELL_SIZE / 2
    cy = y * CELL_SIZE + CELL_SIZE / 2
    half = CELL_SIZE / 2

    corners = [
        (-half, -half),
        ( half, -half),
        ( half,  half),
        (-half,  half),
    ]

    rotated = []
    for (px, py) in corners:
        rx = px * math.cos(angle_rad) - py * math.sin(angle_rad)
        ry = px * math.sin(angle_rad) + py * math.cos(angle_rad)
        rotated.append((cx + rx, cy + ry))

    p1, p2, p3, p4 = rotated

    dpg.draw_image_quad(texture_id, p1, p2, p3, p4, parent=canvas_id)


def draw_snake_and_food():
    # HEAD
    head_x, head_y = snake[0]
    head_angle = angle_from_direction(direction[0], direction[1])

    if snake_head_texture_id is not None:
        draw_sprite_rotated(head_x, head_y, snake_head_texture_id, head_angle)
    else:
        draw_sprite(head_x, head_y, snake_body_texture_id or apple_texture_id)

    # BODY + TAIL
    for index in range(1, len(snake)):
        x, y = snake[index]
        is_tail = (index == len(snake) - 1)

        if is_tail:
            if len(snake) >= 2:
                prev_x, prev_y = snake[index - 1]
                dx = prev_x - x
                dy = prev_y - y
                tail_angle = angle_from_direction(dx, dy)
            else:
                tail_angle = head_angle

            if snake_tail_texture_id is not None:
                draw_sprite_rotated(x, y, snake_tail_texture_id, tail_angle)
            else:
                draw_sprite(x, y, snake_body_texture_id or apple_texture_id)
        else:
            # corpo sem rotação
            if snake_body_texture_id is not None:
                draw_sprite(x, y, snake_body_texture_id)
            else:
                draw_sprite(x, y, apple_texture_id)

    # Food (sprite)
    fx, fy = food
    if apple_texture_id is None:
        fx1, fy1 = fx * CELL_SIZE, fy * CELL_SIZE
        fx2, fy2 = fx1 + CELL_SIZE, fy1 + CELL_SIZE
        dpg.draw_rectangle(
            (fx1, fy1),
            (fx2, fy2),
            fill=(255, 0, 0, 255),
            parent=canvas_id,
        )
    else:
        draw_sprite(fx, fy, apple_texture_id)


def draw():
    dpg.delete_item(canvas_id, children_only=True)
    draw_grid()
    draw_snake_and_food()


def update_game():
    global snake, direction, food, score, game_over

    if game_over:
        return

    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # colisão com corpo ou borda
    if new_head in snake or not 0 <= new_head[0] < GRID_SIZE or not 0 <= new_head[1] < GRID_SIZE:
        game_over = True
        dpg.set_value(score_text_id, f"Game Over! Score: {score}")
        return

    snake.insert(0, new_head)

    if new_head == food:
        food = spawn_food()
        score += 1
        dpg.set_value(score_text_id, f"Score: {score}")
    else:
        snake.pop()

    draw()


# Movimentos
def set_direction_up():
    global direction
    if direction != (0, 1):
        direction = (0, -1)


def set_direction_down():
    global direction
    if direction != (0, -1):
        direction = (0, 1)


def set_direction_left():
    global direction
    if direction != (1, 0):
        direction = (-1, 0)


def set_direction_right():
    global direction
    if direction != (-1, 0):
        direction = (1, 0)


# Construção da UI
def build_ui():
    global canvas_id, score_text_id

    with dpg.window(label="Snake - DearPyGui 2.0", width=WINDOW_SIZE + 20, height=WINDOW_SIZE + 80):
        dpg.add_text("Use W A S D or arrow keys to move. Press R to restart.")
        dpg.add_button(label="Restart", callback=reset_game)
        score_text_id = dpg.add_text(f"Score: {score}")
        with dpg.drawlist(width=WINDOW_SIZE, height=WINDOW_SIZE) as canvas:
            canvas_id = canvas

    # Input
    with dpg.handler_registry():
        dpg.add_key_press_handler(key=dpg.mvKey_W, callback=lambda s, a: set_direction_up())
        dpg.add_key_press_handler(key=dpg.mvKey_A, callback=lambda s, a: set_direction_left())
        dpg.add_key_press_handler(key=dpg.mvKey_S, callback=lambda s, a: set_direction_down())
        dpg.add_key_press_handler(key=dpg.mvKey_D, callback=lambda s, a: set_direction_right())

        dpg.add_key_press_handler(key=dpg.mvKey_Up, callback=lambda s, a: set_direction_up())
        dpg.add_key_press_handler(key=dpg.mvKey_Left, callback=lambda s, a: set_direction_left())
        dpg.add_key_press_handler(key=dpg.mvKey_Down, callback=lambda s, a: set_direction_down())
        dpg.add_key_press_handler(key=dpg.mvKey_Right, callback=lambda s, a: set_direction_right())

        dpg.add_key_press_handler(key=dpg.mvKey_R, callback=lambda s, a: reset_game())


# ---------------------
# INICIALIZAÇÃO
# ---------------------
dpg.create_context()

# Registry de texturas
texture_registry_id = dpg.add_texture_registry(show=False)

# Carrega sprites (se algum arquivo não existir, vai levantar exceção clara)
apple_texture_id = load_texture(APPLE_SPRITE_PATH)
snake_head_texture_id = load_texture(SNAKE_HEAD_SPRITE_PATH)
snake_body_texture_id = load_texture(SNAKE_BODY_SPRITE_PATH)
snake_tail_texture_id = load_texture(SNAKE_TAIL_SPRITE_PATH)

build_ui()
reset_game()

dpg.create_viewport(
    title="Snake with DearPyGui 2.0",
    width=WINDOW_SIZE + 40,
    height=WINDOW_SIZE + 100,
)
dpg.setup_dearpygui()
dpg.show_viewport()

# Gameloop manual
last_time = time.time()
while dpg.is_dearpygui_running():
    now = time.time()
    if now - last_time >= MOVE_INTERVAL:
        update_game()
        last_time = now
    dpg.render_dearpygui_frame()

dpg.destroy_context() 
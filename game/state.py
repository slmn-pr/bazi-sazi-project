import random
import pygame
from .config import WIDTH, HEIGHT, OBSTACLE_SIZE, BASE_SPEED
from .config import INVINCIBILITY_DURATION  # for access if needed
from .config import COLORS


def reset_game(player_size, current_best=0):
    return {
        "player_rect": pygame.Rect((WIDTH - player_size.x) / 2, HEIGHT - 100, player_size.x, player_size.y),
        "items": [],
        "score": 0,
        "best_score": current_best,
        "speed_multiplier": 1.0,
        "lives": 3,
        "state": "MENU",
        "shield_active": False,
        "shield_until": 0,
        "invincible_until": 0,
        "shake_intensity": 0,
        "frame_count": 0,
    }


def spawn_item(score):
    cols = list(range(20, WIDTH - 40, 50))
    x_pos = random.choice(cols)
    roll = random.random()
    if roll < 0.05:
        kind = "life"
    elif roll < 0.15:
        kind = "shield"
    elif roll < 0.35:
        kind = "bonus"
    else:
        kind = "hazard"

    if kind == "hazard":
        color = COLORS["danger"]
    elif kind == "bonus":
        color = COLORS["bonus"]
    elif kind == "shield":
        color = COLORS["accent"]
    elif kind == "life":
        color = COLORS["life"]
    else:
        color = COLORS["white"]

    return {
        "rect": pygame.Rect(x_pos, -60, OBSTACLE_SIZE, OBSTACLE_SIZE),
        "kind": kind,
        "color": color,
        "angle": 0,
    }


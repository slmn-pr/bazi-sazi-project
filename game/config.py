from pathlib import Path
import pygame

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
ICON_DIR = ASSETS_DIR / "icons"
JETS_DIR = ASSETS_DIR / "jets"
SOUNDS_DIR = ASSETS_DIR / "sounds"

DEFAULT_JET_PATH = ASSETS_DIR / "airplane.png"
HEART_ICON_PATH = ICON_DIR / "heart-svgrepo-com.svg"
SHIELD_ICON_PATH = ICON_DIR / "shield.svg"
BOMB_ICON_PATH = ICON_DIR / "bomb.svg"
MUSIC_PATH = SOUNDS_DIR / "music.mp3"
SOUND_BOMB_PATH = SOUNDS_DIR / "bomb.mp3"
SOUND_POINT_PATH = SOUNDS_DIR / "point.mp3"
SOUND_LIFE_PATH = SOUNDS_DIR / "life.mp3"
SOUND_SHIELD_PATH = SOUNDS_DIR / "shield.mp3"

WIDTH, HEIGHT = 800, 600

COLORS = {
    "bg_top": (15, 20, 35),
    "bg_bottom": (30, 35, 60),
    "white": (250, 250, 255),
    "accent": (0, 255, 255),
    "danger": (255, 50, 80),
    "mine": (150, 50, 255),
    "bonus": (50, 255, 100),
    "life": (255, 200, 0),
    "gray_text": (150, 160, 170),
}

PLAYER_SIZE = pygame.Vector2(70, 62)
JET_THUMB_SIZE = 96
OBSTACLE_SIZE = 40
BASE_SPEED = 5
SHIELD_DURATION = 5000
INVINCIBILITY_DURATION = 1500

def load_fonts():
    try:
        title = pygame.font.SysFont("segoeui", 70, bold=True)
        ui = pygame.font.SysFont("segoeui", 22, bold=True)
        btn = pygame.font.SysFont("segoeui", 30, bold=True)
        small = pygame.font.SysFont("segoeui", 16)
    except Exception:
        title = pygame.font.SysFont("arial", 70, bold=True)
        ui = pygame.font.SysFont("arial", 22, bold=True)
        btn = pygame.font.SysFont("arial", 30, bold=True)
        small = pygame.font.SysFont("arial", 16)
    return title, ui, btn, small


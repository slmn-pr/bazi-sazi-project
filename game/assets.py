import pygame
from pathlib import Path
from typing import List, Dict, Any
from .config import (
    DEFAULT_JET_PATH,
    HEART_ICON_PATH,
    SHIELD_ICON_PATH,
    BOMB_ICON_PATH,
    MUSIC_PATH,
    SOUND_BOMB_PATH,
    SOUND_POINT_PATH,
    SOUND_LIFE_PATH,
    SOUND_SHIELD_PATH,
    JETS_DIR,
    JET_THUMB_SIZE,
    PLAYER_SIZE,
)


def init_audio():
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"Warning: audio init failed ({e})")


def load_music():
    if MUSIC_PATH.exists():
        try:
            pygame.mixer.music.load(str(MUSIC_PATH))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
            return True
        except Exception as e:
            print(f"Music load error: {e}")
    return False


def load_sound(path: Path, volume: float = 0.8):
    try:
        snd = pygame.mixer.Sound(str(path))
        snd.set_volume(volume)
        return snd
    except Exception:
        return None


def load_icon(path: Path, size, color_tint=None):
    try:
        icon = pygame.image.load(str(path)).convert_alpha()
        icon = pygame.transform.smoothscale(icon, size)
        if color_tint:
            tint = pygame.Surface(size, pygame.SRCALPHA)
            tint.fill(color_tint)
            icon.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return icon
    except Exception:
        return None


def _strip_background(surf: pygame.Surface, tol=(18, 18, 18)):
    try:
        corners = [
            surf.get_at((0, 0)),
            surf.get_at((surf.get_width() - 1, 0)),
            surf.get_at((0, surf.get_height() - 1)),
            surf.get_at((surf.get_width() - 1, surf.get_height() - 1)),
        ]
        key = max(set(corners), key=corners.count)
        transparent = (0, 0, 0, 0) if len(key) == 4 else (0, 0, 0)
        pygame.transform.threshold(surf, surf, key, tol, transparent, 1, None, True)
        surf.set_colorkey(key)
    except Exception:
        pass


def load_player_sprite(path: Path):
    try:
        surf = pygame.image.load(str(path)).convert_alpha()
        target_w = int(PLAYER_SIZE.x)
        ratio = target_w / surf.get_width()
        target_h = int(surf.get_height() * ratio)
        surf = pygame.transform.smoothscale(surf, (target_w, target_h))
        _strip_background(surf)
        PLAYER_SIZE.y = target_h
        return surf
    except Exception:
        return None


def load_jet_thumb(path: Path):
    try:
        surf = pygame.image.load(str(path)).convert_alpha()
        surf = pygame.transform.smoothscale(surf, (JET_THUMB_SIZE, JET_THUMB_SIZE))
        _strip_background(surf)
        return surf
    except Exception:
        return None


def load_jet_choices() -> List[Dict[str, Any]]:
    paths = []
    if DEFAULT_JET_PATH.exists():
        paths.append(DEFAULT_JET_PATH)
    if JETS_DIR.exists():
        for p in sorted(JETS_DIR.glob("*.png")):
            if p not in paths:
                paths.append(p)

    choices = []
    for p in paths:
        choices.append(
            {
                "path": p,
                "name": p.stem.replace("_", " ").title(),
                "thumb": load_jet_thumb(p),
            }
        )
    return choices


init_audio()
SFX = {
    "hazard": load_sound(SOUND_BOMB_PATH, 0.85),
    "bonus": load_sound(SOUND_POINT_PATH, 0.7),
    "life": load_sound(SOUND_LIFE_PATH, 0.8),
    "shield": load_sound(SOUND_SHIELD_PATH, 0.8),
}
MUSIC_LOADED = load_music()

JET_CHOICES = []
selected_jet_index = 0
PLAYER_IMG = None
HEART_IMG = None
SHIELD_IMG = None
BOMB_IMG = None


def set_current_jet(index: int):
    global selected_jet_index, PLAYER_IMG
    if not JET_CHOICES:
        return
    selected_jet_index = max(0, min(index, len(JET_CHOICES) - 1))
    PLAYER_IMG = load_player_sprite(JET_CHOICES[selected_jet_index]["path"])


def play_sfx(kind: str):
    snd = SFX.get(kind)
    if snd:
        try:
            snd.play()
        except Exception:
            pass


def init_assets():
    """Load jets and icons after display is initialized."""
    global JET_CHOICES, HEART_IMG, SHIELD_IMG, BOMB_IMG, selected_jet_index, PLAYER_IMG
    JET_CHOICES = load_jet_choices()
    HEART_IMG = load_icon(HEART_ICON_PATH, (28, 28))
    SHIELD_IMG = load_icon(SHIELD_ICON_PATH, (30, 30))
    BOMB_IMG = load_icon(BOMB_ICON_PATH, (30, 30))
    selected_jet_index = 0
    set_current_jet(selected_jet_index)
    return {
        "jets": JET_CHOICES,
        "heart": HEART_IMG,
        "shield": SHIELD_IMG,
        "bomb": BOMB_IMG,
        "player_img": PLAYER_IMG,
    }


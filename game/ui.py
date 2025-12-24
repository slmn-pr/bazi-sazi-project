import pygame
from .config import COLORS, WIDTH, HEIGHT, JET_THUMB_SIZE, SHIELD_DURATION


def clamp(value, min_v, max_v):
    return max(min_v, min(max_v, value))


class Button:
    def __init__(self, text, center_pos, font):
        self.text = text
        self.rect = pygame.Rect(0, 0, 220, 60)
        self.rect.center = center_pos
        self.hovered = False
        self.scale = 1.0
        self.font = font

    def draw(self, surface, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        target_scale = 1.1 if self.hovered else 1.0
        self.scale += (target_scale - self.scale) * 0.2

        scaled_w = int(self.rect.width * self.scale)
        scaled_h = int(self.rect.height * self.scale)
        draw_rect = pygame.Rect(0, 0, scaled_w, scaled_h)
        draw_rect.center = self.rect.center

        bg_color = COLORS["accent"] if self.hovered else COLORS["white"]
        text_color = (0, 0, 0) if self.hovered else (50, 50, 70)

        shadow_rect = draw_rect.copy()
        shadow_rect.y += 4
        pygame.draw.rect(surface, (0, 0, 0, 80), shadow_rect, border_radius=15)
        pygame.draw.rect(surface, bg_color, draw_rect, border_radius=15)
        pygame.draw.rect(surface, COLORS["accent"], draw_rect, 3, border_radius=15)

        txt_surf = self.font.render(self.text, True, text_color)
        surface.blit(txt_surf, txt_surf.get_rect(center=draw_rect.center))
        return self.hovered


def create_background():
    surf = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(COLORS["bg_top"][0] * (1 - t) + COLORS["bg_bottom"][0] * t)
        g = int(COLORS["bg_top"][1] * (1 - t) + COLORS["bg_bottom"][1] * t)
        b = int(COLORS["bg_top"][2] * (1 - t) + COLORS["bg_bottom"][2] * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (WIDTH, y))
    return surf


def draw_hud(screen, fonts, state, heart_img):
    ui_font = fonts["ui"]
    score_surf = ui_font.render(f"SCORE: {state['score']}", True, COLORS["white"])
    screen.blit(score_surf, (20, 20))

    for i in range(state["lives"]):
        x_pos = 30 + i * 35
        if heart_img:
            screen.blit(heart_img, (x_pos - 10, 50))
        else:
            pygame.draw.circle(screen, COLORS["life"], (x_pos, 60), 10)

    if state["shield_active"]:
        time_left = max(0, (state["shield_until"] - pygame.time.get_ticks()) // 100)
        bar_width = int((time_left / (SHIELD_DURATION / 100)) * 100)
        pygame.draw.rect(screen, COLORS["accent"], (20, 85, bar_width, 8), border_radius=4)
        lbl = ui_font.render("SHIELD", True, COLORS["accent"])
        screen.blit(lbl, (20 + bar_width + 10, 75))


def draw_garage(screen, fonts, jets, mouse_pos, scroll, selected_idx):
    title_font = fonts["title"]
    ui_font = fonts["ui"]
    title = title_font.render("SELECT YOUR JET", True, COLORS["white"])
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

    hint = ui_font.render(
        "Scroll / ← → then click a jet to select • ESC/BACK to return",
        True,
        (170, 180, 190),
    )
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 170)))

    spacing = JET_THUMB_SIZE + 30
    row_y = HEIGHT - 160
    cards = []
    max_scroll = max(0, spacing * len(jets) - (WIDTH - 120))

    for idx, jet in enumerate(jets):
        x = 80 + idx * spacing - scroll
        rect = pygame.Rect(x, row_y, JET_THUMB_SIZE, JET_THUMB_SIZE)
        if rect.right < -80 or rect.left > WIDTH + 80:
            continue

        card_rect = rect.inflate(28, 28)
        pygame.draw.rect(screen, (0, 0, 0, 90), card_rect, border_radius=16)
        pygame.draw.rect(screen, (32, 36, 60), card_rect, border_radius=16)
        border_color = COLORS["accent"] if idx == selected_idx else (90, 100, 130)
        pygame.draw.rect(screen, border_color, card_rect, 3, border_radius=16)

        if jet["thumb"]:
            screen.blit(jet["thumb"], jet["thumb"].get_rect(center=rect.center))
        else:
            pygame.draw.polygon(
                screen,
                COLORS["white"],
                [
                    (rect.centerx, rect.top),
                    (rect.right, rect.bottom),
                    (rect.centerx, rect.bottom - 10),
                    (rect.left, rect.bottom),
                ],
            )

        name_surf = ui_font.render(jet["name"], True, (210, 220, 230))
        screen.blit(name_surf, name_surf.get_rect(center=(rect.centerx, row_y + JET_THUMB_SIZE + 24)))

        cards.append((idx, card_rect))

    return cards, max_scroll


import math
import random
import pygame
from .config import (
    WIDTH,
    HEIGHT,
    COLORS,
    BASE_SPEED,
    SHIELD_DURATION,
    INVINCIBILITY_DURATION,
    load_fonts,
    PLAYER_SIZE,
)
from . import assets
from .particles import ParticleSystem
from .state import reset_game, spawn_item
from .ui import Button, create_background, draw_garage, draw_hud, clamp


def main():
    # Initialize pygame subsystems before using fonts or display
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Neon Dodge: Ultimate (Modular)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fonts_tuple = load_fonts()
    fonts = {"title": fonts_tuple[0], "ui": fonts_tuple[1], "btn": fonts_tuple[2], "small": fonts_tuple[3]}

    bg_surface = create_background()

    game_state = reset_game(PLAYER_SIZE)
    particles = ParticleSystem()

    btn_start = Button("START GAME", (WIDTH // 2, HEIGHT // 2 + 20), fonts["btn"])
    btn_garage = Button("CHOOSE JET", (WIDTH // 2, HEIGHT // 2 + 90), fonts["btn"])
    btn_restart = Button("PLAY AGAIN", (WIDTH // 2, HEIGHT // 2 + 40), fonts["btn"])
    btn_quit = Button("EXIT", (WIDTH // 2, HEIGHT // 2 + 110), fonts["btn"])
    btn_back = Button("BACK", (WIDTH // 2, HEIGHT - 60), fonts["btn"])

    garage_scroll = 0
    garage_cards = []
    garage_max_scroll = 0
    # After display is ready, load assets that need a display surface
    asset_bundle = assets.init_assets()
    HEART_IMG = asset_bundle["heart"]
    SHIELD_IMG = asset_bundle["shield"]
    BOMB_IMG = asset_bundle["bomb"]
    JET_CHOICES = asset_bundle["jets"]
    PLAYER_IMG = asset_bundle["player_img"]
    selected_jet_index = assets.selected_jet_index

    music_playing = assets.MUSIC_LOADED

    running = True
    while running:
        dt = clock.tick(60)
        now = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        game_state["frame_count"] += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state["state"] == "GARAGE":
                        game_state["state"] = "MENU"
                    else:
                        running = False

                if event.key == pygame.K_m:
                    if music_playing:
                        pygame.mixer.music.pause()
                        music_playing = False
                    else:
                        try:
                            pygame.mixer.music.unpause()
                            music_playing = True
                        except Exception:
                            pass

                if game_state["state"] == "GARAGE":
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        garage_scroll = clamp(garage_scroll - 80, 0, garage_max_scroll)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        garage_scroll = clamp(garage_scroll + 80, 0, garage_max_scroll)

            if event.type == pygame.MOUSEWHEEL and game_state["state"] == "GARAGE":
                garage_scroll = clamp(garage_scroll - event.y * 50, 0, garage_max_scroll)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state["state"] == "MENU":
                    if btn_start.hovered:
                        game_state["state"] = "PLAYING"
                    elif btn_garage.hovered:
                        game_state["state"] = "GARAGE"
                elif game_state["state"] == "GARAGE":
                    if btn_back.hovered:
                        game_state["state"] = "MENU"
                    else:
                        for idx, rect in garage_cards:
                            if rect.collidepoint(event.pos):
                                assets.set_current_jet(idx)
                                PLAYER_IMG = assets.PLAYER_IMG
                                selected_jet_index = assets.selected_jet_index
                                game_state = reset_game(PLAYER_SIZE, game_state["best_score"])
                                game_state["state"] = "GARAGE"
                                particles.emit(rect.centerx, rect.centery, COLORS["accent"], count=15)
                                break
                elif game_state["state"] == "GAMEOVER":
                    if btn_restart.hovered:
                        game_state = reset_game(PLAYER_SIZE, game_state["best_score"])
                        game_state["state"] = "PLAYING"
                    if btn_quit.hovered:
                        running = False

        shake_x, shake_y = 0, 0
        if game_state["shake_intensity"] > 0:
            game_state["shake_intensity"] -= 1
            shake_x = random.randint(-5, 5)
            shake_y = random.randint(-5, 5)

        screen.blit(bg_surface, (shake_x, shake_y))

        if game_state["state"] == "MENU":
            glow = abs(math.sin(now * 0.003)) * 50
            title_surf = fonts["title"].render("NEON DODGE", True, (255, 255, 255))
            shadow_surf = fonts["title"].render("NEON DODGE", True, (0, 200, 255))
            title_rect = title_surf.get_rect(center=(WIDTH // 2, 150))
            screen.blit(shadow_surf, (title_rect.x + shake_x, title_rect.y + 4 + shake_y))
            screen.blit(title_surf, (title_rect.x + shake_x, title_rect.y + shake_y))

            btn_start.draw(screen, mouse_pos)
            btn_garage.draw(screen, mouse_pos)
            help_txt = fonts["ui"].render("Use A/D or Arrows to Move", True, (150, 160, 180))
            screen.blit(help_txt, help_txt.get_rect(center=(WIDTH // 2, HEIGHT - 50)))

        elif game_state["state"] == "GARAGE":
            garage_cards, garage_max_scroll = draw_garage(
                screen, fonts, assets.JET_CHOICES, mouse_pos, garage_scroll, assets.selected_jet_index
            )
            btn_back.draw(screen, mouse_pos)
            current_name = fonts["ui"].render(
                f"Current: {assets.JET_CHOICES[assets.selected_jet_index]['name']}", True, COLORS["accent"]
            )
            screen.blit(current_name, current_name.get_rect(center=(WIDTH // 2, HEIGHT - 90)))

        elif game_state["state"] == "PLAYING":
            player = game_state["player_rect"]
            keys = pygame.key.get_pressed()
            move_x = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                move_x = -BASE_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                move_x = BASE_SPEED
            player.x += move_x
            player.x = max(0, min(WIDTH - player.width, player.x))

            if game_state["frame_count"] % max(20, 60 - int(game_state["score"] / 50)) == 0:
                game_state["items"].append(spawn_item(game_state["score"]))

            to_remove = []
            player_hitbox = player.inflate(-15, -15)

            for item in game_state["items"]:
                item["rect"].y += (4 + game_state["score"] * 0.01) * game_state["speed_multiplier"]

                rect_pos = (item["rect"].x + shake_x, item["rect"].y + shake_y)

                glow_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*item["color"], 60), glow_surf.get_rect(), border_radius=8)
                screen.blit(glow_surf, rect_pos)

                icon_drawn = False
                if item["kind"] == "hazard" and BOMB_IMG:
                    screen.blit(BOMB_IMG, BOMB_IMG.get_rect(center=item["rect"].center))
                    icon_drawn = True
                elif item["kind"] == "shield" and SHIELD_IMG:
                    screen.blit(SHIELD_IMG, SHIELD_IMG.get_rect(center=item["rect"].center))
                    icon_drawn = True
                elif item["kind"] == "life" and HEART_IMG:
                    screen.blit(HEART_IMG, HEART_IMG.get_rect(center=item["rect"].center))
                    icon_drawn = True

                if not icon_drawn:
                    if item["kind"] == "bonus":
                        pygame.draw.circle(
                            screen,
                            item["color"],
                            (item["rect"].centerx + shake_x, item["rect"].centery + shake_y),
                            20 - 5,
                        )
                    elif item["kind"] == "hazard":
                        pygame.draw.rect(
                            screen,
                            item["color"],
                            (rect_pos[0] + 5, rect_pos[1] + 5, 30, 30),
                            border_radius=4,
                        )
                    else:
                        pygame.draw.circle(
                            screen,
                            item["color"],
                            (item["rect"].centerx + shake_x, item["rect"].centery + shake_y),
                            20,
                        )

                if player_hitbox.colliderect(item["rect"]):
                    to_remove.append(item)
                    center = item["rect"].center

                    if item["kind"] == "hazard":
                        if game_state["shield_active"]:
                            game_state["shield_active"] = False
                            game_state["shield_until"] = 0
                            game_state["invincible_until"] = now + 1000
                            particles.emit(center[0], center[1], COLORS["accent"], count=20)
                            game_state["shake_intensity"] = 10
                        elif now > game_state["invincible_until"]:
                            game_state["lives"] -= 1
                            game_state["shake_intensity"] = 20
                            game_state["invincible_until"] = now + INVINCIBILITY_DURATION
                            particles.emit(center[0], center[1], COLORS["danger"], count=30, speed=2.0)
                            if game_state["lives"] <= 0:
                                game_state["state"] = "GAMEOVER"
                                if game_state["score"] > game_state["best_score"]:
                                    game_state["best_score"] = game_state["score"]
                        assets.play_sfx("hazard")
                    elif item["kind"] == "bonus":
                        game_state["score"] += 50
                        particles.emit(center[0], center[1], COLORS["bonus"], count=10)
                        assets.play_sfx("bonus")
                    elif item["kind"] == "shield":
                        game_state["shield_active"] = True
                        game_state["shield_until"] = now + SHIELD_DURATION
                        particles.emit(center[0], center[1], COLORS["accent"], count=15)
                        assets.play_sfx("shield")
                    elif item["kind"] == "life":
                        game_state["lives"] = min(5, game_state["lives"] + 1)
                        particles.emit(center[0], center[1], COLORS["life"], count=15)
                        assets.play_sfx("life")

                if item["rect"].y > HEIGHT:
                    to_remove.append(item)
                    if item["kind"] == "hazard":
                        game_state["score"] += 10

            for r in to_remove:
                if r in game_state["items"]:
                    game_state["items"].remove(r)

            if game_state["shield_active"] and now > game_state["shield_until"]:
                game_state["shield_active"] = False

            is_invincible = now < game_state["invincible_until"]

            if not is_invincible or (now // 100) % 2 == 0:
                player_pos = (player.x + shake_x, player.y + shake_y)
                if PLAYER_IMG:
                    screen.blit(PLAYER_IMG, player_pos)
                else:
                    surf = pygame.Surface((int(PLAYER_SIZE.x), int(PLAYER_SIZE.y)), pygame.SRCALPHA)
                    points = [
                        (PLAYER_SIZE.x // 2, 0),
                        (PLAYER_SIZE.x, PLAYER_SIZE.y),
                        (PLAYER_SIZE.x // 2, PLAYER_SIZE.y - 10),
                        (0, PLAYER_SIZE.y),
                    ]
                    pygame.draw.polygon(surf, COLORS["white"], points)
                    screen.blit(surf, player_pos)

                if game_state["shield_active"]:
                    center_pt = (player.centerx + shake_x, player.centery + shake_y)
                    pygame.draw.circle(screen, (0, 255, 255), center_pt, max(PLAYER_SIZE.x, PLAYER_SIZE.y) // 1.5, 2)

                particles.emit(player.centerx, player.bottom - 10, (100, 200, 255), count=1, speed=0.5)

            draw_hud(screen, fonts, game_state, HEART_IMG)

        elif game_state["state"] == "GAMEOVER":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            over_txt = fonts["title"].render("GAME OVER", True, COLORS["danger"])
            score_txt = fonts["ui"].render(f"Final Score: {game_state['score']}", True, COLORS["white"])
            best_txt = fonts["ui"].render(f"Best: {game_state['best_score']}", True, COLORS["bonus"])

            screen.blit(over_txt, over_txt.get_rect(center=(WIDTH // 2, 180)))
            screen.blit(score_txt, score_txt.get_rect(center=(WIDTH // 2, 260)))
            screen.blit(best_txt, best_txt.get_rect(center=(WIDTH // 2, 300)))

            btn_restart.draw(screen, mouse_pos)
            btn_quit.draw(screen, mouse_pos)

        particles.update_and_draw(screen, (shake_x, shake_y))
        pygame.display.flip()

    pygame.quit()
    raise SystemExit


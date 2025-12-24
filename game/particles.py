import random
import math
import pygame


class Particle:
    def __init__(self, x, y, color, speed_factor=1.0):
        self.x = x
        self.y = y
        angle = random.uniform(0, 6.28)
        speed = random.uniform(1, 4) * speed_factor
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(20, 40)
        self.color = color
        self.size = random.randint(3, 6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(0, self.size - 0.1)

    def draw(self, surface, offset_x=0, offset_y=0):
        if self.life > 0 and self.size > 0:
            alpha = min(255, self.life * 8)
            surf = pygame.Surface((int(self.size) * 2, int(self.size) * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), (self.size, self.size), self.size)
            surface.blit(surf, (self.x - self.size + offset_x, self.y - self.size + offset_y))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10, speed=1.0):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, speed_factor=speed))

    def update_and_draw(self, surface, shake_offset=(0, 0)):
        self.particles = [p for p in self.particles if p.life > 0]
        for p in self.particles:
            p.update()
            p.draw(surface, *shake_offset)


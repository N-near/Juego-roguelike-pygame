"""Configuración y generación de oleadas de enemigos."""

from dataclasses import dataclass
import random
from typing import TypedDict

import pygame


class Enemy(TypedDict):
    rect: pygame.Rect
    x: float
    y: float
    velocidad: float
    vida: int
    sprite: pygame.Surface


@dataclass(frozen=True)
class WaveConfig:
    """Valores base y crecimiento por ronda."""

    first_wave_count: int = 3
    extra_enemies_per_wave: int = 2
    spawn_interval: float = 2.0
    minimum_spawn_interval: float = 0.5
    spawn_interval_reduction: float = 0.1
    base_speed: float = 35.0
    speed_per_wave: float = 3.0
    base_health: int = 3
    extra_health_every_waves: int = 2
    intermission_duration: float = 3.0
    enemy_size: int = 24


class WaveManager:
    """Controla cuándo empieza una ronda y cuándo aparece cada enemigo."""

    def __init__(self, config: WaveConfig | None = None) -> None:
        self.config = config or WaveConfig()
        self.wave_number = 1
        self.remaining_to_spawn = self._enemy_count_for_wave(self.wave_number)
        self.spawn_timer = 0.0
        self.intermission_timer = 0.0
        self.awaiting_reward = False
        self.intermission_active = False

    def update(
        self,
        delta_time: float,
        enemies: list[Enemy],
        screen_size: tuple[int, int],
        enemy_sprites: list[pygame.Surface],
    ) -> bool:
        """Actualiza la oleada; devuelve True al detectar su fin por primera vez."""
        if self.awaiting_reward:
            return False

        if self.intermission_active:
            self.intermission_timer += delta_time
            if self.intermission_timer >= self.config.intermission_duration:
                self.wave_number += 1
                self.remaining_to_spawn = self._enemy_count_for_wave(self.wave_number)
                self.spawn_timer = 0.0
                self.intermission_timer = 0.0
                self.intermission_active = False
            return False

        if self.remaining_to_spawn == 0 and not enemies:
            self.awaiting_reward = True
            return True

        self.spawn_timer += delta_time
        interval = self._spawn_interval_for_wave(self.wave_number)
        while self.remaining_to_spawn > 0 and self.spawn_timer >= interval:
            self.spawn_timer -= interval
            enemies.append(self._create_enemy(screen_size, enemy_sprites))
            self.remaining_to_spawn -= 1

        return False

    def continue_after_reward(self) -> None:
        """Inicia el descanso previo a la siguiente oleada tras elegir una mejora."""
        if self.awaiting_reward:
            self.awaiting_reward = False
            self.intermission_active = True
            self.intermission_timer = 0.0

    def _enemy_count_for_wave(self, wave_number: int) -> int:
        return self.config.first_wave_count + (wave_number - 1) * self.config.extra_enemies_per_wave

    def _spawn_interval_for_wave(self, wave_number: int) -> float:
        reduction = (wave_number - 1) * self.config.spawn_interval_reduction
        return max(self.config.minimum_spawn_interval, self.config.spawn_interval - reduction)

    def _create_enemy(
        self,
        screen_size: tuple[int, int],
        enemy_sprites: list[pygame.Surface],
    ) -> Enemy:
        """Crea un enemigo en un borde, fuera del área visible."""
        screen_width, screen_height = screen_size
        size = self.config.enemy_size
        edge = random.choice(("top", "bottom", "left", "right"))

        if edge == "top":
            x, y = random.randrange(screen_width), -size
        elif edge == "bottom":
            x, y = random.randrange(screen_width), screen_height
        elif edge == "left":
            x, y = -size, random.randrange(screen_height)
        else:
            x, y = screen_width, random.randrange(screen_height)

        extra_health = (self.wave_number - 1) // self.config.extra_health_every_waves
        return {
            "rect": pygame.Rect(x, y, size, size),
            "x": float(x),
            "y": float(y),
            "velocidad": self.config.base_speed + (self.wave_number - 1) * self.config.speed_per_wave,
            "vida": self.config.base_health + extra_health,
            "sprite": random.choice(enemy_sprites),
        }

import pygame
from typing import Tuple

from app_config import AppConfig
from window_manager import WindowManager

class OverlayRenderer:
    def __init__(self, window_manager: WindowManager, config: AppConfig) -> None:
        self.window = window_manager
        self.config = config
        self.screen = pygame.display.set_mode((self.window.screen_width, self.window.screen_height), pygame.NOFRAME)

    def extend_line_to_edges(self, vx: float, vy: float, center_x: int, center_y: int,
                             window_rect: Tuple[int, int, int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        window_left, window_top, window_width, window_height = window_rect
        window_right = window_left + window_width
        window_bottom = window_top + window_height

        eps = 1e-5
        t_values = []

        # Вычисляем точки пересечения с границами окна
        if abs(vx) > eps:
            t_values.extend([(window_left - center_x) / vx, (window_right - center_x) / vx])
        if abs(vy) > eps:
            t_values.extend([(window_top - center_y) / vy,(window_bottom - center_y) / vy])

        if not t_values:
            return (window_left, window_top), (window_right, window_bottom)

        t_min = min(t_values)
        t_max = max(t_values)

        start = (int(center_x + vx * t_min), int(center_y + vy * t_min))
        end = (int(center_x + vx * t_max), int(center_y + vy * t_max))

        return start, end

    def render(self, vx: float, vy: float, mouse_pos: Tuple[int, int], window_rect: Tuple[int, int, int, int]) -> None:
        self.screen.fill((0, 0, 0, 0))
        if vx != 0 or vy != 0:
            start, end = self.extend_line_to_edges(vx, vy, mouse_pos[0], mouse_pos[1], window_rect)
            pygame.draw.line(self.screen, self.config.line_color, start, end, width=1)
        pygame.display.flip()
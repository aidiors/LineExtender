import pygame
import win32api
import win32con
import cv2
import numpy as np

from app_config import AppConfig
from window_manager import WindowManager
from window_capture import WindowCapture
from line_detector import LineDetector
from overlay_renderer import OverlayRenderer
from settings_control import SettingsControl

class Application:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.window_manager = WindowManager(config)
        self.window_capture = WindowCapture(config.game_window_name)
        self.line_detector = LineDetector(config)
        self.renderer = OverlayRenderer(self.window_manager, config)
        self.settings_control = SettingsControl(config)
        self.running = True
        self.clock = pygame.time.Clock()
        self.last_foreground_update = 0

    def _process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

    def _check_exit_key(self) -> None:
        if win32api.GetAsyncKeyState(win32con.VK_INSERT) & 0x8000:
            self.running = False

    def _update_foreground(self) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_foreground_update > 500:
            self.window_manager.bring_to_front()
            self.last_foreground_update = current_time

    def run(self) -> None:
        try:
            self.window_capture.start()

            while self.running and self.window_capture.latest_screenshot is None:
                pygame.time.delay(10)
                self._process_events()
                self._check_exit_key()

            while self.running:
                self._process_events()
                self._check_exit_key()
                self._update_foreground()

                cv2.waitKey(1)

                mouse_pos = win32api.GetCursorPos()
                screenshot = self.window_capture.latest_screenshot

                if screenshot:
                    left = max(0, mouse_pos[0] - self.config.capture_size // 2)
                    top = max(0, mouse_pos[1] - self.config.capture_size // 2)
                    right = min(self.window_manager.screen_width, mouse_pos[0] + self.config.capture_size // 2)
                    bottom = min(self.window_manager.screen_height, mouse_pos[1] + self.config.capture_size // 2)

                    if right - left > 120 and bottom - top > 120:
                        region = screenshot.crop((left, top, right, bottom))
                        region_np = np.array(region)
                        region_cv = cv2.cvtColor(region_np, cv2.COLOR_RGB2BGR)

                        local_cursor = (mouse_pos[0] - left, mouse_pos[1] - top)

                        vx, vy = self.line_detector.detect_main_direction(region_cv, *local_cursor)

                        self.renderer.render(vx, vy, mouse_pos)

                self.clock.tick(self.config.target_fps)

        finally:
            self.shutdown()

    def shutdown(self) -> None:
        self.running = False
        self.window_capture.stop()
        pygame.quit()
        cv2.destroyAllWindows()
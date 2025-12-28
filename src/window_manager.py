import win32api
import win32con
import win32gui
import pygame

from app_config import AppConfig

class WindowManager:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.hwnd: int | None = None
        self.screen_size = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
        self._setup_overlay_window()

    def _setup_overlay_window(self) -> None:
        pygame.init()
        pygame.display.set_mode(self.screen_size, pygame.NOFRAME)
        pygame.display.set_caption("Line Detection Overlay")
        self.hwnd = pygame.display.get_wm_info()["window"]

        ex_style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
        new_style = ex_style | (
                win32con.WS_EX_LAYERED |
                win32con.WS_EX_TRANSPARENT |
                win32con.WS_EX_TOPMOST |
                win32con.WS_EX_NOACTIVATE)
        win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, new_style)
        win32gui.SetLayeredWindowAttributes(self.hwnd, 0, 0, win32con.LWA_COLORKEY)

        win32gui.SetWindowLong(self.hwnd, win32con.GWL_WNDPROC, self._prevent_window_minimize)

        self.bring_to_front()

    @staticmethod
    def _prevent_window_minimize(hwnd: int, msg: int, wparam: int, lparam: int) -> int:
        if msg == win32con.WM_SYSCOMMAND:
            if wparam in (win32con.SC_MINIMIZE, win32con.SC_CLOSE):
                return 0
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def bring_to_front(self) -> None:
        if self.hwnd:
            win32gui.SetWindowPos(
                self.hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOACTIVATE |
                win32con.SWP_NOMOVE |
                win32con.SWP_NOSIZE |
                win32con.SWP_SHOWWINDOW
            )

    @property
    def screen_width(self) -> int:
        return self.screen_size[0]

    @property
    def screen_height(self) -> int:
        return self.screen_size[1]
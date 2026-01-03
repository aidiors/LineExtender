import threading
from typing import Optional, Tuple

import win32gui
import win32ui
import win32con
from PIL import Image

class WindowCapture:
    def __init__(self, window_name: str) -> None:
        self.window_name = window_name
        self.hwnd = self._find_target_window()
        self._screenshot: Optional[Image.Image] = None
        self._lock = threading.Lock()
        self._running = True
        self._capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.window_left = 0
        self.window_top = 0
        self.window_width = 0
        self.window_height = 0

    def _find_target_window(self) -> int:
        hwnd = win32gui.FindWindow(None, self.window_name)
        if not hwnd:
            raise RuntimeError(f"Window named '{self.window_name}' not found.")
        return hwnd

    def _capture_loop(self) -> None:
        while self._running:
            try:
                screenshot = self._capture_single_frame()
                with self._lock:
                    self._screenshot = screenshot
            except Exception as e:
                print(f"Frame capture error: {str(e)}")
                self._running = False

    def _capture_single_frame(self) -> Image.Image | None:
        if win32gui.IsIconic(self.hwnd):
            win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.BringWindowToTop(self.hwnd)

        left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
        left, top = win32gui.ClientToScreen(self.hwnd, (left, top))
        right, bottom = win32gui.ClientToScreen(self.hwnd, (right, bottom))
        width, height = right - left, bottom - top

        self.window_left = left
        self.window_top = top
        self.window_width = width
        self.window_height = height

        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        save_bitmap = win32ui.CreateBitmap()
        try:
            save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
            save_dc.SelectObject(save_bitmap)
            save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

            bmp_info = save_bitmap.GetInfo()
            bmp_str = save_bitmap.GetBitmapBits(True)
            return Image.frombuffer("RGB", (bmp_info["bmWidth"], bmp_info["bmHeight"]), bmp_str, "raw", "BGRX", 0, 1)
        finally:
            win32gui.DeleteObject(save_bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwnd_dc)

    def start(self) -> None:
        self._capture_thread.start()

    def stop(self) -> None:
        self._running = False
        self._capture_thread.join(timeout=1.0)

    def get_window_rect(self) -> Tuple[int, int, int, int]:
        return self.window_left, self.window_top, self.window_width, self.window_height

    @property
    def latest_screenshot(self) -> Optional[Image.Image]:
        with self._lock:
            return self._screenshot.copy() if self._screenshot else None
import cv2
from typing import Callable

from app_config import AppConfig

class SettingsControl:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.window_name = "Detection Settings"
        self._setup_window()

    def _setup_window(self) -> None:
        cv2.namedWindow(self.window_name)

        cv2.createTrackbar(
            "Capture Size", self.window_name,
            self.config.capture_size, 800,
            self._update_capture_size
        )
        cv2.createTrackbar(
            "Hough Threshold", self.window_name,
            self.config.hough_threshold, 140,
            self._update_hough_threshold
        )
        cv2.createTrackbar(
            "Min Line Length", self.window_name,
            self.config.min_line_length, 200,
            self._update_min_line_length
        )
        cv2.createTrackbar(
            "Max Line Gap", self.window_name,
            self.config.max_line_gap, 100,
            self._update_max_line_gap
        )

    def _update_parameter(self, trackbar_name: str, min_val: int, setter: Callable[[int], None]) -> None:
        value = cv2.getTrackbarPos(trackbar_name, self.window_name)
        setter(max(min_val, value))

    def _update_capture_size(self, _) -> None:
        self._update_parameter(
            "Capture Size", 120,
            lambda v: setattr(self.config, "capture_size", v)
        )

    def _update_hough_threshold(self, _) -> None:
        self._update_parameter(
            "Hough Threshold", 1,
            lambda v: setattr(self.config, "hough_threshold", v)
        )

    def _update_min_line_length(self, _) -> None:
        self._update_parameter(
            "Min Line Length", 1,
            lambda v: setattr(self.config, "min_line_length", v)
        )

    def _update_max_line_gap(self, _) -> None:
        self._update_parameter(
            "Max Line Gap", 1,
            lambda v: setattr(self.config, "max_line_gap", v)
        )
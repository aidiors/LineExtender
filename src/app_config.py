import argparse
from dataclasses import dataclass
from typing import Tuple

from constants import DEFAULT_CONFIG

@dataclass
class AppConfig:
    game_window_name: str
    capture_size: int
    hough_threshold: int
    min_line_length: int
    max_line_gap: int
    target_fps: int
    line_color: Tuple[int, int, int]

    @classmethod
    def from_defaults(cls, game_window_name: str) -> "AppConfig":
        return cls(
            game_window_name=game_window_name,
            capture_size=DEFAULT_CONFIG["capture_size"],
            hough_threshold=DEFAULT_CONFIG["hough_threshold"],
            min_line_length=DEFAULT_CONFIG["min_line_length"],
            max_line_gap=DEFAULT_CONFIG["max_line_gap"],
            target_fps=DEFAULT_CONFIG["target_fps"],
            line_color=DEFAULT_CONFIG["line_color"]
        )

    def validate(self) -> None:
        if not self.game_window_name:
            raise ValueError("Game window name cannot be empty")

        constraints = {
            "capture_size": (120, 800),
            "hough_threshold": (1, 140),
            "min_line_length": (1, 200),
            "max_line_gap": (1, 100),
            "target_fps": (30, 1000)
        }

        for param, (min_val, max_val) in constraints.items():
            value = getattr(self, param)
            if not (min_val <= value <= max_val):
                raise ValueError(f"Parameter {param} = {value} is outside valid range [{min_val}, {max_val}]")

def parse_arguments() -> AppConfig:
    parser = argparse.ArgumentParser(description="Game line detection overlay system")
    parser.add_argument("--window", required=True, help="Exact game window name to capture")

    args = parser.parse_args()
    config = AppConfig.from_defaults(args.window)
    config.validate()

    return config
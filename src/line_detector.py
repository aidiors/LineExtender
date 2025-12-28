import math
from typing import Any, Dict, List, Tuple

import cv2
import numpy as np

from app_config import AppConfig

class LineDetector:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    @staticmethod
    def _create_line_mask(image: np.ndarray) -> np.ndarray:
        brightness_mask = cv2.inRange(image, np.array([142, 142, 142]), np.array([255, 255, 255]))

        channel_diff = np.ptp(image, axis=2)
        grayscale_mask = (channel_diff <= 29).astype(np.uint8) * 255

        return cv2.bitwise_and(brightness_mask, grayscale_mask)

    @staticmethod
    def _cluster_lines(lines: np.ndarray, cursor_pos: Tuple[int, int]) -> List[Dict[str, Any]]:
        if lines is None or len(lines) == 0:
            return []

        processed = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            dx, dy = x2 - x1, y2 - y1

            if dx < 0 or (abs(dx) < 1e-8 and dy < 0):
                x1, x2 = x2, x1
                y1, y2 = y2, y1
                dx, dy = -dx, -dy

            length = math.hypot(dx, dy)
            if length < 1e-8:
                continue

            vx, vy = dx / length, dy / length
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            normal_x, normal_y = -vy, vx
            distance_to_line = abs(normal_x * (cursor_pos[0] - mid_x) + normal_y * (cursor_pos[1] - mid_y))

            processed.append({
                "vx": vx, "vy": vy,
                "mid_x": mid_x, "mid_y": mid_y,
                "distance": distance_to_line,
                "angle": math.atan2(vy, vx)
            })

        clusters = []
        used = [False] * len(processed)
        angle_threshold = math.radians(5)
        dist_threshold = 6.0

        for i, line_i in enumerate(processed):
            if used[i]:
                continue

            cluster = [i]
            used[i] = True

            for j, line_j in enumerate(processed[i + 1:], start=i + 1):
                if used[j]:
                    continue
                angle_diff = abs(line_i["angle"] - line_j["angle"])
                if angle_diff < angle_threshold:
                    mid_diff = math.hypot(line_i["mid_x"] - line_j["mid_x"], line_i["mid_y"] - line_j["mid_y"])
                    if mid_diff < dist_threshold:
                        cluster.append(j)
                        used[j] = True

            clusters.append([processed[idx] for idx in cluster])

        return clusters

    def detect_main_direction(self, image: np.ndarray, cursor_x: int, cursor_y: int) -> Tuple[float, float]:
        if image.size == 0:
            return 0.0, 0.0

        mask = self._create_line_mask(image)
        masked = cv2.bitwise_and(image, image, mask=mask)
        gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 150)

        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi / 540,
            threshold=self.config.hough_threshold,
            minLineLength=self.config.min_line_length,
            maxLineGap=self.config.max_line_gap
        )

        clusters = self._cluster_lines(lines, (cursor_x, cursor_y))
        if not clusters:
            return 0.0, 0.0

        best_cluster = min(clusters, key=lambda c: min(l["distance"] for l in c))
        avg_vx = sum(line["vx"] for line in best_cluster) / len(best_cluster)
        avg_vy = sum(line["vy"] for line in best_cluster) / len(best_cluster)

        return avg_vx, avg_vy
"""Funções de visualização para frames e detecções."""

from typing import Any

import cv2

from .detector import Detection

DETECTION_COLOR = (0, 165, 255)
INFORMATION_COLOR = (0, 255, 0)


def draw_detections(frame: Any, detections: list[Detection]) -> Any:
    """Desenha bounding boxes, classes e confianças sobre um frame."""
    for detection in detections:
        top_left = (int(detection.x1), int(detection.y1))
        bottom_right = (int(detection.x2), int(detection.y2))
        cv2.rectangle(frame, top_left, bottom_right, DETECTION_COLOR, 2)

        label = f"{detection.class_name} {detection.confidence:.2f}"
        label_position = (top_left[0], max(20, top_left[1] - 8))
        cv2.putText(
            frame,
            label,
            label_position,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            DETECTION_COLOR,
            2,
            cv2.LINE_AA,
        )

    return frame


def draw_video_information(
    frame: Any,
    frame_number: int,
    fps: float,
    width: int,
    height: int,
) -> Any:
    """Adiciona ao frame as informações básicas do vídeo."""
    lines = (
        f"Frame: {frame_number}",
        f"FPS: {fps:.2f}",
        f"Resolucao: {width}x{height}",
    )

    for index, text in enumerate(lines):
        position = (15, 30 + index * 30)
        cv2.putText(
            frame,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            INFORMATION_COLOR,
            2,
            cv2.LINE_AA,
        )

    return frame

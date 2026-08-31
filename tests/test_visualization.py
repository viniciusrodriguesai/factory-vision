"""Testes da visualização sem abrir janelas gráficas."""

import numpy as np

from src.factory_vision.detector import Detection
from src.factory_vision.visualization import (
    DETECTION_COLOR,
    draw_detections,
    draw_video_information,
)


def test_draws_bounding_box_on_artificial_frame() -> None:
    frame = np.zeros((120, 160, 3), dtype=np.uint8)
    detection = Detection(
        x1=20,
        y1=30,
        x2=100,
        y2=90,
        confidence=0.87,
        class_id=0,
        class_name="door",
    )

    result = draw_detections(frame, [detection])

    assert result is frame
    assert tuple(frame[30, 20]) == DETECTION_COLOR
    assert np.any(frame != 0)


def test_drawing_zero_detections_preserves_frame() -> None:
    frame = np.zeros((60, 80, 3), dtype=np.uint8)

    result = draw_detections(frame, [])

    assert result is frame
    assert not np.any(frame)


def test_draws_video_information_on_artificial_frame() -> None:
    frame = np.zeros((120, 320, 3), dtype=np.uint8)

    result = draw_video_information(
        frame,
        frame_number=12,
        fps=30.0,
        width=320,
        height=120,
    )

    assert result is frame
    assert np.any(frame != 0)

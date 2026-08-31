"""Testes do detector sem carregar pesos reais ou usar GPU."""

from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

import numpy as np
import pytest

from src.factory_vision.detector import (
    Detection,
    ObjectDetector,
    validate_confidence,
)


class FakeTensor:
    def __init__(self, values: list[list[float]]) -> None:
        self.values = values

    def cpu(self) -> "FakeTensor":
        return self

    def tolist(self) -> list[list[float]]:
        return self.values


class FakeBoxes:
    def __init__(self, rows: list[list[float]]) -> None:
        self.data = FakeTensor(rows)


class FakeResult:
    def __init__(self, rows: list[list[float]], names: dict[int, str]) -> None:
        self.boxes = FakeBoxes(rows)
        self.names = names


class FakeModel:
    def __init__(self, results: list[FakeResult]) -> None:
        self.results = results
        self.calls: list[dict[str, Any]] = []

    def predict(self, **arguments: Any) -> list[FakeResult]:
        self.calls.append(arguments)
        return self.results


@pytest.fixture
def model_path(tmp_path: Path) -> Path:
    path = tmp_path / "fake_model.pt"
    path.write_bytes(b"artificial test model")
    return path


@pytest.mark.parametrize("confidence", [0.0, 0.5, 1.0])
def test_accepts_valid_confidence(confidence: float) -> None:
    assert validate_confidence(confidence) == confidence


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_rejects_confidence_outside_range(confidence: float) -> None:
    with pytest.raises(ValueError, match="entre 0 e 1"):
        validate_confidence(confidence)


def test_rejects_non_numeric_confidence() -> None:
    with pytest.raises(ValueError, match="número entre 0 e 1"):
        validate_confidence("invalid")


def test_reports_missing_model(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Modelo YOLO não encontrado"):
        ObjectDetector(tmp_path / "missing.pt")


def test_loads_model_only_once(model_path: Path) -> None:
    fake_model = FakeModel([])

    with patch(
        "src.factory_vision.detector._load_yolo_model",
        return_value=fake_model,
    ) as loader:
        detector = ObjectDetector(model_path)
        detector.detect(np.zeros((20, 20, 3), dtype=np.uint8))
        detector.detect(np.zeros((20, 20, 3), dtype=np.uint8))

    loader.assert_called_once_with(model_path)


def test_returns_zero_objects(model_path: Path) -> None:
    fake_model = FakeModel([FakeResult([], {})])

    with patch(
        "src.factory_vision.detector._load_yolo_model",
        return_value=fake_model,
    ):
        detector = ObjectDetector(model_path)

    assert detector.detect(np.zeros((20, 20, 3), dtype=np.uint8)) == []


def test_returns_one_detection_with_expected_structure(model_path: Path) -> None:
    rows = [[10.5, 20.0, 50.0, 80.5, 0.91, 2.0]]
    fake_model = FakeModel([FakeResult(rows, {2: "door"})])

    with patch(
        "src.factory_vision.detector._load_yolo_model",
        return_value=fake_model,
    ):
        detector = ObjectDetector(model_path, confidence=0.75)

    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    detections = detector.detect(frame)

    assert detections == [
        Detection(
            x1=10.5,
            y1=20.0,
            x2=50.0,
            y2=80.5,
            confidence=0.91,
            class_id=2,
            class_name="door",
        )
    ]
    assert fake_model.calls == [
        {
            "source": frame,
            "conf": 0.75,
            "device": "cpu",
            "verbose": False,
        }
    ]


def test_returns_multiple_detections(model_path: Path) -> None:
    rows = [
        [1.0, 2.0, 10.0, 20.0, 0.80, 0.0],
        [30.0, 40.0, 70.0, 90.0, 0.65, 1.0],
    ]
    fake_model = FakeModel([FakeResult(rows, {0: "door", 1: "person"})])

    with patch(
        "src.factory_vision.detector._load_yolo_model",
        return_value=fake_model,
    ):
        detector = ObjectDetector(model_path)

    detections = detector.detect(np.zeros((100, 100, 3), dtype=np.uint8))

    assert len(detections) == 2
    assert [detection.class_name for detection in detections] == ["door", "person"]
    assert all(isinstance(detection, Detection) for detection in detections)

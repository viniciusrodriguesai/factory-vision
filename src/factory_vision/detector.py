"""Detecção de objetos em frames com Ultralytics YOLO."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Detection:
    """Representa uma única detecção com bounding box e classe."""

    x1: float
    y1: float
    x2: float
    y2: float
    confidence: float
    class_id: int
    class_name: str


class ModelLoadError(RuntimeError):
    """Indica que o modelo não pôde ser carregado."""


class DetectionError(RuntimeError):
    """Indica uma falha durante a inferência em um frame."""


def validate_confidence(confidence: float | str) -> float:
    """Valida e normaliza um limiar de confiança entre zero e um."""
    try:
        value = float(confidence)
    except (TypeError, ValueError) as error:
        raise ValueError("A confiança deve ser um número entre 0 e 1.") from error

    if not 0 <= value <= 1:
        raise ValueError("A confiança deve estar entre 0 e 1.")

    return value


def _load_yolo_model(model_path: Path) -> Any:
    from ultralytics import YOLO

    return YOLO(str(model_path), task="detect")


class ObjectDetector:
    """Carrega um modelo YOLO local e detecta objetos em frames na CPU."""

    def __init__(self, model_path: str | Path, confidence: float = 0.50) -> None:
        if isinstance(model_path, str) and not model_path.strip():
            raise ValueError("O caminho do modelo não pode estar vazio.")

        self.model_path = Path(model_path)
        self.confidence = validate_confidence(confidence)

        if not self.model_path.is_file():
            raise FileNotFoundError(f"Modelo YOLO não encontrado: {self.model_path}")

        try:
            self._model = _load_yolo_model(self.model_path)
        except Exception as error:
            raise ModelLoadError(
                f"Não foi possível carregar o modelo YOLO: {self.model_path}"
            ) from error

    def detect(self, frame: Any) -> list[Detection]:
        """Executa inferência em um frame e retorna detecções simples."""
        try:
            results = self._model.predict(
                source=frame,
                conf=self.confidence,
                device="cpu",
                verbose=False,
            )
        except Exception as error:
            raise DetectionError("Falha ao executar a detecção no frame.") from error

        if not results:
            return []

        result = results[0]
        if result.boxes is None:
            return []

        detections: list[Detection] = []
        for x1, y1, x2, y2, confidence, class_id in (
            result.boxes.data.cpu().tolist()
        ):
            class_id = int(class_id)
            detections.append(
                Detection(
                    x1=float(x1),
                    y1=float(y1),
                    x2=float(x2),
                    y2=float(y2),
                    confidence=float(confidence),
                    class_id=class_id,
                    class_name=str(result.names[class_id]),
                )
            )

        return detections

"""Leitura de arquivos de vídeo com OpenCV."""

from pathlib import Path
from typing import Any

import cv2


class VideoOpenError(RuntimeError):
    """Indica que o OpenCV não conseguiu abrir um arquivo de vídeo."""


class VideoReader:
    """Encapsula a abertura, as propriedades e a leitura de um vídeo."""

    def __init__(self, video_path: str | Path) -> None:
        if isinstance(video_path, str) and not video_path.strip():
            raise ValueError("O caminho do vídeo não pode estar vazio.")

        self.path = Path(video_path)
        self._capture: cv2.VideoCapture | None = None

    @property
    def is_opened(self) -> bool:
        """Informa se existe uma captura de vídeo aberta."""
        return self._capture is not None and self._capture.isOpened()

    @property
    def fps(self) -> float:
        """Retorna o FPS informado pelo arquivo."""
        return float(self._require_open_capture().get(cv2.CAP_PROP_FPS))

    @property
    def width(self) -> int:
        """Retorna a largura dos frames em pixels."""
        return int(self._require_open_capture().get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self) -> int:
        """Retorna a altura dos frames em pixels."""
        return int(self._require_open_capture().get(cv2.CAP_PROP_FRAME_HEIGHT))

    def open(self) -> None:
        """Valida o caminho e abre o vídeo."""
        if not self.path.is_file():
            raise FileNotFoundError(f"Arquivo de vídeo não encontrado: {self.path}")

        self.release()
        capture = cv2.VideoCapture(str(self.path))

        if not capture.isOpened():
            capture.release()
            raise VideoOpenError(
                f"Não foi possível abrir o vídeo: {self.path}. "
                "Verifique se o arquivo é um vídeo válido e possui um codec compatível."
            )

        self._capture = capture

    def read(self) -> tuple[bool, Any | None]:
        """Lê o próximo frame; ``False`` indica o final do vídeo."""
        return self._require_open_capture().read()

    def release(self) -> None:
        """Libera a captura, se estiver aberta."""
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def _require_open_capture(self) -> cv2.VideoCapture:
        if not self.is_opened or self._capture is None:
            raise RuntimeError("O vídeo não está aberto.")
        return self._capture

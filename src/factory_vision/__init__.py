"""Factory Vision: detecção de objetos em vídeos industriais."""

from .detector import Detection, ObjectDetector
from .video_reader import VideoOpenError, VideoReader

__version__ = "0.0.2"

__all__ = [
    "Detection",
    "ObjectDetector",
    "VideoOpenError",
    "VideoReader",
    "__version__",
]

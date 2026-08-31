"""Factory Vision: base para processamento de vídeo industrial."""

from .video_reader import VideoOpenError, VideoReader

__version__ = "0.0.1"

__all__ = ["VideoOpenError", "VideoReader", "__version__"]

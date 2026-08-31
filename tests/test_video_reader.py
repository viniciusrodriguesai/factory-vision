"""Testes automatizados da leitura de vídeo."""

from pathlib import Path

import cv2
import numpy as np
import pytest

from src.factory_vision import VideoOpenError, VideoReader

VIDEO_WIDTH = 64
VIDEO_HEIGHT = 48
VIDEO_FPS = 10.0
VIDEO_FRAME_COUNT = 4


@pytest.fixture
def valid_video(tmp_path: Path) -> Path:
    """Cria um vídeo curto e descartável, sem usar dados da fábrica."""
    video_path = tmp_path / "video_test.avi"
    codec = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(
        str(video_path),
        codec,
        VIDEO_FPS,
        (VIDEO_WIDTH, VIDEO_HEIGHT),
    )

    if not writer.isOpened():
        pytest.skip("O codec MJPG não está disponível neste ambiente.")

    try:
        for frame_index in range(VIDEO_FRAME_COUNT):
            pixel_value = frame_index * 50
            frame = np.full(
                (VIDEO_HEIGHT, VIDEO_WIDTH, 3),
                pixel_value,
                dtype=np.uint8,
            )
            writer.write(frame)
    finally:
        writer.release()

    return video_path


def test_rejects_empty_path() -> None:
    with pytest.raises(ValueError, match="não pode estar vazio"):
        VideoReader("   ")


def test_reports_missing_file(tmp_path: Path) -> None:
    reader = VideoReader(tmp_path / "missing.mp4")

    with pytest.raises(FileNotFoundError, match="não encontrado"):
        reader.open()


def test_rejects_invalid_video(tmp_path: Path) -> None:
    invalid_video = tmp_path / "invalid.mp4"
    invalid_video.write_text("este arquivo não é um vídeo", encoding="utf-8")
    reader = VideoReader(invalid_video)

    with pytest.raises(VideoOpenError, match="vídeo válido"):
        reader.open()

    assert not reader.is_opened


def test_opens_valid_video(valid_video: Path) -> None:
    reader = VideoReader(valid_video)

    try:
        reader.open()
        assert reader.is_opened
    finally:
        reader.release()


def test_reads_video_properties(valid_video: Path) -> None:
    reader = VideoReader(valid_video)

    try:
        reader.open()
        assert reader.fps == pytest.approx(VIDEO_FPS, abs=0.5)
        assert reader.width == VIDEO_WIDTH
        assert reader.height == VIDEO_HEIGHT
    finally:
        reader.release()


def test_reads_all_frames_until_end(valid_video: Path) -> None:
    reader = VideoReader(valid_video)
    frames_read = 0

    try:
        reader.open()
        while True:
            success, frame = reader.read()
            if not success:
                assert frame is None
                break

            assert frame is not None
            assert frame.shape[:2] == (VIDEO_HEIGHT, VIDEO_WIDTH)
            frames_read += 1
    finally:
        reader.release()

    assert frames_read == VIDEO_FRAME_COUNT


def test_releases_video_resources(valid_video: Path) -> None:
    reader = VideoReader(valid_video)
    reader.open()

    reader.release()

    assert not reader.is_opened
    with pytest.raises(RuntimeError, match="não está aberto"):
        reader.read()

    reader.release()

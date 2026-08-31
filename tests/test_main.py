"""Testes da CLI e da integração do pipeline sem interface gráfica."""

from unittest.mock import Mock, patch

import numpy as np
import pytest

from src.factory_vision.main import build_argument_parser, main, play_video


def test_cli_uses_default_confidence() -> None:
    arguments = build_argument_parser().parse_args(
        ["video.mp4", "--model", "model.pt"]
    )

    assert arguments.video == "video.mp4"
    assert arguments.model == "model.pt"
    assert arguments.confidence == 0.50


@pytest.mark.parametrize("confidence", ["-0.1", "1.1", "invalid"])
def test_cli_rejects_invalid_confidence(
    confidence: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as error:
        build_argument_parser().parse_args(
            [
                "video.mp4",
                "--model",
                "model.pt",
                "--confidence",
                confidence,
            ]
        )

    assert error.value.code == 2
    assert "entre 0 e 1" in capsys.readouterr().err


def test_main_passes_cli_arguments_to_pipeline() -> None:
    with patch("src.factory_vision.main.play_video", return_value=0) as playback:
        exit_code = main(
            [
                "video.mp4",
                "--model",
                "model.pt",
                "--confidence",
                "0.65",
            ]
        )

    assert exit_code == 0
    playback.assert_called_once_with("video.mp4", "model.pt", 0.65)


def test_pipeline_releases_video_when_model_cannot_be_loaded() -> None:
    reader = Mock()

    with (
        patch("src.factory_vision.main.VideoReader", return_value=reader),
        patch(
            "src.factory_vision.main.ObjectDetector",
            side_effect=FileNotFoundError("modelo ausente"),
        ),
    ):
        exit_code = play_video("video.mp4", "missing.pt", 0.50)

    assert exit_code == 1
    reader.open.assert_called_once_with()
    reader.release.assert_called_once_with()


def test_pipeline_processes_artificial_frame_without_opening_window() -> None:
    frame = np.zeros((80, 120, 3), dtype=np.uint8)
    reader = Mock()
    reader.fps = 25.0
    reader.width = 120
    reader.height = 80
    reader.read.side_effect = [(True, frame), (False, None)]

    detector = Mock()
    detector.detect.return_value = []

    with (
        patch("src.factory_vision.main.VideoReader", return_value=reader),
        patch("src.factory_vision.main.ObjectDetector", return_value=detector),
        patch("src.factory_vision.main.cv2.imshow") as imshow,
        patch("src.factory_vision.main.cv2.waitKey", return_value=-1),
        patch("src.factory_vision.main.cv2.destroyAllWindows") as destroy_windows,
    ):
        exit_code = play_video("video.mp4", "model.pt", 0.50)

    assert exit_code == 0
    reader.open.assert_called_once_with()
    detector.detect.assert_called_once_with(frame)
    imshow.assert_called_once()
    reader.release.assert_called_once_with()
    destroy_windows.assert_called_once_with()

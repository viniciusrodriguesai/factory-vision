"""Interface de linha de comando do Factory Vision v0.0.2."""

import argparse
from collections.abc import Sequence
import cv2

from .detector import (
    DetectionError,
    ModelLoadError,
    ObjectDetector,
    validate_confidence,
)
from .video_reader import VideoOpenError, VideoReader
from .visualization import draw_detections, draw_video_information

WINDOW_NAME = "Factory Vision v0.0.2"


def play_video(video_path: str, model_path: str, confidence: float) -> int:
    """Detecta objetos em um vídeo até o fim ou até a tecla Q."""
    try:
        detector = ObjectDetector(model_path, confidence)
    except (ValueError, FileNotFoundError, ModelLoadError) as error:
        print(f"Erro: {error}")
        return 1

    try:
        reader = VideoReader(video_path)
        reader.open()
    except (ValueError, FileNotFoundError, VideoOpenError) as error:
        print(f"Erro: {error}")
        return 1

    try:
        fps = reader.fps
        width = reader.width
        height = reader.height
        wait_time_ms = max(1, round(1000 / fps)) if fps > 0 else 1
        frame_number = 0

        while True:
            success, frame = reader.read()
            if not success:
                print("Fim do vídeo.")
                break

            frame_number += 1
            detections = detector.detect(frame)
            draw_detections(frame, detections)
            draw_video_information(frame, frame_number, fps, width, height)
            cv2.imshow(WINDOW_NAME, frame)

            pressed_key = cv2.waitKey(wait_time_ms) & 0xFF
            if pressed_key in (ord("q"), ord("Q")):
                print("Reprodução encerrada pelo usuário.")
                break
    except (cv2.error, DetectionError) as error:
        print(f"Erro durante o processamento do vídeo: {error}")
        return 1
    finally:
        reader.release()
        cv2.destroyAllWindows()

    return 0


def build_argument_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos da aplicação."""
    parser = argparse.ArgumentParser(
        description="Detecta objetos em um vídeo local com Ultralytics YOLO."
    )
    parser.add_argument("video", help="caminho do arquivo de vídeo")
    parser.add_argument(
        "--model",
        required=True,
        help="caminho de um modelo YOLO local",
    )
    parser.add_argument(
        "--confidence",
        type=parse_confidence_argument,
        default=0.50,
        help="confiança mínima entre 0 e 1 (padrão: 0.50)",
    )
    return parser


def parse_confidence_argument(value: str) -> float:
    """Converte a confiança da CLI em um valor validado."""
    try:
        return validate_confidence(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def main(argv: Sequence[str] | None = None) -> int:
    """Processa os argumentos da linha de comando e executa a aplicação."""
    arguments = build_argument_parser().parse_args(argv)
    return play_video(arguments.video, arguments.model, arguments.confidence)


if __name__ == "__main__":
    raise SystemExit(main())

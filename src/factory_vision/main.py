"""Interface de linha de comando do Factory Vision v0.0.1."""

import argparse
from collections.abc import Sequence
from typing import Any

import cv2

from .video_reader import VideoOpenError, VideoReader

WINDOW_NAME = "Factory Vision v0.0.1"


def add_video_information(
    frame: Any,
    frame_number: int,
    fps: float,
    width: int,
    height: int,
) -> None:
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
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )


def play_video(video_path: str) -> int:
    """Abre e reproduz um arquivo de vídeo até o fim ou até a tecla Q."""
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
            add_video_information(frame, frame_number, fps, width, height)
            cv2.imshow(WINDOW_NAME, frame)

            pressed_key = cv2.waitKey(wait_time_ms) & 0xFF
            if pressed_key in (ord("q"), ord("Q")):
                print("Reprodução encerrada pelo usuário.")
                break
    except cv2.error as error:
        print(f"Erro do OpenCV durante a reprodução: {error}")
        return 1
    finally:
        reader.release()
        cv2.destroyAllWindows()

    return 0


def build_argument_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos da aplicação."""
    parser = argparse.ArgumentParser(
        description="Reproduz um arquivo de vídeo com seus metadados básicos."
    )
    parser.add_argument("video", help="caminho do arquivo de vídeo")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Processa os argumentos da linha de comando e executa a aplicação."""
    arguments = build_argument_parser().parse_args(argv)
    return play_video(arguments.video)


if __name__ == "__main__":
    raise SystemExit(main())

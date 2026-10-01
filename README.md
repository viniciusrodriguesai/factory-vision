# Factory Vision

An incremental computer vision project for manufacturing video analysis. The current release, **v0.0.1**, implements a local video reader using OpenCV.

## Implemented

- Validate local paths and report missing or unreadable videos.
- Read frames sequentially and display frame number, reported FPS and resolution.
- Stop at the end of the video or when Q is pressed.
- Release the capture and close windows safely.
- Test capture behavior with temporary synthetic videos.

## Run locally

Use Python 3.10 or later and a graphical desktop. Create and activate a virtual environment, then:

```bash
python -m pip install -r requirements.txt
python -m src.factory_vision.main /path/to/video.mp4
```

The video must use a codec supported by the local OpenCV installation. On Windows, pass a quoted Windows path instead.

## Tests

```bash
python -m pytest -q
```

Tests use synthetic video and do not open a graphical window. Seven tests passed during the portfolio audit; desktop playback was not manually validated in that environment.

## Architecture

`src/factory_vision/video_reader.py` manages the capture lifecycle and metadata. `src/factory_vision/main.py` handles terminal input, display and keyboard interaction.

## Planned work

Door detection, counting, event storage, production downtime, cycle time, multiple cameras and defect detection are future milestones. They are not implemented in this release, and no detection accuracy or industrial deployment results are available.

## Data policy

Use synthetic or appropriately licensed public footage for examples. Do not commit private factory footage, employee images, camera addresses or credentials. See [data/README.md](data/README.md).

## License

[MIT](LICENSE).

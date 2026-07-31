# Contributing

Contributions are welcome. This is a small, single-purpose utility, so please
keep changes focused and easy to review.

## Reporting issues

When filing a bug, please include:

- Windows version, and whether you are running from source or from the
  installer.
- The camera model or, if unknown, whether the camera exposes an H.264 RTSP
  stream (most do).
- The relevant log output from the GUI or CLI. Enable `debug: true` in
  `config.json` first if the issue is related to FFmpeg itself.
- Whatever changed between "it worked" and "it broke," if applicable.

Never paste your raw `config.json` into an issue — it contains your camera's
RTSP credentials. Redact the username/password before sharing.

## Development setup

```
git clone https://github.com/Rahideh/rtsp-virtual-webcam.git
cd REPO-NAME-HERE
pip install -r requirements.txt
```

The core pipeline logic lives in `engine.py` and is shared by both the CLI
(`main.py`) and the GUI (`gui.py`). If you are changing pipeline behavior
(reconnect logic, delay buffering, backend selection), make the change in
`engine.py` so both front ends stay in sync.

## Code style

- Keep the video/audio pipeline logic backend-agnostic where possible; new
  virtual camera or virtual audio backends should be added as configuration
  options, not hardcoded assumptions.
- Prefer small, testable functions over large ones, particularly in
  `engine.py`.
- Comments and log messages in the existing code are in Persian, matching the
  project's primary audience; new contributions in either English or Persian
  are fine, but please don't mix languages within the same function.

## Pull requests

- Describe what the change does and why, not just what it does.
- If the change affects the installer (`installer/setup.iss`), please test it
  on a clean Windows VM before submitting, since Inno Setup scripts are hard
  to review for correctness from the diff alone.

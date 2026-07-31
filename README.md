# RTSP Virtual Webcam

Turn any RTSP IP camera into a virtual webcam and microphone that any
application can use — Google Meet, Zoom, Teams, Discord, OBS, whatever reads
from a standard camera/microphone device on Windows.

[![Latest Release](https://img.shields.io/github/v/release/Rahideh/rtsp-virtual-webcam)](https://github.com/Rahideh/rtsp-virtual-webcam/releases)
[![License](https://img.shields.io/github/license/Rahideh/rtsp-virtual-webcam)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue)](https://github.com/Rahideh/rtsp-virtual-webcam)

Persian translation: [Translations/README.fa.md](Translations/README.fa.md)

## Demo

![RTSP Virtual Webcam Demo](images/demo.gif)

## Why this exists

Most commercial "IP camera as webcam" tools are either paid, bundled with
software you don't need, or too heavy for what is fundamentally a small
pipeline: decode an RTSP stream and hand the frames to a virtual device. This
project is that small pipeline, with a GUI, a reconnect strategy, and an
installer, and nothing else.

## Features

- Streams RTSP video to a virtual webcam via UnityCapture (no OBS Studio
  required) or, optionally, via OBS Studio's virtual camera driver.
- Streams RTSP audio to a virtual microphone via VB-Audio VB-CABLE.
- Hardware-accelerated video decoding (`-hwaccel`), so CPU usage stays low.
- Automatic reconnect if the camera drops the connection.
- Configurable audio/video delay to correct sync drift between the two
  independent RTSP sub-connections.
- A GUI (Tkinter, no extra dependencies) and a CLI, sharing the same engine.
- A Windows installer (Inno Setup) that registers the virtual camera driver
  automatically and walks the user through the one remaining manual step
  (installing VB-CABLE, which cannot legally be bundled — see
  [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)).

## Requirements

### Using the Windows Installer

The installer is the recommended way to use RTSP Virtual Webcam. You only need:

- Windows 10 or 11 (64-bit)
- An IP camera that provides an RTSP stream
- [VB-Audio VB-CABLE](https://vb-audio.com/Cable/) for virtual microphone support

The installer automatically handles the virtual webcam driver setup. FFmpeg and
the required application components are included with the packaged application.

## Quick Start

1. Download the latest installer from [Releases](../../releases).
2. Install RTSP Virtual Webcam.
3. Install VB-Audio VB-CABLE when prompted.
4. Enter your camera's RTSP URL.
5. Start the stream.
6. Select `RTSP Virtual Webcam` as the camera in Google Meet, Zoom, Teams, or another application.
7. Select the VB-CABLE recording device as the microphone if audio is enabled.


### Running from Source

If you want to run RTSP Virtual Webcam directly from source, you will need:

- Windows 10 or 11 (64-bit)
- Python 3.10+
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) (`ffmpeg.exe` and `ffprobe.exe`)
- [UnityCapture](https://github.com/schellingb/UnityCapture) (default) or
  [OBS Studio](https://obsproject.com/) as the virtual webcam backend
- [VB-Audio VB-CABLE](https://vb-audio.com/Cable/) for virtual microphone support
- An IP camera that provides an RTSP stream (H.264 video is recommended)

## How it works

The camera is read over two independent RTSP connections, because the video
and audio are consumed by two separate FFmpeg processes:

```text
RTSP camera --(video, FFmpeg)--> raw frames --> virtual webcam (UnityCapture / OBS)
RTSP camera --(audio, FFmpeg)--> raw PCM   --> virtual microphone (VB-CABLE)
```

```text
                 ┌──────────────┐
                 │  IP Camera   │
                 │    RTSP      │
                 └──────┬───────┘
                        │
              ┌─────────┴─────────┐
              │                   │
           Video                Audio
              │                   │
           FFmpeg              FFmpeg
              │                   │
        UnityCapture          VB-CABLE
              │                   │
       Virtual Webcam      Virtual Microphone
              │                   │
              └─────────┬─────────┘
                        │
             Google Meet / Zoom / ...
```

Both processes are supervised by a small Python engine (`engine.py`) that
reconnects on failure and optionally delays one stream relative to the other
to keep them in sync. See [`engine.py`](engine.py) for the implementation.

## Installation

### Option A: Windows installer (recommended)

Download the latest `RTSP-Virtual-Webcam-Setup.exe` from the
[Releases](../../releases) page and run it. The installer registers the
UnityCapture driver automatically and prompts you to install VB-CABLE (one
manual step, for licensing reasons — see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)).

### Option B: Run from source

```
git clone https://github.com/Rahideh/rtsp-virtual-webcam.git
cd rtsp-virtual-webcam
pip install -r requirements.txt
```

Install FFmpeg, UnityCapture (or OBS Studio), and VB-CABLE manually — see
the step-by-step instructions further down this file.

#### Installing FFmpeg

Download a build from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/)
("release essentials" is enough) and either add its `bin` folder to your
`PATH`, or place `ffmpeg.exe` and `ffprobe.exe` next to this project's `.py`
files.

#### Installing UnityCapture (default virtual webcam backend)

1. Download `UnityCaptureFilter32.dll` and `UnityCaptureFilter64.dll` from
   [github.com/schellingb/UnityCapture/tree/master/Install](https://github.com/schellingb/UnityCapture/tree/master/Install).
2. Open an **administrator** Command Prompt and register both:
   ```
   regsvr32 "C:\path\to\UnityCaptureFilter64.dll"
   regsvr32 "C:\path\to\UnityCaptureFilter32.dll"
   ```
3. That's it — no need to install or run OBS Studio.

If you'd rather use OBS Studio instead, install it, open it once, click
**Start Virtual Camera** then **Stop Virtual Camera** (this registers the
driver), and set `"video_backend": "obs"` in `config.json`.

#### Installing VB-Audio VB-CABLE

Download and run the installer from
[vb-audio.com/Cable](https://vb-audio.com/Cable/), then reboot. This creates
two audio devices: `CABLE Input` (playback) and `CABLE Output` (recording).

## Configuration

Copy `config.example.json` to `config.json` and edit it:

```json
{
  "rtsp_url": "rtsp://username:password@192.168.1.50:554/stream1",
  "rtsp_transport": "tcp",
  "audio_output_device": "CABLE Input (VB-Audio Virtual Cable)",
  "reconnect_delay_seconds": 3,
  "video_delay_ms": 0,
  "audio_delay_ms": 0,
  "hwaccel": "auto",
  "video_backend": "unitycapture",
  "debug": false
}
```

**`config.json` contains your camera's username and password. It is
git-ignored by default — do not remove it from `.gitignore`, and never paste
its contents into an issue or a public forum.**

| Field | Description |
|---|---|
| `rtsp_url` | Full RTSP URL of your camera, including credentials if required. |
| `rtsp_transport` | `tcp` (recommended, more reliable) or `udp`. |
| `audio_output_device` | Name or index of the virtual audio device (run `list_audio_devices.py` or use the GUI's dropdown to find it). |
| `reconnect_delay_seconds` | Wait time before retrying after a dropped connection. |
| `video_delay_ms` / `audio_delay_ms` | Intentional delay to correct audio/video sync drift. Only one of these is normally non-zero. See Troubleshooting. |
| `hwaccel` | `auto` (recommended), a specific FFmpeg hwaccel method (e.g. `d3d11va`), or `none` to force software decoding. |
| `video_backend` | `unitycapture` (default, lightweight) or `obs`. |
| `debug` | Set to `true` to see FFmpeg's own log output, for troubleshooting. |

## Usage

### GUI

```
python gui.py
```

Enter the RTSP URL, pick the audio device from the dropdown, and click Run.
Settings are saved to `config.json` automatically.

### CLI

```
python main.py
```

Reads `config.json` from the current directory (or a path passed via
`--config`).

## Tested With

### Cameras

- H.264 RTSP IP cameras

### Applications

- Google Meet
- Zoom
- Microsoft Teams
- Discord
- OBS Studio

### Windows

- Windows 10 64-bit
- Windows 11 64-bit

## Troubleshooting

**Audio and video are out of sync.** This is expected: video and audio are
each read over a separate RTSP connection with slightly different pipeline
latency, and there is no shared clock between them. Measure the offset (for
example, clap and time how long the sound lags the video) and set
`video_delay_ms` (or `audio_delay_ms`, if audio is ahead) to that value in
milliseconds. The offset should be constant for a given camera/network, so
you only need to tune it once.

**High CPU or RAM usage.** Make sure `hwaccel` is set to `auto` — this offloads
H.264 decoding to the GPU. If your camera offers a lower-resolution substream
(often `stream2` or similar), use that instead of the main stream; it is
usually more than sufficient for video calls and dramatically lighter.

**A console window pops up for FFmpeg when running the packaged .exe.** This
should not happen — subprocess calls use `CREATE_NO_WINDOW`. If you see this,
please open an issue with your Windows version.

**Video shows inverted colors (blue/red swapped).** Change `pix_fmt bgr24`
to `rgb24` and `PixelFormat.BGR` to `PixelFormat.RGB` in
`start_ffmpeg_video()` / `video_worker()` in `engine.py`.

**The camera only allows one RTSP session at a time.** Some budget cameras
enforce this. Since this project opens two separate connections (one for
video, one for audio), you would need a single FFmpeg process demuxing both
streams into two output pipes instead. Open an issue if you hit this — it's
a solvable but non-trivial change.

## Building the installer

See [installer/PACKAGING.md](installer/PACKAGING.md) for the full,
step-by-step process of producing `RTSP-Virtual-Webcam-Setup.exe` from
source.

## Acknowledgments

This project relies on FFmpeg, UnityCapture, pyvirtualcam, sounddevice, and
VB-Audio VB-CABLE. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for
licensing details on each.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

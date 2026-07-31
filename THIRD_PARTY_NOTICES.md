# Third-Party Notices

This project does not vendor or redistribute the binaries listed below. It
either invokes them as external processes, links against their public Python
bindings, or asks the installer to fetch them from their official source at
build or install time. This file exists so users and downstream packagers
understand what each dependency is, where it comes from, and under what terms
it is licensed.

## FFmpeg / FFprobe

- Project: https://ffmpeg.org
- Used for: decoding the RTSP video and audio streams.
- License: depends on the specific build (LGPL or GPL). This repository does
  not include FFmpeg binaries; users download their own build (see README).
- If you package a build of FFmpeg together with this application, you are
  responsible for complying with the license of that specific build.

## UnityCapture

- Project: https://github.com/schellingb/UnityCapture
- Used for: registering a virtual webcam device on Windows without requiring
  a full OBS Studio installation.
- License: MIT. The compiled filter DLLs may be redistributed; see the
  UnityCapture repository for the full license text.

## pyvirtualcam

- Project: https://github.com/letmaik/pyvirtualcam
- Used for: sending decoded video frames to the virtual camera device
  (OBS Virtual Camera or UnityCapture backend).
- License: MIT.

## sounddevice / NumPy

- Projects: https://python-sounddevice.readthedocs.io, https://numpy.org
- Used for: audio playback to the selected virtual audio device, and raw
  frame handling.
- License: MIT (sounddevice), BSD (NumPy).

## VB-Audio VB-CABLE

- Project: https://vb-audio.com/Cable/
- Used for: exposing the camera's audio as a virtual microphone that other
  applications (Google Meet, Zoom, Teams, etc.) can select.
- License: Donationware, proprietary. VB-CABLE is not bundled with this
  project. The installer either links to the official download page or
  downloads the installer directly from VB-Audio's own domain at install
  time. Bundling or redistributing the VB-CABLE installer directly requires
  a separate agreement with VB-Audio; see https://vb-audio.com/Services/licensing.htm.

## Inno Setup

- Project: https://jrsoftware.org/isinfo.php
- Used for: building the Windows installer from `installer/setup.iss`.
- License: free for any use, including commercial, per the Inno Setup
  license terms; the compiler itself is not redistributed with this project.

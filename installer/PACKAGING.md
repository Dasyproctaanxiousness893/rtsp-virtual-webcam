# Packaging Guide — Building the Windows Installer

This document explains how to produce `RTSP-Virtual-Webcam-Setup.exe`, a
standard Windows installer that end users can double-click, with no need for
Python, a command line, or a manual OBS Studio install.

Persian translation: [../Translations/PACKAGING.fa.md](../Translations/PACKAGING.fa.md)

## 1. A licensing note on VB-Audio VB-CABLE (read this first)

Per VB-Audio's own terms
([vb-audio.com/Cable](https://vb-audio.com/Cable/),
[shop.vb-audio.com](https://shop.vb-audio.com/en/win-apps/11-vb-cable.html)),
bundling or integrating the VB-CABLE installer inside another piece of
software requires contacting VB-Audio directly for a distribution
agreement. Downloading it yourself, directly from their site, for personal
use is free (donationware) — but shipping their installer inside our own
installer and distributing that publicly on GitHub is a different thing.

For that reason, `setup.iss` does not bundle the VB-CABLE installer. Instead:

- The installer has a mandatory checkbox the user must check to continue.
- Two buttons are offered: one opens the official VB-CABLE download page in
  the browser; the other runs `install-vbcable.ps1`, which downloads the
  installer directly from VB-Audio's own domain at install time and runs it.

**If you want a fully bundled, silent install:** contact VB-Audio through
their [contact form](https://vb-audio.com/Services/contact.htm) and request
a distribution/bundle license. If they agree, the `setup.iss` script can be
modified to include their installer directly and run it silently
(`-i -h`) — open an issue or ask for that variant.

## 2. Files you need in `installer/files` before compiling

| File | Where to get it |
|---|---|
| `RTSP-Virtual-Webcam.exe` | Built with PyInstaller — see section 3 below. |
| `ffmpeg.exe`, `ffprobe.exe` | Download the "release essentials" build from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/) and take these two files from its `bin` folder. |
| `UnityCaptureFilter32.dll`, `UnityCaptureFilter64.dll` | Download directly from [github.com/schellingb/UnityCapture/tree/master/Install](https://github.com/schellingb/UnityCapture/tree/master/Install) (MIT license, prebuilt, no build step needed). |
| `install-vbcable.ps1` | Already present in `installer/files/` — nothing to do. |

**One more required step:** open `installer/setup.iss` and replace
`REPO-NAME-HERE` in the `#define MyAppGitHubURL` line with your actual
GitHub repository URL. It is shown on the installer's welcome page.

## 3. Building `RTSP-Virtual-Webcam.exe` with PyInstaller

```
cd rtsp_to_webcam
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --name RTSP-Virtual-Webcam gui.py
```

Copy the resulting `dist\RTSP-Virtual-Webcam.exe` into `installer\files\`.

## 4. Installing Inno Setup and compiling the installer

1. Install Inno Setup (free) from [jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php).
2. Open `installer\setup.iss` in the Inno Setup Compiler.
3. Confirm all files from section 2 are present in `installer\files\`.
4. Build → Compile (or press F9).
5. The final installer is written to `installer\Output\RTSP-Virtual-Webcam-Setup.exe`.

Upload that file directly to a GitHub Release — do not commit it to the
repository itself (see `.gitignore`).

## 5. What the end user experiences

1. Runs `RTSP-Virtual-Webcam-Setup.exe` (one Administrator prompt).
2. Sees a welcome page with a short description of the project, the author,
   and links to the website and GitHub repository.
3. Reaches the "Virtual audio cable" page with two buttons — download
   manually, or run the PowerShell auto-installer — and a mandatory checkbox
   that blocks progress until checked.
4. The rest of the install (file copy, UnityCapture driver registration)
   happens automatically.
5. The application (the packaged `gui.py`) launches at the end.

## 6. Testing before release

Test on a clean Windows install or VM snapshot (no OBS/UnityCapture/VB-CABLE
already installed) and confirm:

- Installation completes without errors.
- The UnityCapture driver is actually registered (any application should
  see a camera named "Unity Video Capture").
- After installing VB-CABLE manually and rebooting, audio works end to end.
- Uninstalling from Control Panel correctly unregisters the UnityCapture
  driver as well.

This installer has not been compiled or run on an actual Windows machine by
the author of this guide (developed in a Linux sandbox) — if you hit a
compile or runtime error, please open an issue with the exact error message.

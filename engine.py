"""
Engine
------
هسته‌ی اصلی پروژه: پروب کردن استریم RTSP و اجرای پایپ‌لاین‌های ویدیو/صدا.
هم main.py (خط فرمان) و هم gui.py (رابط گرافیکی) از این ماژول استفاده می‌کنن.
تابع‌های video_worker/audio_worker یک callback به اسم log می‌گیرن تا پیام‌ها رو
چه در کنسول چاپ کنن چه در پنجره‌ی گرافیکی نشون بدن.
"""

import json
import os
import queue
import subprocess
import threading
import time

import numpy as np
import pyvirtualcam
import sounddevice as sd

# جلوگیری از باز شدن پنجره‌ی کنسول جداگانه برای هر زیرفرایند (ffmpeg/ffprobe)
# وقتی برنامه‌ی اصلی (GUI) خودش کنسول نداره (مثلاً exe ساخته‌شده با --noconsole).
_NO_WINDOW = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def read_exact(stream, n: int):
    """دقیقاً n بایت از یک stream می‌خونه. اگر اتصال قطع بشه None برمی‌گردونه."""
    buf = bytearray()
    while len(buf) < n:
        chunk = stream.read(n - len(buf))
        if not chunk:
            return None
        buf.extend(chunk)
    return bytes(buf)


def terminate_process(proc: subprocess.Popen) -> None:
    if proc is None:
        return
    try:
        proc.terminate()
        proc.wait(timeout=3)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


class DelayBuffer:
    """صفی که هر آیتم رو با timestamp لحظه‌ی ورود نگه می‌داره و امکان مصرف با
    تأخیر عمدی (delay_seconds) رو می‌ده؛ برای هم‌گام‌سازی صدا/تصویر."""

    def __init__(self):
        self._q = queue.Queue()

    def put(self, item) -> None:
        self._q.put((time.monotonic(), item))

    def get_delayed(self, delay_seconds: float, stop_event: threading.Event):
        while not stop_event.is_set():
            try:
                ts, item = self._q.get(timeout=0.5)
            except queue.Empty:
                continue
            target = ts + delay_seconds
            while True:
                remaining = target - time.monotonic()
                if remaining <= 0 or stop_event.is_set():
                    break
                time.sleep(min(remaining, 0.05))
            if stop_event.is_set():
                return
            yield item


def probe_video_stream(rtsp_url: str, rtsp_transport: str):
    """با ffprobe عرض/ارتفاع/فریم‌ریت واقعی دوربین رو می‌خونه."""
    cmd = [
        "ffprobe", "-v", "error",
        "-rtsp_transport", rtsp_transport,
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate",
        "-of", "json",
        rtsp_url,
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=15, creationflags=_NO_WINDOW
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    data = json.loads(result.stdout)
    if not data.get("streams"):
        raise RuntimeError("جریان ویدیویی در RTSP پیدا نشد")
    stream = data["streams"][0]
    width = int(stream["width"])
    height = int(stream["height"])
    num, den = stream["r_frame_rate"].split("/")
    den = int(den) if int(den) != 0 else 1
    fps = (int(num) / den) if den else 25.0
    if fps <= 0 or fps > 120:
        fps = 25.0
    return width, height, fps


def start_ffmpeg_video(rtsp_url, rtsp_transport, debug, hwaccel="auto"):
    cmd = ["ffmpeg", "-rtsp_transport", rtsp_transport]
    if hwaccel and hwaccel != "none":
        # decode را به GPU می‌سپاریم تا مصرف CPU به‌شدت کم بشه
        cmd += ["-hwaccel", hwaccel]
    cmd += [
        "-i", rtsp_url,
        "-an",
        "-f", "rawvideo",
        "-pix_fmt", "bgr24",
        "-",
    ]
    stderr_target = None if debug else subprocess.DEVNULL
    return subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=stderr_target, creationflags=_NO_WINDOW
    )


def start_ffmpeg_audio(rtsp_url, rtsp_transport, debug):
    cmd = [
        "ffmpeg", "-rtsp_transport", rtsp_transport,
        "-i", rtsp_url,
        "-vn",
        "-f", "s16le",
        "-acodec", "pcm_s16le",
        "-ar", "48000",
        "-ac", "2",
        "-",
    ]
    stderr_target = None if debug else subprocess.DEVNULL
    return subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=stderr_target, creationflags=_NO_WINDOW
    )


def list_output_audio_devices():
    """لیست دستگاه‌های صوتی که قابلیت خروجی/پخش دارن رو برمی‌گردونه:
    [(index, name, hostapi_name), ...] — برای پر کردن dropdown در GUI."""
    devices = sd.query_devices()
    hostapis = sd.query_hostapis()
    result = []
    for idx, d in enumerate(devices):
        if d.get("max_output_channels", 0) > 0:
            hostapi_name = hostapis[d["hostapi"]]["name"]
            result.append((idx, d["name"], hostapi_name))
    return result


def video_worker(config, width, height, fps, stop_event, log):
    frame_size = width * height * 3
    reconnect_delay = config.get("reconnect_delay_seconds", 3)
    video_delay = config.get("video_delay_ms", 0) / 1000.0
    debug = config.get("debug", False)
    hwaccel = config.get("hwaccel", "auto")
    video_backend = config.get("video_backend", "unitycapture")
    if video_backend in (None, "", "auto"):
        video_backend = None

    while not stop_event.is_set():
        proc = start_ffmpeg_video(config["rtsp_url"], config.get("rtsp_transport", "tcp"), debug, hwaccel)
        buf = DelayBuffer()
        reader_stop = threading.Event()

        def reader():
            while not reader_stop.is_set() and not stop_event.is_set():
                raw = read_exact(proc.stdout, frame_size)
                if raw is None:
                    buf.put(None)
                    return
                buf.put(raw)

        reader_thread = threading.Thread(target=reader, daemon=True)
        reader_thread.start()

        try:
            with pyvirtualcam.Camera(
                width=width, height=height, fps=fps, fmt=pyvirtualcam.PixelFormat.BGR,
                backend=video_backend,
            ) as cam:
                extra = f" | تأخیر عمدی: {video_delay * 1000:.0f}ms" if video_delay > 0 else ""
                log(f"[ویدیو] دوربین مجازی فعال شد: {cam.device} ({width}x{height} @ {fps:.1f}fps){extra}")
                for raw in buf.get_delayed(video_delay, stop_event):
                    if raw is None:
                        log("[ویدیو] اتصال به دوربین قطع شد، تلاش مجدد...")
                        break
                    frame = np.frombuffer(raw, dtype=np.uint8).reshape((height, width, 3))
                    cam.send(frame)
        except Exception as e:
            log(f"[ویدیو] خطا: {e}")
        finally:
            reader_stop.set()
            terminate_process(proc)
            reader_thread.join(timeout=2)

        if not stop_event.is_set():
            time.sleep(reconnect_delay)


def audio_worker(config, stop_event, log):
    reconnect_delay = config.get("reconnect_delay_seconds", 3)
    audio_delay = config.get("audio_delay_ms", 0) / 1000.0
    debug = config.get("debug", False)
    device = config.get("audio_output_device")
    if device is None:
        log("[صدا] audio_output_device تنظیم نشده؛ مسیر صدا غیرفعال است.")
        return

    samplerate = 48000
    channels = 2
    chunk_ms = 20
    chunk_bytes = int(samplerate * chunk_ms / 1000) * channels * 2  # 2 بایت به ازای هر sample

    while not stop_event.is_set():
        proc = start_ffmpeg_audio(config["rtsp_url"], config.get("rtsp_transport", "tcp"), debug)
        buf = DelayBuffer()
        reader_stop = threading.Event()

        def reader():
            while not reader_stop.is_set() and not stop_event.is_set():
                data = read_exact(proc.stdout, chunk_bytes)
                if data is None:
                    buf.put(None)
                    return
                buf.put(data)

        reader_thread = threading.Thread(target=reader, daemon=True)
        reader_thread.start()

        try:
            with sd.RawOutputStream(
                samplerate=samplerate, channels=channels, dtype="int16", device=device, latency="low"
            ) as stream:
                extra = f" | تأخیر عمدی: {audio_delay * 1000:.0f}ms" if audio_delay > 0 else ""
                log(f"[صدا] در حال پخش روی دستگاه: {device}{extra}")
                for data in buf.get_delayed(audio_delay, stop_event):
                    if data is None:
                        log("[صدا] اتصال به دوربین قطع شد، تلاش مجدد...")
                        break
                    stream.write(data)
        except Exception as e:
            log(f"[صدا] خطا: {e}")
        finally:
            reader_stop.set()
            terminate_process(proc)
            reader_thread.join(timeout=2)

        if not stop_event.is_set():
            time.sleep(reconnect_delay)


def run_pipeline(config, stop_event, log):
    """probe می‌کنه و ترد‌های ویدیو/صدا رو راه می‌ندازه. لیست thread ها رو برمی‌گردونه.
    اگر probe شکست بخوره یک Exception پرتاب می‌شه (caller باید مدیریتش کنه)."""
    log("در حال دریافت مشخصات ویدیوی دوربین (ffprobe)...")
    width, height, fps = probe_video_stream(config["rtsp_url"], config.get("rtsp_transport", "tcp"))
    threads = [
        threading.Thread(target=video_worker, args=(config, width, height, fps, stop_event, log), daemon=True),
        threading.Thread(target=audio_worker, args=(config, stop_event, log), daemon=True),
    ]
    for t in threads:
        t.start()
    return threads

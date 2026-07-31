"""
RTSP to Virtual Webcam/Microphone — نسخه‌ی خط فرمان (CLI)
------------------------------------------------------------
دوربین IP (RTSP) رو به یک وبکم و میکروفون مجازی تبدیل می‌کنه.
برای رابط گرافیکی (بدون نیاز به cmd) به‌جای این فایل، gui.py را اجرا کنید.

نیازمندی‌ها (به README.md مراجعه کنید):
  - FFmpeg و FFprobe در PATH سیستم
  - OBS Studio نصب شده باشه (فقط برای ثبت درایور OBS Virtual Camera)
  - VB-Audio Virtual Cable یا Virtual Audio Cable نصب شده باشه
  - pip install -r requirements.txt
"""

import argparse
import json
import sys
import threading
import time
from datetime import datetime

import engine


def log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="تبدیل دوربین RTSP به وبکم و میکروفون مجازی")
    parser.add_argument("--config", default="config.json", help="مسیر فایل تنظیمات")
    args = parser.parse_args()

    try:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        log(f"فایل تنظیمات پیدا نشد: {args.config}")
        log("یک نسخه از config.example.json بسازید و آن را ویرایش کنید.")
        sys.exit(1)

    stop_event = threading.Event()
    try:
        threads = engine.run_pipeline(config, stop_event, log)
    except Exception as e:
        log(f"اتصال به دوربین ناموفق بود: {e}")
        log("آدرس RTSP، یوزر/پسورد و روشن بودن دوربین را بررسی کنید.")
        sys.exit(1)

    log("در حال اجرا... برای توقف کلید Ctrl+C را بزنید.")
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        log("در حال خاموش کردن...")
        stop_event.set()
        for t in threads:
            t.join(timeout=5)
        log("متوقف شد.")


if __name__ == "__main__":
    main()

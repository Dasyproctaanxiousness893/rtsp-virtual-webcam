"""
RTSP to Virtual Webcam/Microphone — رابط گرافیکی (GUI)
------------------------------------------------------------
اجرا: python gui.py
یا برای ساخت فایل exe مستقل، به بخش «ساخت فایل EXE» در README.md مراجعه کنید.
"""

import json
import os
import queue
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

import engine

CONFIG_PATH = "config.json"

DEFAULT_CONFIG = {
    "rtsp_url": "",
    "rtsp_transport": "tcp",
    "audio_output_device": None,
    "reconnect_delay_seconds": 3,
    "video_delay_ms": 0,
    "audio_delay_ms": 0,
    "hwaccel": "auto",
    "video_backend": "unitycapture",
    "debug": False,
}


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("RTSP به وبکم مجازی")
        root.geometry("600x590")
        root.resizable(False, False)

        self.stop_event = threading.Event()
        self.threads = []
        self.log_queue = queue.Queue()
        self.running = False

        self.config_data = self.load_config()
        self.audio_devices = []

        self.build_ui()
        self.refresh_devices(initial=True)
        self.populate_from_config()
        self.root.after(150, self.poll_log_queue)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ---------------- UI ----------------
    def build_ui(self):
        pad = {"padx": 10, "pady": 6}
        frm = ttk.Frame(self.root)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="آدرس RTSP دوربین:").grid(row=0, column=0, sticky="w", **pad)
        self.rtsp_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.rtsp_var, width=58).grid(row=0, column=1, columnspan=2, **pad)

        ttk.Label(frm, text="نوع درایور دوربین مجازی:").grid(row=1, column=0, sticky="w", **pad)
        self.video_backend_var = tk.StringVar(value="unitycapture")
        ttk.Combobox(
            frm, textvariable=self.video_backend_var,
            values=["unitycapture", "obs", "auto"], width=15, state="readonly"
        ).grid(row=1, column=1, sticky="w", **pad)

        ttk.Label(frm, text="نوع اتصال (transport):").grid(row=2, column=0, sticky="w", **pad)
        self.transport_var = tk.StringVar(value="tcp")
        ttk.Combobox(
            frm, textvariable=self.transport_var, values=["tcp", "udp"], width=10, state="readonly"
        ).grid(row=2, column=1, sticky="w", **pad)

        ttk.Label(frm, text="دستگاه صوتی خروجی (کابل مجازی):").grid(row=3, column=0, sticky="w", **pad)
        self.audio_var = tk.StringVar()
        self.audio_combo = ttk.Combobox(frm, textvariable=self.audio_var, width=50, state="readonly")
        self.audio_combo.grid(row=3, column=1, columnspan=2, **pad)

        ttk.Button(frm, text="بازخوانی لیست دستگاه‌ها", command=self.refresh_devices).grid(
            row=4, column=1, sticky="w", **pad
        )

        ttk.Label(frm, text="تأخیر عمدی تصویر (میلی‌ثانیه):").grid(row=5, column=0, sticky="w", **pad)
        self.video_delay_var = tk.StringVar(value="0")
        ttk.Entry(frm, textvariable=self.video_delay_var, width=10).grid(row=5, column=1, sticky="w", **pad)

        ttk.Label(frm, text="تأخیر عمدی صدا (میلی‌ثانیه):").grid(row=6, column=0, sticky="w", **pad)
        self.audio_delay_var = tk.StringVar(value="0")
        ttk.Entry(frm, textvariable=self.audio_delay_var, width=10).grid(row=6, column=1, sticky="w", **pad)

        self.debug_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(frm, text="نمایش لاگ کامل ffmpeg (برای عیب‌یابی)", variable=self.debug_var).grid(
            row=7, column=1, sticky="w", **pad
        )

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=8, column=0, columnspan=3, pady=8)
        self.run_btn = ttk.Button(btn_frame, text="▶  اجرا", command=self.start)
        self.run_btn.pack(side="left", padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="■  توقف", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        ttk.Button(btn_frame, text="ذخیره تنظیمات", command=self.save_config).pack(side="left", padx=5)

        self.status_var = tk.StringVar(value="متوقف")
        ttk.Label(frm, textvariable=self.status_var, foreground="#555").grid(
            row=9, column=0, columnspan=3, **pad
        )

        self.log_box = scrolledtext.ScrolledText(frm, width=72, height=15, state="disabled")
        self.log_box.grid(row=10, column=0, columnspan=3, padx=10, pady=6)

    # ---------------- Config ----------------
    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                merged = DEFAULT_CONFIG.copy()
                merged.update(data)
                return merged
            except Exception:
                pass
        return DEFAULT_CONFIG.copy()

    def populate_from_config(self):
        c = self.config_data
        self.rtsp_var.set(c.get("rtsp_url", ""))
        self.transport_var.set(c.get("rtsp_transport", "tcp"))
        self.video_backend_var.set(c.get("video_backend", "unitycapture"))
        self.video_delay_var.set(str(c.get("video_delay_ms", 0)))
        self.audio_delay_var.set(str(c.get("audio_delay_ms", 0)))
        self.debug_var.set(bool(c.get("debug", False)))
        dev = c.get("audio_output_device")
        if dev is not None:
            for i, (idx, name, _api) in enumerate(self.audio_devices):
                if idx == dev or name == dev:
                    self.audio_combo.current(i)
                    break

    def gather_config(self):
        selected_audio = None
        if self.audio_combo.current() >= 0:
            selected_audio = self.audio_devices[self.audio_combo.current()][0]  # device index
        try:
            video_delay = int(self.video_delay_var.get() or 0)
            audio_delay = int(self.audio_delay_var.get() or 0)
        except ValueError:
            messagebox.showerror("خطا", "مقدار تأخیر باید یک عدد صحیح (میلی‌ثانیه) باشد.")
            return None
        return {
            "rtsp_url": self.rtsp_var.get().strip(),
            "rtsp_transport": self.transport_var.get(),
            "audio_output_device": selected_audio,
            "reconnect_delay_seconds": 3,
            "video_delay_ms": video_delay,
            "audio_delay_ms": audio_delay,
            "hwaccel": "auto",
            "video_backend": self.video_backend_var.get(),
            "debug": self.debug_var.get(),
        }

    def save_config(self):
        cfg = self.gather_config()
        if cfg is None:
            return
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        self.append_log("تنظیمات ذخیره شد.")

    def refresh_devices(self, initial: bool = False):
        self.audio_devices = engine.list_output_audio_devices()
        self.audio_combo["values"] = [f"{idx}: {name} ({api})" for idx, name, api in self.audio_devices]
        if not initial:
            self.append_log("لیست دستگاه‌های صوتی بازخوانی شد.")

    # ---------------- Run/Stop ----------------
    def start(self):
        if self.running:
            return
        cfg = self.gather_config()
        if cfg is None:
            return
        if not cfg["rtsp_url"]:
            messagebox.showerror("خطا", "آدرس RTSP را وارد کنید.")
            return
        if cfg["audio_output_device"] is None:
            if not messagebox.askyesno(
                "هشدار", "دستگاه صوتی انتخاب نشده؛ فقط تصویر ارسال می‌شود. ادامه می‌دهید؟"
            ):
                return

        self.save_config()
        self.stop_event = threading.Event()
        self.running = True
        self.run_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_var.set("در حال اتصال به دوربین...")

        def gui_log(msg):
            self.log_queue.put(msg)

        def worker():
            try:
                self.threads = engine.run_pipeline(cfg, self.stop_event, gui_log)
                self.log_queue.put("__STATUS__در حال اجرا ✅")
            except Exception as e:
                self.log_queue.put(f"اتصال به دوربین ناموفق بود: {e}")
                self.log_queue.put("__STATUS__متوقف (خطا)")
                self.log_queue.put("__RESET_BUTTONS__")
                self.running = False

        threading.Thread(target=worker, daemon=True).start()

    def stop(self):
        if not self.running:
            return
        self.stop_event.set()
        self.running = False
        self.run_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_var.set("متوقف")
        self.append_log("در حال توقف...")

    def on_close(self):
        self.stop_event.set()
        self.root.after(300, self.root.destroy)

    # ---------------- Logging ----------------
    def append_log(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def poll_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                if msg == "__RESET_BUTTONS__":
                    self.run_btn.config(state="normal")
                    self.stop_btn.config(state="disabled")
                elif msg.startswith("__STATUS__"):
                    self.status_var.set(msg.replace("__STATUS__", ""))
                else:
                    self.append_log(msg)
        except queue.Empty:
            pass
        self.root.after(150, self.poll_log_queue)


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# RTSP Virtual Webcam

تبدیل دوربین IP (با پروتکل RTSP) به یک وبکم و میکروفون مجازی که هر برنامه‌ای
می‌تونه ازش استفاده کنه — گوگل میت، زوم، تیمز، دیسکورد، یا هر برنامه‌ی دیگه‌ای
که از دوربین/میکروفون استاندارد ویندوز می‌خونه.

[![Latest Release](https://img.shields.io/github/v/release/Rahideh/rtsp-virtual-webcam)](https://github.com/Rahideh/rtsp-virtual-webcam/releases)
[![GitHub Stars](https://img.shields.io/github/stars/Rahideh/rtsp-virtual-webcam)](https://github.com/Rahideh/rtsp-virtual-webcam/stargazers)
[![License](https://img.shields.io/github/license/Rahideh/rtsp-virtual-webcam)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue)](https://github.com/Rahideh/rtsp-virtual-webcam)

نسخه‌ی انگلیسی (اصلی): [../README.md](../README.md)

## دمو

![RTSP Virtual Webcam Demo](../images/demo.gif)

## چرا این پروژه ساخته شد

اکثر نرم‌افزارهای تجاری «دوربین IP به وبکم» یا پولی‌ان، یا با نرم‌افزارهای
اضافی که نیازی بهشون نیست همراه میان، یا برای کاری که در اصل یه پایپ‌لاین
کوچیکه (decode کردن استریم RTSP و تحویلش به یه دستگاه مجازی) خیلی سنگین‌ان.
این پروژه همون پایپ‌لاین کوچیکه، به‌همراه یه رابط گرافیکی، یه استراتژی
reconnect، و یه نصب‌کننده — و نه چیز بیشتر.

## امکانات

- ارسال تصویر RTSP به یک وبکم مجازی از طریق UnityCapture (بدون نیاز به OBS
  Studio) یا در صورت تمایل، از طریق درایور دوربین مجازی OBS Studio.
- ارسال صدای RTSP به یک میکروفون مجازی از طریق VB-Audio VB-CABLE.
- Decode کردن ویدیو با شتاب‌دهی سخت‌افزاری (`hwaccel`) برای مصرف پایین CPU.
- اتصال مجدد خودکار در صورت قطع شدن اتصال دوربین.
- تنظیم تأخیر عمدی صدا/تصویر برای اصلاح عدم هم‌گامی بین دو اتصال مستقل RTSP.
- یک رابط گرافیکی (Tkinter، بدون وابستگی اضافه) و یک نسخه‌ی خط فرمان، هر دو
  با یک هسته‌ی مشترک.
- یک نصب‌کننده‌ی ویندوزی (Inno Setup) که درایور دوربین مجازی رو خودکار ثبت
  می‌کنه و کاربر رو برای تنها مرحله‌ی دستی باقی‌مونده (نصب VB-CABLE، که به
  دلایل قانونی نمی‌شه bundle کرد — به
  [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) مراجعه کنید) راهنمایی
  می‌کنه.

  ## پیش‌نیازها

### استفاده از فایل نصب ویندوز

استفاده از فایل نصب، روش پیشنهادی برای اجرای RTSP Virtual Webcam است. برای
استفاده از نسخه نصبی فقط به موارد زیر نیاز دارید:

- ویندوز 10 یا 11 (۶۴ بیتی)
- یک دوربین تحت شبکه که استریم RTSP ارائه دهد
- [VB-Audio VB-CABLE](https://vb-audio.com/Cable/) برای استفاده از میکروفون مجازی

نصب‌کننده، راه‌اندازی درایور وب‌کم مجازی را به‌صورت خودکار انجام می‌دهد.
FFmpeg و سایر اجزای موردنیاز برنامه نیز در نسخه بسته‌بندی‌شده قرار دارند.

### اجرای برنامه از سورس

اگر می‌خواهید RTSP Virtual Webcam را مستقیماً از سورس اجرا کنید، به موارد زیر
نیاز خواهید داشت:

- ویندوز 10 یا 11 (۶۴ بیتی)
- Python نسخه 3.10 یا بالاتر
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) (`ffmpeg.exe` و `ffprobe.exe`)
- [UnityCapture](https://github.com/schellingb/UnityCapture) (پیش‌فرض) یا
  [OBS Studio](https://obsproject.com/) به‌عنوان Backend وب‌کم مجازی
- [VB-Audio VB-CABLE](https://vb-audio.com/Cable/) برای استفاده از میکروفون مجازی
- یک دوربین تحت شبکه که استریم RTSP ارائه دهد (ویدئوی H.264 توصیه می‌شود)

## نحوه‌ی کارکرد

دوربین از طریق دو اتصال مستقل RTSP خونده می‌شه، چون تصویر و صدا هرکدوم توسط
یک فرایند جدای FFmpeg مصرف می‌شن:

```
دوربین RTSP --(تصویر، FFmpeg)--> فریم خام --> وبکم مجازی (UnityCapture / OBS)
دوربین RTSP --(صدا، FFmpeg)--> PCM خام   --> میکروفون مجازی (VB-CABLE)
```

هر دو فرایند توسط یک هسته‌ی کوچیک پایتون (`engine.py`) مدیریت می‌شن که در
صورت قطعی reconnect می‌کنه و در صورت نیاز یکی از دو مسیر رو با دیگری هم‌گام
می‌کنه. برای پیاده‌سازی به [`engine.py`](../engine.py) مراجعه کنید.

## نصب

### روش الف: نصب‌کننده‌ی ویندوزی (پیشنهادی)

آخرین نسخه‌ی `RTSP-Virtual-Webcam-Setup.exe` رو از صفحه‌ی
[Releases](../../../releases) دانلود و اجرا کنید. نصب‌کننده خودکار درایور
UnityCapture رو ثبت می‌کنه و برای نصب VB-CABLE (به دلایل قانونی، تنها مرحله‌ی
دستی باقی‌مونده — به
[THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) مراجعه کنید) راهنماییتون
می‌کنه.

### روش ب: اجرا از سورس

```
git clone https://github.com/Rahideh/rtsp-virtual-webcam.git
cd rtsp-virtual-webcam
pip install -r requirements.txt
```

FFmpeg، UnityCapture (یا OBS Studio)، و VB-CABLE رو دستی نصب کنید — به
توضیحات گام‌به‌گام پایین‌تر همین فایل مراجعه کنید.

#### نصب FFmpeg

از [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/) نسخه‌ی
"release essentials" رو دانلود کنید و یا پوشه‌ی `bin`ش رو به PATH اضافه کنید،
یا `ffmpeg.exe` و `ffprobe.exe` رو کنار فایل‌های `.py` این پروژه بذارید.

#### نصب UnityCapture (پیش‌فرض دوربین مجازی)

۱. دو فایل `UnityCaptureFilter32.dll` و `UnityCaptureFilter64.dll` رو از
   [github.com/schellingb/UnityCapture/tree/master/Install](https://github.com/schellingb/UnityCapture/tree/master/Install)
   دانلود کنید.
۲. یک Command Prompt با دسترسی **Administrator** باز کنید و هر دو رو ثبت کنید:
   ```
   regsvr32 "C:\path\to\UnityCaptureFilter64.dll"
   regsvr32 "C:\path\to\UnityCaptureFilter32.dll"
   ```
۳. همین — نیازی به نصب یا اجرای OBS Studio نیست.

اگه ترجیح می‌دید از OBS Studio استفاده کنید: نصبش کنید، یک‌بار بازش کنید،
**Start Virtual Camera** و بعد **Stop Virtual Camera** رو بزنید (این درایور
رو ثبت می‌کنه)، و در `config.json` مقدار `"video_backend"` رو `"obs"` بذارید.

#### نصب VB-Audio VB-CABLE

از [vb-audio.com/Cable](https://vb-audio.com/Cable/) دانلود و نصب کنید، بعد
ری‌استارت کنید. این کار دو دستگاه صوتی می‌سازه: `CABLE Input` (پخش) و
`CABLE Output` (ضبط).

## شروع سریع

1. آخرین نسخه برنامه را از صفحه [Releases](../../releases) دانلود کنید.
2. فایل نصب را اجرا کرده و **RTSP Virtual Webcam** را نصب کنید.
3. در صورت درخواست، **VB-Audio VB-CABLE** را نصب کنید.
4. آدرس RTSP دوربین خود را وارد کنید.
5. دستگاه صوتی موردنظر را انتخاب کرده و استریم را اجرا کنید.
6. در Google Meet، Zoom، Microsoft Teams، Discord یا OBS، گزینه **RTSP Virtual Webcam** را به‌عنوان دوربین انتخاب کنید.
7. برای استفاده از صدای دوربین، دستگاه **CABLE Output** را به‌عنوان میکروفون انتخاب کنید.

## تنظیمات

فایل `config.example.json` رو کپی کنید به‌اسم `config.json` و ویرایشش کنید:

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

**`config.json` شامل یوزرنیم و پسورد دوربین شماست. به‌طور پیش‌فرض در
`.gitignore` قرار داره — آن را از `.gitignore` حذف نکنید، و هرگز محتوایش را
در یک issue یا فروم عمومی قرار ندید.**

| فیلد | توضیح |
|---|---|
| `rtsp_url` | آدرس کامل RTSP دوربین، شامل یوزر/پسورد در صورت نیاز. |
| `rtsp_transport` | `tcp` (پیشنهادی، پایدارتر) یا `udp`. |
| `audio_output_device` | نام یا شماره‌ی دستگاه صوتی مجازی (با `list_audio_devices.py` یا منوی کشویی GUI پیداش کنید). |
| `reconnect_delay_seconds` | زمان انتظار قبل از تلاش مجدد بعد از قطعی. |
| `video_delay_ms` / `audio_delay_ms` | تأخیر عمدی برای اصلاح عدم هم‌گامی صدا/تصویر. معمولاً فقط یکی از این دو مقدار غیرصفره. به بخش عیب‌یابی مراجعه کنید. |
| `hwaccel` | `auto` (پیشنهادی)، یک روش خاص FFmpeg (مثل `d3d11va`)، یا `none` برای اجبار به decode نرم‌افزاری. |
| `video_backend` | `unitycapture` (پیش‌فرض، سبک) یا `obs`. |
| `debug` | برای دیدن خروجی کامل لاگ FFmpeg (عیب‌یابی) روی `true` بذارید. |

## استفاده

### رابط گرافیکی

```
python gui.py
```

آدرس RTSP رو وارد کنید، دستگاه صوتی رو از منوی کشویی انتخاب کنید، و روی اجرا
کلیک کنید. تنظیمات خودکار در `config.json` ذخیره می‌شن.

### خط فرمان

```
python main.py
```

`config.json` رو از پوشه‌ی جاری می‌خونه (یا مسیری که با `--config` دادید).

## عیب‌یابی

**صدا و تصویر sync نیستن.** این طبیعیه: چون تصویر و صدا هرکدوم از یک اتصال
RTSP جدا با تأخیر پایپ‌لاین کمی متفاوت خونده می‌شن و هیچ ساعت مشترکی بینشون
نیست. مقدار تأخیر رو اندازه بگیرید (مثلاً دست بزنید و ببینید صدا چقدر بعد از
تصویر میاد) و همون مقدار رو (به میلی‌ثانیه) در `video_delay_ms` (یا
`audio_delay_ms` اگه صدا جلوتره) بذارید. این مقدار برای یک دوربین/شبکه‌ی
مشخص معمولاً ثابته، پس فقط یک‌بار لازمه تنظیمش کنید.

**مصرف بالای CPU یا RAM.** مطمئن بشید `hwaccel` روی `auto` تنظیم شده — این
کار decode ویدیوی H.264 رو به GPU می‌سپاره. اگه دوربینتون یک substream با
کیفیت پایین‌تر داره (معمولاً `stream2` یا مشابه)، از اون به‌جای استریم اصلی
استفاده کنید؛ معمولاً برای تماس تصویری کاملاً کافیه و خیلی سبک‌تره.

**موقع اجرای فایل exe بسته‌بندی‌شده، یه پنجره‌ی کنسول برای FFmpeg باز می‌شه.**
این نباید اتفاق بیفته — فراخوانی‌های subprocess از `CREATE_NO_WINDOW` استفاده
می‌کنن. اگه این رو دیدید، لطفاً با نسخه‌ی ویندوزتون یک issue باز کنید.

**رنگ‌های تصویر برعکسه (آبی/قرمز جابه‌جا).** مقدار `pix_fmt bgr24` رو به
`rgb24` و `PixelFormat.BGR` رو به `PixelFormat.RGB` در توابع
`start_ffmpeg_video()` / `video_worker()` داخل `engine.py` تغییر بدید.

**دوربین فقط یک نشست RTSP همزمان قبول می‌کنه.** بعضی دوربین‌های ارزون این
محدودیت رو دارن. چون این پروژه دو اتصال جدا باز می‌کنه (یکی تصویر، یکی صدا)،
در این حالت نیاز به یک فرایند واحد FFmpeg دارید که هر دو استریم رو به دو پایپ
خروجی جدا demux کنه. اگه به این مشکل خوردید، یک issue باز کنید — قابل‌حله ولی
تغییر ساده‌ای نیست.

## ساخت نصب‌کننده

برای فرآیند کامل و گام‌به‌گام ساخت `RTSP-Virtual-Webcam-Setup.exe` از سورس،
به [installer/PACKAGING.md](../installer/PACKAGING.md) (انگلیسی) یا
[PACKAGING.fa.md](PACKAGING.fa.md) (فارسی) مراجعه کنید.

## قدردانی

این پروژه به FFmpeg، UnityCapture، pyvirtualcam، sounddevice، و VB-Audio
VB-CABLE وابسته‌ست. برای جزئیات لایسنس هرکدوم به
[THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) مراجعه کنید.

## مشارکت

به [CONTRIBUTING.md](../CONTRIBUTING.md) مراجعه کنید.

## لایسنس

MIT. به [LICENSE](../LICENSE) مراجعه کنید.

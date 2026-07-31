# راهنمای بسته‌بندی — ساخت نصب‌کننده‌ی ویندوز

این راهنما توضیح می‌ده چطور `RTSP-Virtual-Webcam-Setup.exe` رو بسازید؛ یک
نصب‌کننده‌ی استاندارد ویندوزی که کاربر نهایی فقط دابل‌کلیکش می‌کنه، بدون نیاز
به پایتون، خط فرمان، یا نصب دستی OBS Studio.

نسخه‌ی انگلیسی (اصلی): [../installer/PACKAGING.md](../installer/PACKAGING.md)

## ۱. نکته‌ی مهم درباره‌ی لایسنس VB-Audio VB-CABLE (اول این رو بخونید)

طبق شرایط خودِ VB-Audio
([vb-audio.com/Cable](https://vb-audio.com/Cable/)،
[shop.vb-audio.com](https://shop.vb-audio.com/en/win-apps/11-vb-cable.html))،
بسته‌بندی یا ادغام فایل نصب VB-CABLE داخل یک نرم‌افزار دیگه نیاز به تماس
مستقیم با VB-Audio برای گرفتن یک توافق توزیع داره. دانلود مستقیم از سایتشون
برای استفاده‌ی شخصی رایگانه (donationware)، ولی قرار دادنش داخل نصب‌کننده‌ی
خودمون و پخش عمومی روی گیت‌هاب چیز دیگه‌ایه.

به همین دلیل، `setup.iss` فایل نصب VB-CABLE رو bundle نمی‌کنه. در عوض:

- نصب‌کننده یک چک‌باکس اجباری داره که کاربر باید تیک بزنه تا ادامه بده.
- دو دکمه در اختیار کاربره: یکی صفحه‌ی دانلود رسمی VB-CABLE رو در مرورگر باز
  می‌کنه؛ دیگری اسکریپت `install-vbcable.ps1` رو اجرا می‌کنه که مستقیم از
  دامنه‌ی خودِ VB-Audio دانلود و نصبش می‌کنه.

**اگه می‌خواید کاملاً bundle و silent باشه:** از طریق
[فرم تماس](https://vb-audio.com/Services/contact.htm) VB-Audio باهاشون
صحبت کنید و درخواست «bundle license» بدید. اگه موافقت کردن، `setup.iss` رو
می‌شه طوری تغییر داد که فایل نصبشون رو مستقیم شامل بشه و کاملاً خودکار
(`-i -h`) نصبش کنه — یک issue باز کنید یا این نسخه رو درخواست بدید.

## ۲. فایل‌هایی که قبل از کامپایل باید داخل `installer/files` باشن

| فایل | از کجا بگیرید |
|---|---|
| `RTSP-Virtual-Webcam.exe` | با PyInstaller ساخته می‌شه — بخش ۳ پایین‌تر. |
| `ffmpeg.exe`، `ffprobe.exe` | نسخه‌ی "release essentials" رو از [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/) دانلود کنید و این دو فایل رو از پوشه‌ی `bin` بردارید. |
| `UnityCaptureFilter32.dll`، `UnityCaptureFilter64.dll` | مستقیم از [github.com/schellingb/UnityCapture/tree/master/Install](https://github.com/schellingb/UnityCapture/tree/master/Install) دانلود کنید (MIT license، از قبل کامپایل‌شده، نیازی به build نیست). |
| `install-vbcable.ps1` | از قبل داخل `installer/files/` هست — کاری لازم نیست. |

**یک قدم اضافه‌ی ضروری:** فایل `installer/setup.iss` رو باز کنید و در خط
`#define MyAppGitHubURL`، عبارت `REPO-NAME-HERE` رو با آدرس واقعی
ریپازیتوری گیت‌هابتون جایگزین کنید. این آدرس در صفحه‌ی خوش‌آمدگویی نصب‌کننده
نمایش داده می‌شه.

## ۳. ساخت `RTSP-Virtual-Webcam.exe` با PyInstaller

```
cd rtsp_to_webcam
pip install pyinstaller
python -m PyInstaller --onefile --noconsole --name RTSP-Virtual-Webcam gui.py
```

فایل خروجی `dist\RTSP-Virtual-Webcam.exe` رو داخل `installer\files\` کپی کنید.

## ۴. نصب Inno Setup و کامپایل نصب‌کننده

۱. Inno Setup رو (رایگان) از [jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php) نصب کنید.
۲. فایل `installer\setup.iss` رو با Inno Setup Compiler باز کنید.
۳. مطمئن بشید همه‌ی فایل‌های بخش ۲ داخل `installer\files\` هستن.
۴. از منو Build → Compile (یا کلید F9) بزنید.
۵. نصب‌کننده‌ی نهایی در `installer\Output\RTSP-Virtual-Webcam-Setup.exe`
   ساخته می‌شه.

همین فایل رو مستقیم به یک GitHub Release آپلود کنید — داخل خودِ ریپازیتوری
کامیتش نکنید (به `.gitignore` مراجعه کنید).

## ۵. تجربه‌ی کاربر نهایی

۱. `RTSP-Virtual-Webcam-Setup.exe` رو اجرا می‌کنه (یک درخواست Administrator).
۲. یک صفحه‌ی خوش‌آمدگویی می‌بینه با توضیح کوتاه پروژه، نام نویسنده، و لینک‌های
   وب‌سایت و گیت‌هاب.
۳. به صفحه‌ی «کابل صوتی مجازی» می‌رسه؛ دو دکمه (دانلود دستی / نصب خودکار با
   PowerShell) و یک چک‌باکس اجباری که تا تیک نخوره جلو نمی‌ره.
۴. بقیه‌ی نصب (کپی فایل‌ها، ثبت درایور UnityCapture) خودکار انجام می‌شه.
۵. در پایان، برنامه (نسخه‌ی بسته‌بندی‌شده‌ی `gui.py`) اجرا می‌شه.

## ۶. تست قبل از انتشار

روی یک ویندوز تمیز یا یک Snapshot ماشین مجازی (بدون OBS/UnityCapture/VB-CABLE
از قبل نصب‌شده) تست کنید و مطمئن بشید:

- نصب بدون خطا کامل می‌شه.
- درایور UnityCapture واقعاً ثبت شده (هر برنامه‌ای باید دوربینی به اسم
  "Unity Video Capture" ببینه).
- بعد از نصب دستی VB-CABLE و ری‌استارت، صدا هم درست کار می‌کنه.
- Uninstall از Control Panel، درایور UnityCapture رو هم درست پاک می‌کنه.

این نصب‌کننده توسط نویسنده‌ی این راهنما روی یک ویندوز واقعی کامپایل یا اجرا
نشده (در یک sandbox لینوکسی توسعه داده شده) — اگه هنگام کامپایل یا اجرا به
خطایی خوردید، لطفاً با متن دقیق خطا یک issue باز کنید.

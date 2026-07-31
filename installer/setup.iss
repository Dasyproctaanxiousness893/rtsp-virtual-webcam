; ============================================================================
; RTSP Virtual Webcam - Inno Setup Installer Script
; ============================================================================
; قبل از کامپایل کردن این اسکریپت:
;   1. Inno Setup 6.1 یا جدیدتر رو نصب کنید: https://jrsoftware.org/isdl.php
;   2. فایل‌های لازم رو داخل پوشه‌ی installer\files بذارید (به PACKAGING.md
;      مراجعه کنید که دقیقاً هرکدوم رو از کجا دانلود کنید):
;        - RTSP-Virtual-Webcam.exe   (خروجی PyInstaller از gui.py)
;        - ffmpeg.exe
;        - ffprobe.exe
;        - UnityCaptureFilter32.dll
;        - UnityCaptureFilter64.dll
;        - install-vbcable.ps1        (از قبل توی این پوشه هست، دست نزنید)
;   3. مقدار MyAppGitHubURL رو پایین‌تر با آدرس واقعی ریپازیتوری گیت‌هابتون
;      جایگزین کنید.
;   4. این فایل (setup.iss) رو با Inno Setup Compiler باز کنید و Build/Compile
;      بزنید. خروجی نهایی توی installer\Output\RTSP-Virtual-Webcam-Setup.exe
;      ساخته می‌شه.
; ============================================================================

#define MyAppName "RTSP Virtual Webcam"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Rahideh"
#define MyAppURL "https://trustit.ir"
#define MyAppGitHubURL "https://github.com/Rahideh/rtsp-virtual-webcam"
#define MyAppExeName "RTSP-Virtual-Webcam.exe"

[Setup]
AppId={{B6E1B6B0-2F1E-4C2A-9B7E-RTSPVIRTUALCAM}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppGitHubURL}
AppUpdatesURL={#MyAppGitHubURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
; صفحه‌ی خوش‌آمدگویی (Welcome) رو فعال می‌کنیم تا قبل از انتخاب مسیر نصب دیده بشه
DisableWelcomePage=no
OutputDir=Output
OutputBaseFilename=RTSP-Virtual-Webcam-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; نصب درایورها (UnityCapture COM registration) نیاز به دسترسی ادمین داره
PrivilegesRequired=admin
; پشتیبانی از ویندوزهای x64 و Arm64 (سازگار با x64)
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

; متن صفحه‌ی خوش‌آمدگویی (Welcome) رو با معرفی نویسنده و لینک‌ها سفارشی می‌کنیم
[Messages]
WelcomeLabel1=خوش آمدید {#MyAppName} به نصب
WelcomeLabel2=-رضا رهیده توسعه داده شده است. Rahideh این نرم افزار توسط%n%nآدرس وبسایت: {#MyAppURL}%n%n:سورس‌کد کامل و مستندات در گیت‌هاب {#MyAppGitHubURL}%n%nکلیک کنید Next برای ادامه نصب، روی

[Tasks]
Name: "desktopicon"; Description: "ساخت میان‌بر روی دسکتاپ"; GroupDescription: "میانبر نرم افزار:"

[Files]
Source: "files\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "files\ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "files\ffprobe.exe"; DestDir: "{app}"; Flags: ignoreversion
; دو DLL زیر مربوط به UnityCapture (پروژه‌ی متن‌باز MIT-license) هستن که
; جایگزین OBS Studio برای دوربین مجازی می‌شن. با فلگ regserver خودکار در
; حین نصب ثبت (regsvr32) و در حین حذف نصب، خودکار unregister می‌شن.
Source: "files\UnityCaptureFilter32.dll"; DestDir: "{app}"; Flags: ignoreversion regserver 32bit
Source: "files\UnityCaptureFilter64.dll"; DestDir: "{app}"; Flags: ignoreversion regserver 64bit
; اسکریپت نصب خودکار VB-CABLE؛ فقط موقع نیاز از {tmp} استخراج می‌شه، داخل
; پوشه‌ی نصب دائمی کپی نمی‌شه (Flags: dontcopy)
Source: "files\install-vbcable.ps1"; DestDir: "{tmp}"; Flags: dontcopy

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "اجرای {#MyAppName}"; Flags: nowait postinstall skipifsilent

; ============================================================================
; [Code]: صفحه‌ی سفارشی با چک‌باکس اجباری برای VB-Audio Virtual Cable
; ============================================================================
; چون VB-Cable برای بسته‌بندی/توزیع مستقیم نیاز به توافق جدا با VB-Audio داره
; (به PACKAGING.md مراجعه کنید)، فایل نصبش رو داخل این installer قرار نمی‌دیم؛
; در عوض این صفحه دو گزینه به کاربر می‌ده: باز کردن صفحه‌ی دانلود رسمی در مرورگر،
; یا دانلود و نصب خودکار با یک اسکریپت PowerShell که مستقیم از سایت رسمی
; VB-Audio دانلود می‌کنه. در هر دو حالت، چک‌باکس باید تیک بخوره تا نصب ادامه پیدا کنه.
[Code]
var
  VBCablePage: TWizardPage;
  VBCableInfoLabel: TNewStaticText;
  VBCableBrowserButton: TNewButton;
  VBCablePSButton: TNewButton;
  VBCableCheckBox: TNewCheckBox;

procedure VBCableBrowserButtonClick(Sender: TObject);
var
  ResultCode: Integer;
begin
  ShellExec('open', 'https://vb-audio.com/Cable/', '', '', SW_SHOWNORMAL, ewNoWait, ResultCode);
end;

procedure VBCablePSButtonClick(Sender: TObject);
var
  ResultCode: Integer;
  ScriptPath: string;
begin
  ExtractTemporaryFile('install-vbcable.ps1');
  ScriptPath := ExpandConstant('{tmp}\install-vbcable.ps1');
  Exec('powershell.exe',
    '-NoExit -ExecutionPolicy Bypass -File "' + ScriptPath + '"',
    '', SW_SHOW, ewNoWait, ResultCode);
end;

procedure InitializeWizard;
begin
  VBCablePage := CreateCustomPage(
    wpSelectTasks,
    'نصب کابل صوتی مجازی (ضروری)',
    'برای اینکه صدای دوربین به‌عنوان میکروفون در برنامه‌هایی مثل گوگل میت شناخته بشه، ' +
    'نیاز به یک درایور صوتی مجازی دارید.'
  );

  VBCableInfoLabel := TNewStaticText.Create(VBCablePage);
  VBCableInfoLabel.Parent := VBCablePage.Surface;
  VBCableInfoLabel.Left := 0;
  VBCableInfoLabel.Top := 0;
  VBCableInfoLabel.Width := VBCablePage.SurfaceWidth;
  VBCableInfoLabel.AutoSize := False;
  VBCableInfoLabel.WordWrap := True;
  VBCableInfoLabel.Height := 60;
  VBCableInfoLabel.Caption :=
    'انتخاب کنید VB-Audio VB-CABLE یکی از دو روش زیر رو برای نصب ' +
    'و بعد از نصب کامپیوترتون رو ری استارت کنید که میکروفون مجازی به عنوان صدای دوربین کار کنه';

  VBCableBrowserButton := TNewButton.Create(VBCablePage);
  VBCableBrowserButton.Parent := VBCablePage.Surface;
  VBCableBrowserButton.Left := 0;
  VBCableBrowserButton.Top := VBCableInfoLabel.Top + VBCableInfoLabel.Height + 12;
  VBCableBrowserButton.Width := 190;
  VBCableBrowserButton.Height := 28;
  VBCableBrowserButton.Caption := 'دانلود دستی از مرورگر';
  VBCableBrowserButton.OnClick := @VBCableBrowserButtonClick;

  VBCablePSButton := TNewButton.Create(VBCablePage);
  VBCablePSButton.Parent := VBCablePage.Surface;
  VBCablePSButton.Left := VBCableBrowserButton.Left + VBCableBrowserButton.Width + 12;
  VBCablePSButton.Top := VBCableBrowserButton.Top;
  VBCablePSButton.Width := 190;
  VBCablePSButton.Height := 28;
  VBCablePSButton.Caption := 'نصب خودکار با PowerShell';
  VBCablePSButton.OnClick := @VBCablePSButtonClick;

  VBCableCheckBox := TNewCheckBox.Create(VBCablePage);
  VBCableCheckBox.Parent := VBCablePage.Surface;
  VBCableCheckBox.Left := 0;
  VBCableCheckBox.Top := VBCableBrowserButton.Top + VBCableBrowserButton.Height + 16;
  VBCableCheckBox.Width := VBCablePage.SurfaceWidth;
  VBCableCheckBox.Caption :=
    'ضروریست اوکی؟ VB-Audio VB-CABLE اگر دوربین شما میکروفون دارد و میخواهید از آن استفاده کنید';
  
  VBCableCheckBox.Checked := False;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  if (CurPageID = VBCablePage.ID) and (not VBCableCheckBox.Checked) then
  begin
    MsgBox(
      'برای ادامه، باید تیک این گزینه را بزنید. VB-Audio VB-CABLE برای عملکرد ' +
      'صدای برنامه ضروری است.',
      mbError, MB_OK
    );
    Result := False;
  end;
end;

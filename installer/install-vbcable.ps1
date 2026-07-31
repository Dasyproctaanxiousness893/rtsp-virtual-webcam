# نصب خودکار VB-Audio VB-CABLE
# این اسکریپت مستقیماً از دامنه‌ی رسمی VB-Audio دانلود می‌کنه، نه از یک نسخه‌ی
# ذخیره‌شده در ریپازیتوری ما — چون توزیع/بسته‌بندی مستقیم فایل نصب VB-CABLE
# نیاز به توافق جدا با VB-Audio داره (به installer/PACKAGING.md مراجعه کنید).

$ErrorActionPreference = "Stop"
$url = "https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack45.zip"
$zipPath = Join-Path $env:TEMP "VBCABLE_Driver_Pack45.zip"
$extractPath = Join-Path $env:TEMP "VBCABLE_Driver_Pack45"

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host " نصب خودکار VB-Audio VB-CABLE" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "در حال دانلود از download.vb-audio.com ..." -ForegroundColor Yellow

try {
    Invoke-WebRequest -Uri $url -OutFile $zipPath -UseBasicParsing
}
catch {
    Write-Host ""
    Write-Host "دانلود خودکار ناموفق بود (شاید آدرس فایل تغییر کرده یا اینترنت قطعه)." -ForegroundColor Red
    Write-Host "در حال باز کردن صفحه‌ی دانلود رسمی در مرورگر تا خودتون دستی نصب کنید..." -ForegroundColor Yellow
    Start-Process "https://vb-audio.com/Cable/"
    Read-Host "برای بستن این پنجره، کلید Enter را بزنید"
    exit 1
}

Write-Host "دانلود کامل شد. در حال استخراج فایل‌ها..." -ForegroundColor Yellow
Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force

$setupExe = Get-ChildItem -Path $extractPath -Filter "VBCABLE_Setup_x64.exe" -Recurse | Select-Object -First 1
if (-not $setupExe) {
    $setupExe = Get-ChildItem -Path $extractPath -Filter "VBCABLE_Setup.exe" -Recurse | Select-Object -First 1
}

if ($setupExe) {
    Write-Host "در حال اجرای نصب‌کننده (ممکنه یک پنجره‌ی تأیید دسترسی ادمین یا امنیت ویندوز باز بشه)..." -ForegroundColor Yellow
    Start-Process -FilePath $setupExe.FullName -ArgumentList "-i", "-h" -Verb RunAs -Wait
    Write-Host ""
    Write-Host "نصب VB-CABLE انجام شد." -ForegroundColor Green
    Write-Host "مهم: برای فعال شدن کامل درایور، حتماً کامپیوتر را ری‌استارت کنید." -ForegroundColor Yellow
}
else {
    Write-Host ""
    Write-Host "فایل نصب‌کننده در بسته‌ی دانلودشده پیدا نشد." -ForegroundColor Red
    Write-Host "لطفاً به‌صورت دستی از https://vb-audio.com/Cable/ نصب کنید." -ForegroundColor Red
}

Write-Host ""
Read-Host "برای بستن این پنجره، کلید Enter را بزنید"

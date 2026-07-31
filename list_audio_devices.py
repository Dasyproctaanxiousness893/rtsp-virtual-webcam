"""
این اسکریپت رو اجرا کنید تا لیست دستگاه‌های صوتی سیستم رو ببینید.
دنبال چیزی شبیه "CABLE Input (VB-Audio Virtual Cable)" بگردید و
نام دقیقش رو (یا شماره‌ی index رو) در config.json به‌عنوان audio_output_device قرار بدید.
"""
import sounddevice as sd

print(sd.query_devices())

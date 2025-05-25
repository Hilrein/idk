#!/usr/bin/env python3
"""
Скрипт для проверки наличия и версии FFmpeg в системе
"""

import subprocess
import shutil
import sys
import os

def check_ffmpeg():
    """
    Проверяет установку FFmpeg и выводит информацию о версии
    
    Returns:
        bool: True, если FFmpeg установлен
    """
    print("Проверка установки FFmpeg...")
    
    # Проверяем наличие исполняемого файла FFmpeg в PATH
    ffmpeg_path = shutil.which("ffmpeg")
    
    if ffmpeg_path is None:
        print("\n❌ FFmpeg не найден в системном PATH!")
        print("\nРекомендации по установке FFmpeg:")
        
        if os.name == 'nt':  # Windows
            print("""
1. Скачайте FFmpeg с официального сайта: https://ffmpeg.org/download.html
   - Рекомендуется версия "FFmpeg Builds" от gyan.dev: https://www.gyan.dev/ffmpeg/builds/
   - Скачайте файл "ffmpeg-release-full-shared.7z"

2. Распакуйте архив в удобную директорию, например C:\\FFmpeg

3. Добавьте путь к папке bin в переменную PATH:
   - Нажмите Win + X, выберите "Система"
   - Выберите "Дополнительные параметры системы" → "Переменные среды"
   - В разделе "Переменные среды пользователя" выберите PATH и нажмите "Изменить"
   - Добавьте путь к папке bin FFmpeg (например, C:\\FFmpeg\\bin)
   - Нажмите OK для сохранения изменений

4. Перезапустите командную строку и снова запустите этот скрипт для проверки
            """)
        
        return False
    else:
        print(f"\n✅ FFmpeg найден: {ffmpeg_path}")
        
        try:
            # Получаем версию FFmpeg
            result = subprocess.run(['ffmpeg', '-version'], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    encoding='utf-8')
            
            if result.returncode == 0:
                version_info = result.stdout.split('\n')[0]
                print(f"\nИнформация о версии FFmpeg:")
                print(f"{version_info}")
                print("\nFFmpeg успешно установлен и готов к использованию!")
            else:
                print("\n⚠️ FFmpeg найден, но возникла ошибка при получении версии.")
                print(f"Ошибка: {result.stderr}")
        except Exception as e:
            print(f"\n⚠️ Ошибка при проверке версии FFmpeg: {e}")
            return False
            
        return True

if __name__ == "__main__":
    success = check_ffmpeg()
    
    if success:
        print("\nВсе готово для работы с RTMP → RTSP конвертером!")
        sys.exit(0)
    else:
        print("\nУстановите FFmpeg перед использованием RTMP → RTSP конвертера.")
        sys.exit(1) 
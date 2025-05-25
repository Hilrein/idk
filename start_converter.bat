@echo off
echo ======================================
echo RTMP в RTSP Конвертер - Скрипт запуска
echo ======================================

REM Проверка наличия FFmpeg
echo Проверка зависимостей...
python check_ffmpeg.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ошибка: FFmpeg не установлен или не найден в PATH.
    echo Установите FFmpeg согласно инструкциям выше и повторите попытку.
    echo.
    pause
    exit /b 1
)

echo.
echo ======================================
echo       Запуск RTMP в RTSP конвертера
echo ======================================
echo.

:URL_INPUT
set /p RTMP_URL="Введите URL-адрес RTMP потока (например, rtmp://example.com/live/stream): "

if "%RTMP_URL%"=="" (
    echo Ошибка: URL не может быть пустым. Пожалуйста, введите корректный URL.
    goto URL_INPUT
)

set /p RTSP_PORT="Введите порт для RTSP-сервера (по умолчанию 8554): "
if "%RTSP_PORT%"=="" set RTSP_PORT=8554

set /p RTSP_PATH="Введите путь к потоку на RTSP-сервере (по умолчанию 'stream'): "
if "%RTSP_PATH%"=="" set RTSP_PATH=stream

echo.
echo Запуск конвертера с параметрами:
echo RTMP URL: %RTMP_URL%
echo RTSP-порт: %RTSP_PORT%
echo RTSP-путь: %RTSP_PATH%
echo RTSP-выход будет доступен по адресу: rtsp://localhost:%RTSP_PORT%/%RTSP_PATH%
echo.

echo Для остановки нажмите Ctrl+C
echo.

python main.py --rtmp-url "%RTMP_URL%" --rtsp-port %RTSP_PORT% --rtsp-path %RTSP_PATH%

echo.
echo Конвертер остановлен.
pause 
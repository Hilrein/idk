#!/usr/bin/env python3
import argparse
import signal
import sys
import time
from rtmp_to_rtsp_converter import RTMPtoRTSPConverter, logger, check_ffmpeg_installed

def signal_handler(sig, frame):
    """Обработчик сигнала для корректного завершения программы"""
    logger.info("Получен сигнал завершения, останавливаю конвертер...")
    if converter:
        converter.stop()
    sys.exit(0)

if __name__ == "__main__":
    # Проверяем наличие FFmpeg перед началом работы
    if not check_ffmpeg_installed():
        logger.error("FFmpeg не установлен или не найден в PATH. Выход.")
        sys.exit(1)
    
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description='Конвертер RTMP в RTSP')
    parser.add_argument('--rtmp-url', type=str, required=True,
                        help='URL-адрес источника RTMP (например, rtmp://example.com/live/stream)')
    parser.add_argument('--rtsp-port', type=int, default=8554,
                        help='Порт для RTSP-сервера (по умолчанию: 8554)')
    parser.add_argument('--rtsp-path', type=str, default='stream',
                        help='Путь к потоку на RTSP-сервере (по умолчанию: "stream")')
    parser.add_argument('--max-retries', type=int, default=10,
                        help='Максимальное количество попыток перезапуска при ошибках (по умолчанию: 10)')
    parser.add_argument('--retry-interval', type=int, default=5,
                        help='Интервал между попытками перезапуска в секундах (по умолчанию: 5)')
    
    args = parser.parse_args()
    
    # Настройка обработчика сигналов для корректного завершения
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Инициализация конвертера
    converter = RTMPtoRTSPConverter(
        rtmp_url=args.rtmp_url,
        rtsp_port=args.rtsp_port,
        rtsp_path=args.rtsp_path
    )
    
    # Запуск конвертера
    logger.info(f"Запуск конвертера RTMP → RTSP")
    logger.info(f"RTMP источник: {args.rtmp_url}")
    logger.info(f"RTSP выход: rtsp://localhost:{args.rtsp_port}/{args.rtsp_path}")
    converter.start()
    
    # Основной цикл программы с контролем ошибок
    retry_count = 0
    try:
        while True:
            if not converter.is_running():
                retry_count += 1
                if retry_count > args.max_retries:
                    logger.error(f"Превышено максимальное количество попыток перезапуска ({args.max_retries}). Выход.")
                    break
                
                logger.error(f"Процесс конвертации остановился, попытка перезапуска {retry_count}/{args.max_retries}...")
                converter.start()
                
                # Если FFmpeg не установлен, выходим из цикла
                if not converter.ffmpeg_available:
                    logger.error("Невозможно продолжить работу без FFmpeg. Выход.")
                    break
            else:
                # Сброс счетчика попыток, если конвертер успешно работает
                retry_count = 0
                
            time.sleep(args.retry_interval)
    except KeyboardInterrupt:
        logger.info("Программа прервана пользователем")
        converter.stop()
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        converter.stop()
    
    logger.info("Программа завершена") 
"""
Скрипт для проверки доступности RTSP-потока
"""

import cv2
import argparse
import time
import sys


def test_rtsp_stream(rtsp_url, timeout=30, display=True):
    """
    Проверка доступности RTSP-потока и отображение видео (опционально)
    
    Args:
        rtsp_url: URL RTSP-потока для проверки
        timeout: Время ожидания подключения в секундах
        display: Флаг отображения видео
        
    Returns:
        bool: True если подключение успешно, False в противном случае
    """
    print(f"Подключение к RTSP потоку: {rtsp_url}")
    cap = cv2.VideoCapture(rtsp_url)
    
    if not cap.isOpened():
        print(f"Не удалось открыть RTSP поток: {rtsp_url}")
        return False
    
    start_time = time.time()
    frame_received = False
    
    while time.time() - start_time < timeout:
        ret, frame = cap.read()
        if ret:
            frame_received = True
            print(f"Кадр получен! Размер: {frame.shape}")
            if display:
                cv2.imshow('RTSP Test', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            print("Ожидание кадра...")
            time.sleep(1)
            continue
            
        if frame_received and not display:
            break
    
    cap.release()
    if display:
        cv2.destroyAllWindows()
    
    if frame_received:
        print("Тест RTSP соединения прошел успешно!")
        return True
    else:
        print(f"Тест RTSP соединения не удался. Время ожидания {timeout} секунд истекло.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Тест RTSP соединения')
    parser.add_argument('--rtsp-url', type=str, required=True,
                      help='URL RTSP потока для проверки')
    parser.add_argument('--timeout', type=int, default=30,
                      help='Время ожидания в секундах (по умолчанию: 30)')
    parser.add_argument('--no-display', action='store_true',
                      help='Не отображать видео, только проверить подключение')
    
    args = parser.parse_args()
    
    success = test_rtsp_stream(args.rtsp_url, args.timeout, not args.no_display)
    
    sys.exit(0 if success else 1) 
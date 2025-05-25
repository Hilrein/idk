import subprocess
import time
import os
import signal
import logging
import shutil
import sys
from typing import Optional

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("RTMPtoRTSPConverter")

def check_ffmpeg_installed():
    """
    Проверяет, установлен ли FFmpeg в системе
    
    Returns:
        bool: True если FFmpeg найден, False в противном случае
    """
    if shutil.which("ffmpeg") is None:
        logger.error("FFmpeg не найден! Пожалуйста, установите FFmpeg и добавьте его в PATH.")
        logger.error("Подробные инструкции по установке можно найти в файле README.md")
        return False
    return True

class RTMPtoRTSPConverter:
    """
    Класс для конвертации потока RTMP в RTSP с использованием FFmpeg
    """
    
    def __init__(self, rtmp_url: str, rtsp_port: int = 8554, rtsp_path: str = "stream"):
        """
        Инициализация конвертера
        
        Args:
            rtmp_url: URL источника RTMP
            rtsp_port: Порт для RTSP-сервера
            rtsp_path: Путь к потоку на RTSP-сервере
        """
        self.rtmp_url = rtmp_url
        self.rtsp_port = rtsp_port
        self.rtsp_path = rtsp_path
        self.rtsp_url = f"rtsp://localhost:{rtsp_port}/{rtsp_path}"
        self.ffmpeg_process: Optional[subprocess.Popen] = None
        self.running = False
        
        # Проверяем наличие FFmpeg
        self.ffmpeg_available = check_ffmpeg_installed()
    
    def start(self):
        """
        Запустить процесс конвертации RTMP в RTSP
        """
        if not self.ffmpeg_available:
            logger.error("Невозможно запустить конвертер без FFmpeg")
            return
            
        if self.running:
            logger.warning("Конвертер уже запущен")
            return
        
        logger.info(f"Запуск конвертации из {self.rtmp_url} в {self.rtsp_url}")
        
        # Команда FFmpeg для конвертации RTMP в RTSP
        cmd = [
            "ffmpeg",
            "-i", self.rtmp_url,
            "-rtsp_transport", "tcp",
            "-f", "rtsp",
            "-codec", "copy",  # Копировать кодеки без перекодирования
            self.rtsp_url
        ]
        
        try:
            # Запуск процесса FFmpeg
            self.ffmpeg_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            self.running = True
            logger.info(f"Процесс конвертации запущен с PID {self.ffmpeg_process.pid}")
        except FileNotFoundError:
            logger.error("FFmpeg не найден. Пожалуйста, установите FFmpeg и добавьте его в PATH.")
            logger.error("Подробные инструкции по установке можно найти в файле README.md")
            self.running = False
        except Exception as e:
            logger.error(f"Ошибка при запуске конвертера: {e}")
            self.running = False
    
    def stop(self):
        """
        Остановить процесс конвертации
        """
        if not self.running or self.ffmpeg_process is None:
            logger.warning("Конвертер не запущен")
            return
        
        logger.info("Остановка процесса конвертации")
        
        try:
            # Плавное завершение процесса
            if os.name == 'nt':  # Windows
                self.ffmpeg_process.send_signal(signal.CTRL_C_EVENT)
            else:  # Unix/Linux
                self.ffmpeg_process.send_signal(signal.SIGTERM)
                
            # Даём процессу время на завершение
            self.ffmpeg_process.wait(timeout=5)
            logger.info("Процесс конвертации успешно остановлен")
        except subprocess.TimeoutExpired:
            logger.warning("Процесс не завершился корректно, принудительное завершение")
            self.ffmpeg_process.kill()
        except Exception as e:
            logger.error(f"Ошибка при остановке конвертера: {e}")
        finally:
            self.running = False
            self.ffmpeg_process = None
    
    def is_running(self) -> bool:
        """
        Проверка, запущен ли процесс конвертации
        
        Returns:
            bool: True, если конвертер работает
        """
        if not self.ffmpeg_available:
            return False
            
        if self.ffmpeg_process is None:
            return False
        
        return_code = self.ffmpeg_process.poll()
        if return_code is None:
            return True
        else:
            logger.warning(f"Процесс FFmpeg завершился с кодом {return_code}")
            self.running = False
            return False 
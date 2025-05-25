FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Настройка рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Настройка порта для RTSP
EXPOSE 8554

# Запуск приложения
ENTRYPOINT ["python", "main.py"]

# Значения по умолчанию для ENTRYPOINT
CMD ["--rtmp-url", "rtmp://example.com/live/stream", "--rtsp-port", "8554", "--rtsp-path", "stream"] 
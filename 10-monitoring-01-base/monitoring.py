# Импорт необходимых библиотек
import os
import json
import psutil
from datetime import datetime

# Функция для сбора метрик системы
def collect_metrics():
    # Получение процентной загрузки процессора
    cpu_percent = psutil.cpu_percent()
    # Получение информации об использовании памяти
    mem_info = psutil.virtual_memory()
    # Расчет размера всех файлов в директории /var/log
    log_size = sum(os.path.getsize(os.path.join(root, name)) for root, _, files in os.walk('/var/log') for name in files)
    # Получение информации об использовании диска корневого раздела
    disk_usage = psutil.disk_usage('/')

    # Составление словаря с метриками
    metrics = {
        'timestamp': int(datetime.now().timestamp()),
        'CPU-load': cpu_percent,
        'memory used': mem_info.percent,
        '/var/log size': log_size,
        'disk utilization': disk_usage.percent
    }
    return metrics

# Функция для записи метрик в лог-файл
def write_metrics_to_log(metrics):
    # Форматирование имени файла лога
    log_file_name = datetime.now().strftime('%Y-%m-%d-awesome-monitoring.log')
    log_file_path = os.path.join('/var/log', log_file_name)

    # Запись метрик в файл лога
    with open(log_file_path, 'a') as log_file:
        json.dump(metrics, log_file)
        log_file.write('\n')  # Добавление перевода строки после каждого JSON объекта

# Главная часть скрипта
if __name__ == "__main__":
    # Сбор метрик
    metrics = collect_metrics()
    # Запись метрик в лог-файл
    write_metrics_to_log(metrics)
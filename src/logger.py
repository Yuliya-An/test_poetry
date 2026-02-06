import logging
from pathlib import Path


def setup_logging(log_dir: str = "logs", log_file: str = "app.log") -> None:
    """
    Настройка логирования.
    Создаёт папку logs и файл app.log, форматирует вывод.
    """
    # Создаём папку для логов, если её нет
    path = Path(log_dir)
    path.mkdir(exist_ok=True)

    # Полный путь к файлу лога
    log_path = path / log_file

    # Формат записей: время - имя логера - уровень - сообщение
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для записи в файл (перезаписывает при каждом запуске)
    file_handler = logging.FileHandler(log_path, mode='w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # В файл пишем всё

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)  # В консоль только INFO и выше

    # Настраиваем корневой логер
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Ловим все сообщения

    # Чистим старые обработчики, чтобы не дублировались
    root_logger.handlers.clear()

    # Добавляем наши обработчики
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

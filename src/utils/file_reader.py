import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def read_operations_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Читает JSON-файл с операциями."""
    logger.debug(f"Чтение файла: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Проверка, что это список
        if not isinstance(data, list):
            logger.error(f"В файле {file_path} не список, а {type(data)}")
            raise ValueError("Ожидался список операций")

        logger.info(f"Файл {file_path} прочитан, записей: {len(data)}")
        return data

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}", exc_info=True)
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка JSON в файле {file_path}: {e}", exc_info=True)
        raise

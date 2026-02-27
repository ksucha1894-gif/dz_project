import json
import logging
import os
from typing import Dict, List

current_dir = os.path.dirname(os.path.abspath(__file__))  # Определяем путь в корневую папку проекта

rel_file_path_1 = os.path.join(current_dir, "../logs/utils.log")  # Определяем относительный путь к файлу
abs_file_path_1 = os.path.abspath(rel_file_path_1)  # Определяем абсолютный путь в файлу

logger = logging.getLogger('utils')
file_handler = logging.FileHandler(abs_file_path_1)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def load_transactions(filepath: str) -> List[Dict]:
    """Загружает данные о финансовых транзакциях из JSON-файла.
    :rtype: List[Dict]
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            logger.info(f"Попытка открытия файла: '{filepath}'.")
            data = json.load(f)
            logger.info(f"Успешно загружены данные из файла: '{filepath}'.")
    except FileNotFoundError:
        logger.error(f"Файл по пути '{filepath}' не найден.")
        return []
    except json.JSONDecodeError:
        logger.error(f"Файл '{filepath}' содержит некорректный JSON.")
        return []
    except Exception as e:
        logger.error(f"Непредвиденная ошибка при загрузке файла '{filepath}': {e}")
        return []

    # Проверка структуры данных
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        logger.info(f"Данные в файле '{filepath}' успешно проверены и имеют правильную структуру.")
        return data
    else:
        logger.error(f"Данные в файле '{filepath}' не являются списком словарей.")
        return []

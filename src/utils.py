import json
from typing import Dict, List


def load_transactions(filepath: str) -> List[Dict]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл по пути '{filepath}' не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: Файл '{filepath}' содержит некорректный JSON.")
        return []
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return []

    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return data
    else:
        print(f"Ошибка: Данные в файле '{filepath}' не являются списком словарей.")
        return []

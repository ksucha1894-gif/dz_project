import re

from collections import Counter
from typing import Dict, List


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Ищет в списке словарей по ключу 'description' строки, содержащие search (регулярное выражение).
    Возвращает список словарей, соответствующих условию.
    """
    pattern = re.compile(search, re.IGNORECASE)  # Игнорируем регистр для поиска

    result = []
    for record in data:
        description = record.get('description', '')
        if pattern.search(description):
            result.append(record)
    return result


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по каждой категории на основе поля 'description'.
    Использует Counter для подсчета.
    """
    # Создаем Counter для хранения количества операций по категориям
    category_counts: Counter[str] = Counter()

    # Предварительно формируем регулярные выражения для каждой категории
    category_patterns = {
        cat: re.compile(re.escape(cat), re.IGNORECASE)
        for cat in categories
    }

    for record in data:
        description = record.get('description', '')

        # Проверяем описание на совпадение с категориями
        for cat, pattern in category_patterns.items():
            if pattern.search(description):
                category_counts[cat] += 1
                break  # нашли категорию, идем к следующей операции

    # Возвращаем Counter как словарь
    return dict(category_counts)

import random
import re
from collections import defaultdict
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
    Использует регулярные выражения для поиска, а также random для случайных целей
    (например, при отсутствии совпадений).
    """
    # Создаем словарь с дефолтным значением 0 для каждой категории
    category_counts: Dict[str, int] = defaultdict(int)

    # Предварительно формируем регулярные выражения для каждой категории
    category_patterns = {
        cat: re.compile(re.escape(cat), re.IGNORECASE)
        for cat in categories
    }

    for record in data:
        description = record.get('description', '')
        matched_category = None

        # Проверяем описание на совпадение с категориями
        for cat, pattern in category_patterns.items():
            if pattern.search(description):
                category_counts[cat] += 1
                matched_category = cat
                break  # нашли категорию, идем к следующей операции

        # Если ни одна категория не совпала, можно присвоить "прочие" или случайную категорию
        if matched_category is None:
            # Вариант с рандомным выбором категории
            random_cat = random.choice(categories)
            category_counts[random_cat] += 1

    # Преобразуем defaultdict в обычный dict перед возвратом
    return dict(category_counts)

from functools import wraps
from time import time
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функции.
    Если задан `filename`, лог записывается в файл, иначе выводится в консоль.
    """
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            """Логирование начала и конца выполнения функции, а также ее результаты или возникшие ошибки"""
            try:
                start_time = time()
                result = func(*args, **kwargs)
                end_time = time()
                log_message = (f"Функция: {func.__name__}\n Время начала выполнения функции: {start_time}\n "
                               f"Время окончания выполнения функции: {end_time}\n Результат: {result}\n")
                if filename:
                    with open(filename, "a") as log_file:
                        log_file.write(log_message)
                else:
                    print(log_message)
                return result

            except Exception as e:
                error_message = f'{func.__name__} error: {str(e)}. Inputs: {args}, {kwargs}'
                if filename:
                    with open(filename, "a") as log_file:
                        log_file.write(error_message)
                else:
                    print(error_message)
                raise

        return inner

    return wrapper

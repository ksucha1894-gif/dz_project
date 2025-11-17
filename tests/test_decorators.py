from typing import Any

import pytest

from src.decorators import log


@log(None)
def add(x: int, y: int) -> int:
    return x + y


def test_add_log_output(capsys: pytest.CaptureFixture[str]) -> None:
    add(1, 2)
    captured = capsys.readouterr()
    assert "Функция: add" in captured.out
    assert "Результат: 3" in captured.out


def test_add_log_to_file(tmp_path: Any) -> None:
    log_file = tmp_path / "mylog.txt"

    @log(log_file)
    def add_func(x: int, y: int) -> int:
        return x + y

    add_func(1, 2)

    with open(log_file, "r") as f:
        content = f.read()
        assert "Функция: add_func" in content
        assert "Результат: 3" in content


@log(None)
def error_func(x: int, y: int) -> float:
    return x / y


def test_error_logging(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(ZeroDivisionError):
        error_func(1, 0)
    captured = capsys.readouterr()
    assert "error_func" in captured.out
    assert "division by zero" in captured.out

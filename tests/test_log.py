import os
from typing import Generator
import pytest
from src.decorators.log import log


@pytest.fixture
def remove_log_file() -> Generator[str, None, None]:
    filename = "test_log.txt"
    if os.path.exists(filename):
        os.remove(filename)
    yield filename
    if os.path.exists(filename):
        os.remove(filename)


def test_log_to_console_success(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def func(x: int, y: int) -> int:
        return x + y

    result = func(2, 3)
    captured = capsys.readouterr()
    assert result == 5
    assert "func ok" in captured.out


def test_log_to_console_error(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def func(x: int) -> int:
        if x < 0:
            raise ValueError("Negative!")
        return x

    with pytest.raises(ValueError):
        func(-1)

    captured = capsys.readouterr()
    assert "func error: ValueError" in captured.out
    assert "Inputs: (-1," in captured.out


def test_log_to_file_success(remove_log_file: str) -> None:
    filename = remove_log_file

    @log(filename=filename)
    def func(x: int, y: int) -> int:
        return x + y

    result = func(10, 20)
    assert result == 30

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    assert "func ok" in content


def test_log_to_file_error(remove_log_file: str) -> None:
    filename = remove_log_file

    @log(filename=filename)
    def func(x: int) -> int:
        if x == 0:
            raise ZeroDivisionError("Zero!")
        return 10 // x

    with pytest.raises(ZeroDivisionError):
        func(0)

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    assert "func error: ZeroDivisionError" in content
    assert "Inputs: (0," in content

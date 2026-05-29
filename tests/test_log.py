import os
from typing import Generator
import pytest
from src.decorators.log import log
from src.logger import setup_logging
from pathlib import Path


# Фикстура для удаления файла лога до и после теста
@pytest.fixture
def remove_log_file() -> Generator[str, None, None]:
    filename = "test_log.txt"
    if os.path.exists(filename):
        os.remove(filename)
    yield filename
    if os.path.exists(filename):
        os.remove(filename)


# Фикстура для временной директории
@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path / "test_project"


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


# Тесты для logger.py
def test_setup_logging_creates_directory(temp_dir: Path) -> None:
    """Проверяет создание папки logs."""
    temp_dir = temp_dir / "test_project"
    temp_dir.mkdir(parents=True, exist_ok=True)   # ← ВСТАВЬ ЭТУ СТРОКУ ЗДЕСЬ
    os.chdir(temp_dir)
    setup_logging()

    assert (temp_dir / "logs").exists()
    assert (temp_dir / "logs" / "app.log").exists()


def test_setup_logging_sets_handlers() -> None:
    """Проверяет, что обработчики добавлены."""
    # Сохраняем исходные обработчики
    import logging
    original_handlers = logging.getLogger().handlers.copy()

    try:
        from src.logger import setup_logging
        setup_logging()

        root_logger = logging.getLogger()
        # Проверяем, что есть два обработчика
        assert len(root_logger.handlers) == 2
    finally:
        # Восстанавливаем
        logging.getLogger().handlers = original_handlers

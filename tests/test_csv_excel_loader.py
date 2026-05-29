import pytest
from unittest.mock import patch, PropertyMock, MagicMock
from pathlib import Path
from typing import Generator
from src.csv_excel_loader import read_csv_transactions, read_excel_transactions


mock_transactions = [
    {"id": "1", "amount": 100.0, "currency": "USD", "description": "Test transaction"},
    {"id": "2", "amount": 200.0, "currency": "EUR", "description": "Another transaction"},
]


@pytest.fixture
def mock_pd_read_csv() -> Generator[MagicMock, None, None]:
    with patch("src.csv_excel_loader.Path.exists", return_value=True), \
         patch("src.csv_excel_loader.Path.suffix", new_callable=PropertyMock) as mock_suffix, \
         patch("pandas.read_csv") as mock_read_csv:
        mock_suffix.return_value = ".csv"
        mock_df = MagicMock()
        mock_df.to_dict.return_value = mock_transactions
        mock_df.empty = False
        mock_read_csv.return_value = mock_df
        yield mock_read_csv


@pytest.fixture
def mock_pd_read_excel() -> Generator[MagicMock, None, None]:
    with patch("src.csv_excel_loader.Path.exists", return_value=True), \
         patch("src.csv_excel_loader.Path.suffix", new_callable=PropertyMock) as mock_suffix, \
         patch("pandas.read_excel") as mock_read_excel:
        mock_suffix.return_value = ".xlsx"
        mock_df = MagicMock()
        mock_df.to_dict.return_value = mock_transactions
        mock_df.empty = False
        mock_read_excel.return_value = mock_df
        yield mock_read_excel


def test_read_csv_transactions(mock_pd_read_csv: MagicMock) -> None:
    path: str = "dummy.csv"
    result = read_csv_transactions(path)
    assert result == mock_transactions
    mock_pd_read_csv.assert_called_once_with(Path(path), encoding="utf-8")


def test_read_excel_transactions(mock_pd_read_excel: MagicMock) -> None:
    path: str = "dummy.xlsx"
    result = read_excel_transactions(path)
    assert result == mock_transactions
    mock_pd_read_excel.assert_called_once_with(Path(path), engine="openpyxl")


def test_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        read_csv_transactions("nonexistent.csv")


def test_unsupported_extension() -> None:
    with patch("src.csv_excel_loader.Path.exists", return_value=True):
        with pytest.raises(ValueError):
            read_csv_transactions("file.unsupported")


def test_empty_csv_file() -> None:
    with patch("src.csv_excel_loader.Path.exists", return_value=True), \
         patch("src.csv_excel_loader.Path.suffix", new_callable=PropertyMock) as mock_suffix, \
         patch("pandas.read_csv") as mock_read_csv:
        mock_suffix.return_value = ".csv"
        mock_df = MagicMock()
        mock_df.empty = True
        mock_read_csv.return_value = mock_df
        result = read_csv_transactions("empty.csv")
        assert result == []


def test_empty_excel_file() -> None:
    with patch("src.csv_excel_loader.Path.exists", return_value=True), \
         patch("src.csv_excel_loader.Path.suffix", new_callable=PropertyMock) as mock_suffix, \
         patch("pandas.read_excel") as mock_read_excel:
        mock_suffix.return_value = ".xlsx"
        mock_df = MagicMock()
        mock_df.empty = True
        mock_read_excel.return_value = mock_df
        result = read_excel_transactions("empty.xlsx")
        assert result == []

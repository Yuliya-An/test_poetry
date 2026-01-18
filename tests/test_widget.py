import pytest
from src.widget import mask_account_card, get_date

@pytest.mark.parametrize("text, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
])
def test_mask_account_card(text, expected):
    assert mask_account_card(text) == expected

@pytest.mark.parametrize("date_str, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2019-07-03T18:35:29.512364", "03.07.2019"),
])
def test_get_date(date_str, expected):
    assert get_date(date_str) == expected

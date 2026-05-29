import pytest


from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1596837868705199", "1596 83** **** 5199"),
    ],
)
def test_mask_card(card: str, expected: str) -> None:
    assert get_mask_card_number(card) == expected


@pytest.mark.parametrize(
    "account, expected",
    [
        ("73654108430135874305", "**4305"),
    ],
)
def test_mask_account(account: str, expected: str) -> None:
    assert get_mask_account(account) == expected

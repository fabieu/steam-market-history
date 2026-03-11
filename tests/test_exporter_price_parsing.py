import pytest

from steam_market_history.modules.exporter import _parse_price


@pytest.mark.parametrize(
    ("raw_price", "expected"),
    [
        ("1.234,56€", 1234.56),
        ("1,234.56", 1234.56),
        ("1 234,56 EUR", 1234.56),
        ("1.234.567,89 €", 1234567.89),
        ("1,234,567.89 USD", 1234567.89),
        ("1.234", 1234.0),
        ("1,234", 1234.0),
        ("12,- €", 12.00),
    ],
)
def test_parse_price_locale_and_currency_formats(raw_price: str, expected: float) -> None:
    assert _parse_price(raw_price) == expected


def test_parse_price_invalid_returns_zero() -> None:
    assert _parse_price("not-a-price") == 0.0

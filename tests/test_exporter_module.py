import csv
import json
from uuid import UUID

from steam_market_history.models import MarketTransaction
from steam_market_history.modules import exporter


def _sample_transactions() -> list[MarketTransaction]:
    return [
        MarketTransaction(
            game_name="Test Game",
            item_name="Test Item",
            listed_date="17 Jan",
            price="1.234,56€",
            gain_or_loss="+",
            image_url="https://example.com/item.png",
        ),
        MarketTransaction(
            game_name="Test Game",
            item_name="Sold Item",
            listed_date="18 Jan",
            price="2.000,00€",
            gain_or_loss="-",
            image_url="https://example.com/sold.png",
        ),
    ]


def test_build_output_path_uses_base_name_and_extension(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(exporter.uuid, "uuid4", lambda: UUID("12345678-1234-5678-1234-567812345678"))

    output_path = exporter._build_output_path(tmp_path, "csv")

    assert output_path.is_absolute()
    assert output_path.name == "steam-market-history-12345678-1234-5678-1234-567812345678.csv"


def test_normalize_price_replaces_dash_decimal() -> None:
    assert exporter._normalize_price("12,-- €") == "12,00 €"
    assert exporter._normalize_price(None) == ""


def test_format_date_handles_valid_invalid_and_empty() -> None:
    assert exporter._format_date("17 Jan") == "17th January"
    assert exporter._format_date("29 Feb") == "29th February"
    assert exporter._format_date("not-a-date") == "not-a-date"
    assert exporter._format_date(None) == ""


def test_extract_currency_detects_prefix_and_suffix() -> None:
    suffix = [
        MarketTransaction("Game", "Item", "17 Jan", "1.00€", "+", None),
    ]
    prefix = [
        MarketTransaction("Game", "Item", "17 Jan", "$1.00", "+", None),
    ]
    unknown = [MarketTransaction("Game", "Item", "17 Jan", "1234", "+", None)]

    assert exporter._extract_currency(suffix) == ("€", False)
    assert exporter._extract_currency(prefix) == ("$", True)
    assert exporter._extract_currency(unknown) == ("", False)


def test_format_currency_for_prefix_and_suffix() -> None:
    assert exporter._format_currency(12.5, "$", True) == "$12.50"
    assert exporter._format_currency(12.5, "€", False) == "12.50€"


def test_to_csv_writes_expected_rows(tmp_path, monkeypatch) -> None:
    output_path = tmp_path / "output.csv"
    monkeypatch.setattr(exporter, "_build_output_path", lambda *_: output_path)
    monkeypatch.setattr(exporter.console, "print", lambda *args, **kwargs: None)

    transactions = _sample_transactions()
    exporter.to_csv(transactions, tmp_path)

    with output_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))

    assert rows[0] == ["game_name", "item_name", "listed_date", "price", "gain_or_loss", "image_url"]
    assert rows[1][0:4] == ["Test Game", "Test Item", "17 Jan", "1.234,56€"]


def test_to_json_writes_wrapped_data(tmp_path, monkeypatch) -> None:
    output_path = tmp_path / "output.json"
    monkeypatch.setattr(exporter, "_build_output_path", lambda *_: output_path)
    monkeypatch.setattr(exporter.console, "print", lambda *args, **kwargs: None)

    transactions = _sample_transactions()
    exporter.to_json(transactions, tmp_path)

    content = json.loads(output_path.read_text(encoding="utf-8"))
    assert "data" in content
    assert len(content["data"]) == 2
    assert content["data"][0]["item_name"] == "Test Item"


def test_to_html_renders_summary_and_price_dataset(tmp_path, monkeypatch) -> None:
    output_path = tmp_path / "output.html"
    monkeypatch.setattr(exporter, "_build_output_path", lambda *_: output_path)
    monkeypatch.setattr(exporter.console, "print", lambda *args, **kwargs: None)

    transactions = _sample_transactions()
    exporter.to_html(transactions, tmp_path)

    html = output_path.read_text(encoding="utf-8")
    assert "Steam Market History Export" in html
    assert "data-price=\"1234.56\"" in html
    assert "data-price=\"2000.0\"" in html
    assert "Total purchased" in html
    assert "Total sold" in html
    assert "+765.44€" in html

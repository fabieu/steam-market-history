import csv
import json
import re
import uuid
from dataclasses import asdict, fields
from datetime import datetime
from pathlib import Path

from jinja2 import Template, select_autoescape

from steam_market_history.console import CHECKMARK, console
from steam_market_history.models import MarketTransaction

# Global variables
base_name = "steam-market-history"


def _build_output_path(base_path: Path, extension: str) -> Path:
    return (base_path / f"{base_name}-{uuid.uuid4()}.{extension}").resolve()


def _parse_price(price: str | None) -> float:
    if not price:
        return 0.0

    cleaned = re.sub(r'[^\d,.]', '', price.strip())
    cleaned = cleaned.replace(',', '.')

    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _extract_currency(transactions: list[MarketTransaction]) -> str:
    for t in transactions:
        if t.price:
            match = re.search(r'[^\d\s,.\-]', t.price)
            if match:
                return match.group()
    return ''


def to_csv(market_transactions: list[MarketTransaction], base_path: Path) -> None:
    output_path = _build_output_path(base_path, "csv")

    with open(output_path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([f.name for f in fields(MarketTransaction)])
        writer.writerows([asdict(t).values() for t in market_transactions])

    console.print(f"{CHECKMARK} CSV exported: [bold]{output_path}[/bold]", highlight=False)


def to_html(market_transactions: list[MarketTransaction], base_path: Path) -> None:
    output_path = _build_output_path(base_path, "html")

    with open(Path(__file__).parent.parent / "templates/index.html", encoding="utf-8") as template_file:
        template = Template(template_file.read(), autoescape=select_autoescape())

    with open(output_path, 'w', encoding="utf-8") as rendered_file:
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        currency = _extract_currency(market_transactions)
        total_purchases = round(sum(_parse_price(t.price) for t in market_transactions if t.gain_or_loss == '+'), 2)
        total_sales = round(sum(_parse_price(t.price) for t in market_transactions if t.gain_or_loss == '-'), 2)
        net = round(total_sales - total_purchases, 2)
        summary = {
            "totalTransactions": len(market_transactions),
            "totalPurchases": f"{total_purchases:.2f}{currency}",
            "totalSales": f"{total_sales:.2f}{currency}",
            "net": f"{net:+.2f}{currency}",
        }
        rendered_file.write(template.render(
            summary=summary, transactions=market_transactions, current_date=current_date))

    console.print(f"{CHECKMARK} HTML exported: [bold]{output_path}[/bold]", highlight=False)


def to_json(market_transactions: list[MarketTransaction], base_path: Path) -> None:
    output_path = _build_output_path(base_path, "json")

    wrapper = {
        "data": [asdict(t) for t in market_transactions]
    }

    with open(output_path, 'w', encoding="utf-8") as file:
        file.write(json.dumps(wrapper, indent=4))

    console.print(f"{CHECKMARK} JSON exported: [bold]{output_path}[/bold]", highlight=False)

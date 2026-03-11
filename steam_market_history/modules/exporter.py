import csv
import json
import re
import uuid
from dataclasses import asdict, fields
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from steam_market_history.console import CHECKMARK, console
from steam_market_history.models import MarketTransaction

# Global variables
base_name = "steam-market-history"


def _build_output_path(base_path: Path, extension: str) -> Path:
    return (base_path / f"{base_name}-{uuid.uuid4()}.{extension}").resolve()


def _normalize_price(price: str | None) -> str:
    """Jinja filter. Replaces dash-based decimal notation (e.g. ',-' / ',--') with ',00' for display."""
    if not price:
        return ''

    return re.sub(r',-+', ',00', price)


def _parse_price(price: str | None) -> float:
    """Jinja filter. Strips currency symbols and normalises decimal separators, returning a float."""
    if not price:
        return 0.0

    cleaned = _normalize_price(price).strip()
    cleaned = re.sub(r'[^\d,.]', '', cleaned)
    cleaned = cleaned.replace(',', '.')

    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _format_date(date: str | None) -> str:
    """Jinja filter. Converts Steam's short date (e.g. '17 Jan') to English ordinal format (e.g. '17th January')."""
    if not date:
        return ''
    try:
        dt = datetime.strptime(date.strip(), '%d %b')
        day = dt.day
        suffix = 'th' if 11 <= day % 100 <= 13 else ['th', 'st', 'nd', 'rd', 'th'][min(day % 10, 4)]
        return f"{day}{suffix} {dt.strftime('%B')}"
    except ValueError:
        return date


def _extract_currency(transactions: list[MarketTransaction]) -> tuple[str, bool]:
    """Returns (symbol, is_prefix). is_prefix is True when the symbol appears before the digits."""
    for t in transactions:
        if t.price:
            match = re.search(r'[^\d\s,.\-]', t.price)
            if match:
                symbol = match.group()
                is_prefix = t.price.strip().startswith(symbol)
                return symbol, is_prefix
    return '', False


def _format_currency(amount: float, symbol: str, is_prefix: bool) -> str:
    if is_prefix:
        return f"{symbol}{amount:.2f}"
    else:
        return f"{amount:.2f}{symbol}"


def to_csv(market_transactions: list[MarketTransaction], base_path: Path) -> None:
    output_path = _build_output_path(base_path, "csv")

    with open(output_path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([f.name for f in fields(MarketTransaction)])
        writer.writerows([asdict(t).values() for t in market_transactions])

    console.print(f"{CHECKMARK} CSV exported: [bold]{output_path}[/bold]", highlight=False)


def to_html(market_transactions: list[MarketTransaction], base_path: Path) -> None:
    output_path = _build_output_path(base_path, "html")

    env = Environment(
        loader=FileSystemLoader(Path(__file__).parent.parent / "templates"),
        autoescape=select_autoescape(),
    )
    env.filters['format_date'] = _format_date
    env.filters['normalize_price'] = _normalize_price
    env.filters['parse_price'] = _parse_price
    template = env.get_template("index.html")

    with open(output_path, 'w', encoding="utf-8") as rendered_file:
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        currency, is_prefix = _extract_currency(market_transactions)
        total_purchases = round(sum(_parse_price(t.price) for t in market_transactions if t.gain_or_loss == '+'), 2)
        total_sales = round(sum(_parse_price(t.price) for t in market_transactions if t.gain_or_loss == '-'), 2)
        net = round(total_sales - total_purchases, 2)
        net_sign = '+' if net >= 0 else '-'
        summary = {
            "totalTransactions": len(market_transactions),
            "totalPurchases": _format_currency(total_purchases, currency, is_prefix),
            "totalSales": _format_currency(total_sales, currency, is_prefix),
            "net": f"{net_sign}{_format_currency(abs(net), currency, is_prefix)}",
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

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


def _resolve_single_separator(chunks: list[str]) -> str:
    """Infer decimal vs thousands for a value that contains only one type of separator.

    Multiple same-separator groups (e.g. 1,234,567) or a 3-digit trailing group
    (e.g. 1,234) indicate a thousand separator — strip it.  Any other trailing
    group length indicates a decimal separator.
    """
    trailing_chunk = chunks[-1]
    if len(chunks) > 2 or len(trailing_chunk) == 3:
        # Thousands separator: remove it entirely.
        return ''.join(chunks)
    # Decimal separator: replace it with a dot.
    return ''.join(chunks[:-1]) + '.' + trailing_chunk


def _parse_price(price: str | None) -> float:
    """Jinja filter. Strips currency symbols and normalizes locale-style separators to float."""
    if not price:
        return 0.0

    normalized_price_text = _normalize_price(price).strip()

    # Keep only digits, separator candidates, and whitespace; strip spaces used as thousands separators.
    numeric_text = re.sub(r'[^\d,.\s]', '', normalized_price_text)
    numeric_text = re.sub(r'\s+', '', numeric_text)
    if not numeric_text:
        return 0.0

    last_comma_index = numeric_text.rfind(',')
    last_dot_index = numeric_text.rfind('.')

    if last_comma_index != -1 and last_dot_index != -1:
        # When both separators exist, the rightmost separator is the decimal marker.
        decimal_separator = ',' if last_comma_index > last_dot_index else '.'
        thousands_separator = '.' if decimal_separator == ',' else ','
        numeric_text = (numeric_text
                        .replace(thousands_separator, '')
                        .replace(decimal_separator, '.')
                        )
    elif ',' in numeric_text:
        # Infer whether comma is decimal or thousands separator from group shape.
        numeric_text = _resolve_single_separator(numeric_text.split(','))
    elif '.' in numeric_text:
        # Same heuristic for dot-only values.
        numeric_text = _resolve_single_separator(numeric_text.split('.'))

    try:
        return float(numeric_text)
    except ValueError:
        return 0.0


def _format_date(date: str | None) -> str:
    """Jinja filter. Converts Steam's short date (e.g. '17 Jan') to English ordinal format (e.g. '17th January')."""
    if not date:
        return ''
    try:
        dt_fmt = '%d %b %Y'  # Year is required for strptime, but we can ignore it since we're only formatting day and month.
        dt = datetime.strptime(f"{date.strip()} 2000", dt_fmt)  # Default to a leap year to allow parsing of Feb 29
        day = dt.day
        suffix = 'th' if 11 <= day % 100 <= 13 else ['th', 'st', 'nd', 'rd', 'th'][min(day % 10, 4)]
        return f"{day}{suffix} {dt.strftime('%B')}"
    except ValueError:
        return date


def _extract_currency(transactions: list[MarketTransaction]) -> tuple[str, bool]:
    """Returns (symbol, is_prefix). is_prefix is True when the symbol appears before the digits."""
    for transaction in transactions:
        if not transaction.price:
            continue

        price = transaction.price.strip()

        prefix_match = re.match(r'^([^\d\s,.]+)', price)
        if prefix_match:
            return prefix_match.group(1), True

        suffix_match = re.fullmatch(r'[\d\s,.]*([^\d\s,.]+)', price)
        if suffix_match:
            return suffix_match.group(1), False

    return '', False


def _format_currency(amount: float, symbol: str, is_prefix: bool) -> str:
    if is_prefix:
        return f"{symbol}{amount:.2f}"
    else:
        return f"{amount:.2f}{symbol}"


def _to_normalized_dict(t: MarketTransaction) -> dict:
    d = asdict(t)
    d['price'] = _normalize_price(d['price'])
    return d


def to_csv(market_transactions: list[MarketTransaction], base_path: Path) -> None:
    output_path = _build_output_path(base_path, "csv")

    with open(output_path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([f.name for f in fields(MarketTransaction)])
        writer.writerows([_to_normalized_dict(t).values() for t in market_transactions])

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
        "data": [_to_normalized_dict(t) for t in market_transactions]
    }

    with open(output_path, 'w', encoding="utf-8") as file:
        file.write(json.dumps(wrapper, indent=4))

    console.print(f"{CHECKMARK} JSON exported: [bold]{output_path}[/bold]", highlight=False)

import csv
import json
import typer
from dataclasses import asdict
from datetime import datetime
from jinja2 import Template, select_autoescape
from pathlib import Path
from steam_market_history.console import CHECKMARK, console
from steam_market_history.models import MarketTransaction

# Global variables
base_name = "steam-market-history"


def to_csv(market_transactions: list[MarketTransaction], path: Path, launch: bool) -> None:
    filename = base_name + ".csv"
    output_path = (path / filename).resolve()

    with open(output_path, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(asdict(market_transactions[0]).keys())
        writer.writerows([asdict(x).values() for x in market_transactions])

    console.print(f"{CHECKMARK} CSV exported: [bold]{output_path}[/bold]")

    if launch:
        typer.launch(str(output_path), locate=True)


def to_html(market_transactions: list[MarketTransaction], path: Path, launch: bool) -> None:
    filename = base_name + ".html"
    output_path = (path / filename).resolve()

    with open(Path(__file__).parent.parent / "templates/index.html", encoding="utf-8") as template_file:
        template = Template(template_file.read(), autoescape=select_autoescape())

    with open(output_path, 'w', encoding="utf-8") as rendered_file:
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        summary = {
            "totalTransactions": len(market_transactions)
        }
        rendered_file.write(template.render(
            summary=summary, transactions=market_transactions, current_date=current_date))

    console.print(f"{CHECKMARK} HTML exported: [bold]{output_path}[/bold]")

    if launch:
        typer.launch(str(output_path))


def to_json(market_transactions: list[MarketTransaction], path: Path, launch: bool) -> None:
    filename = base_name + ".json"
    output_path = (path / filename).resolve()

    wrapper = {
        "data": [asdict(t) for t in market_transactions]
    }

    with open(output_path, 'w', encoding="utf-8") as file:
        file.write(json.dumps(wrapper, indent=4))

    console.print(f"{CHECKMARK} JSON exported: [bold]{output_path}[/bold]")

    if launch:
        typer.launch(str(output_path))

# Build-in modules
import csv
import json
from datetime import datetime
from pathlib import Path

# PyPi modules
from jinja2 import Template, select_autoescape
import typer

# Global variables
base_name = "steam-market-history"


def to_csv(market_transactions: list, path: Path, launch: bool) -> None:
    filename = base_name + ".csv"

    with open(filename, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(market_transactions[0].keys())
        writer.writerows([x.values() for x in market_transactions])

    if launch:
        typer.launch(str(path / filename), locate=True)


def to_html(market_transactions: list, path: Path, launch: bool) -> None:
    filename = base_name + ".html"

    with open(Path(__file__).parent.parent / "templates/index.html", encoding="utf-8") as template_file:
        template = Template(template_file.read(), autoescape=select_autoescape())

    with open(filename, 'w', encoding="utf-8") as rendered_file:
        current_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        summary = {
            "totalTransactions": len(market_transactions)
        }
        rendered_file.write(template.render(
            summary=summary, transactions=market_transactions, current_date=current_date))

    if launch:
        typer.launch(str(path / filename))


def to_json(market_transactions: list, path: Path, launch: bool) -> None:
    filename = base_name + ".json"

    wrapper = {
        "data": market_transactions
    }

    with open(filename, 'w', encoding="utf-8") as file:
        file.write(json.dumps(wrapper, indent=4))

    if launch:
        typer.launch(str(path / filename))

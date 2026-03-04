import json
from dataclasses import asdict
from pathlib import Path

import typer

from steam_market_history import __version__, __metadata__
from steam_market_history.console import console, ERROR_STYLE, WARNING_STYLE
from steam_market_history.models import MarketTransaction
from steam_market_history.modules import steam, exporter

app = typer.Typer(help=f"steam-market-history v{__version__}")

CACHE_DIR = Path(".cache")
CACHE_PATH_TRANSACTIONS = CACHE_DIR / "steam_market_transactions.json"


def _load_cached_transactions() -> list[MarketTransaction] | None:
    if not CACHE_PATH_TRANSACTIONS.exists():
        return None

    try:
        with open(CACHE_PATH_TRANSACTIONS, 'r', encoding="utf-8") as f:
            return [MarketTransaction(**t) for t in json.load(f)]
    except (json.JSONDecodeError, TypeError, KeyError) as e:
        console.print(f"Warning: cache file is corrupted ({e}), re-fetching.", style=WARNING_STYLE)

        CACHE_PATH_TRANSACTIONS.unlink(missing_ok=True)
        return None


def _save_cached_transactions(market_transactions: list[MarketTransaction]) -> None:
    CACHE_DIR.mkdir(exist_ok=True)  # Ensure the cache directory exists

    with open(CACHE_PATH_TRANSACTIONS, 'w', encoding="utf-8") as f:
        json.dump([asdict(t) for t in market_transactions], f, indent=4)


@app.command()
def version():
    """
    Display detailed information about this package. For more information use 'steam-market-history --help'
    """
    console.print(f"steam-market-history")
    console.print(f"Version: {__version__}")
    console.print(f"Author: {__metadata__.get('Author')}")
    console.print(f"License: {__metadata__.get('License')}")


@app.command()
def export(
        export_csv: bool = typer.Option(False, "--csv", help="Generate steam market history as csv file"),
        export_html: bool = typer.Option(False, "--html", help="Generate steam market history as interactive website"),
        export_json: bool = typer.Option(False, "--json", help="Generate steam market history as json file"),
        base_path: Path = typer.Option(Path.cwd() / "export", "--path", help="Path for file export"),
        cache: bool = typer.Option(False, help="Use cached market transactions for faster subsequent exports")
):
    """
    Export your entire steam market history to a csv or html file. For more information use 'steam-market-history
    export --help'.
    """
    # Check if at least one export option is provided
    if True not in {export_csv, export_html, export_json}:
        console.print(
            "Please provide at least one export option! For more information use 'steam-market-history export --help'",
            style=ERROR_STYLE)
        raise typer.Exit(1)

    market_transactions = _load_cached_transactions() if cache else None

    if market_transactions is None:
        steam_session = steam.login_cli()

        market_transactions = steam.fetch_market_history(steam_session)

        if cache:
            _save_cached_transactions(market_transactions)

    if export_csv or export_html or export_json:
        base_path.mkdir(exist_ok=True, parents=True)  # Ensure the base path exists

    if export_csv:
        exporter.to_csv(market_transactions, base_path)

    if export_html:
        exporter.to_html(market_transactions, base_path)

    if export_json:
        exporter.to_json(market_transactions, base_path)


if __name__ == "__main__":
    app()

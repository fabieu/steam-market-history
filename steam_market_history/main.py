# Built-in modules
from pathlib import Path
import pickle

# PyPi modules
import typer

# Local modules
from steam_market_history import __version__
from steam_market_history.modules import steam, generator

# Initialize Typer and populate commands
app = typer.Typer(help=f"steam-market-history v{__version__}")


@app.command()
def version():
    """
    Display detailed information about this package
    """
    typer.echo(f"steam-market-history v{__version__}")


@app.command()
def export(
    csv_export: bool = typer.Option(False, "--csv", help="Generate steam market history as csv file"),
    html_export: bool = typer.Option(False, "--html", help="Generate steam market history as interactive website"),
    path: Path = typer.Option(Path.cwd(), help="Path for file export"),
    launch: bool = typer.Option(True, help="Automatically open file(s) after export"),
    cache: bool = typer.Option(False, help="Cache market transactions. Use with caution!"),
    interactive: bool = typer.Option(True, "--interactive/--non-interactive",
                                     help="Interactive or non-interactive steam authentication")
):
    """
    Export your steam market history to CSV or HTML webpage
    """
    market_transactions = None
    cache_path = "market_transactions.pkl"

    if csv_export or html_export:
        if cache:
            try:
                with open(cache_path, 'rb') as f:
                    market_transactions = pickle.load(f)
            except FileNotFoundError:
                market_transactions = steam.fetch_market_history(interactive=interactive)

                with open(cache_path, 'wb') as f:
                    pickle.dump(market_transactions, f)
        else:
            market_transactions = steam.fetch_market_history(interactive=interactive)
    else:
        typer.echo("Please provide at least one option! For more information use 'steam-market-history export --help'", err=True)

    if csv_export:
        generator.generate_csv(market_transactions, path, launch)

    if html_export:
        generator.generate_html(market_transactions, path, launch)


if __name__ == "__main__":
    app()

# Built-in modules
from pathlib import Path
import pickle

# PyPi modules
import typer

# Local modules
from steam_market_history import __version__, __metadata__
from steam_market_history.modules import steam, exporter

# Initialize Typer and populate commands
app = typer.Typer(help=f"steam-market-history v{__version__}")


@app.command()
def version():
    """
    Display detailed information about this package. For more information use 'steam-market-history --help'
    """
    typer.echo(f"steam-market-history")
    typer.echo(f"Version: {__version__}")
    typer.echo(f"Author: {__metadata__.get('Author')}")
    typer.echo(f"License: {__metadata__.get('License')}")


@app.command()
def export(
        export_csv: bool = typer.Option(False, "--csv", help="Generate steam market history as csv file"),
        export_html: bool = typer.Option(False, "--html", help="Generate steam market history as interactive website"),
        path: Path = typer.Option(Path.cwd(), help="Path for file export"),
        launch: bool = typer.Option(True, help="Automatically open file(s) after export"),
        cache: bool = typer.Option(False, help="Cache market transactions. Use with caution!"),
        interactive: bool = typer.Option(True, "--interactive/--non-interactive",
                                         help="Interactive or non-interactive steam authentication")
):
    """
    Export your entire steam market history to a csv or html file. For more information use 'steam-market-history
    export --help'.
    """
    cache_path = "market_transactions.pkl"

    # Check if at least one export option is provided
    if True not in {export_csv, export_html}:
        typer.echo(
            "Please provide at least one export option! For more information use 'steam-market-history export --help'",
            err=True)
        raise typer.Exit(1)

    # Login to steam
    if interactive:
        steam_session = steam.login_cli()
    else:
        steam_session = steam.login_non_interactive()

    # TODO: Improve caching mechanism (maybe use cachetools?)
    if cache:
        try:
            with open(cache_path, 'rb') as f:
                market_transactions = pickle.load(f)
        except FileNotFoundError:
            market_transactions = steam.fetch_market_history(steam_session)

            with open(cache_path, 'wb') as f:
                pickle.dump(market_transactions, f)
    else:
        market_transactions = steam.fetch_market_history(steam_session)

    if export_csv:
        exporter.to_csv(market_transactions, path, launch)

    if export_html:
        exporter.to_html(market_transactions, path, launch)


if __name__ == "__main__":
    app()

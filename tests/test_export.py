# Built-in modules
from pathlib import Path

# PyPi modules
from typer.testing import CliRunner
from dotenv import load_dotenv

# Local modules
from steam_market_history.main import app

load_dotenv()  # take environment variables from .env.
runner = CliRunner()


# def test_export_default():
#     result = runner.invoke(app, ["export", "--non-interactive", "--csv", "--html"])
#     assert result.exit_code == 0
#     assert Path("./steam-market-history.csv").is_file()
#     assert Path("./steam-market-history.html").is_file()

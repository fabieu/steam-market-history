from typer.testing import CliRunner

from steam_market_history.main import app

runner = CliRunner()


def test_version_default():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "steam-market-history" in result.stdout

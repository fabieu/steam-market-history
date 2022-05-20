from typer.testing import CliRunner

from steam_market_history.main import app

runner = CliRunner()


def test_export_default():
    # TODO: Find a way to programmatically authenticate to steam
    assert True

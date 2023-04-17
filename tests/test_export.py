# Built-in modules

# PyPi modules
from typer.testing import CliRunner

# Local modules

runner = CliRunner()


# TODO: Add tests for export command
# def test_export_default():
#     result = runner.invoke(app, ["export", "--non-interactive", "--csv", "--html"])
#     assert result.exit_code == 0
#     assert Path("./steam-market-history.csv").is_file()
#     assert Path("./steam-market-history.html").is_file()

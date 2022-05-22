# Built-in modules

# PyPi modules
import steam.webauth
import typer

# Local modules


def steam_auth_cli():
    """
    Login to Steam via CLI and return the authenticated websession
    """
    username = typer.prompt("Enter username")
    return steam.webauth.WebAuth(username).cli_login()


def steam_auth(username: str, password: str, email_code: str, twofactor_code: str):
    """
    Login to Steam with username and password and return the authenticated websession
    """
    return steam.webauth.WebAuth(username).login(pasword=password, email_code=email_code, twofactor_code=twofactor_code)

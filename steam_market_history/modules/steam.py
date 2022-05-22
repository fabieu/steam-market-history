# Build-in modules
import json
import re
import os

# PyPi modules
from bs4 import BeautifulSoup
import typer

# Local modules
from steam_market_history.modules import auth

app = typer.Typer()


def fetch_market_history(interactive: bool) -> list:
    """
    Fetching market history from Steam with the session created by auth_steam() and returns an array containing all market listings
    """

    if interactive:
        steam_session = auth.steam_auth_cli()
    elif not interactive:
        username = os.getenv("STEAM_USERNAME")
        password = os.getenv("STEAM_PASSWORD")
        email_code = os.getenv("STEAM_EMAIL_CODE")
        twofactor_code = os.getenv("STEAM_TWOFACTOR_CODE")
        steam_session = auth.steam_auth(username=username, password=password,
                                        email_code=email_code, twofactor_code=twofactor_code)

    # Initialize content objects for storing the market history from Steam
    content = ""
    market_transactions = []

    start = 0
    count = 500
    total_count = 1

    while start < total_count:
        page = steam_session.get(f'https://steamcommunity.com/market/myhistory/render/?count={count}&start={start}')
        page_content = json.loads(page.content)

        # Process market history with the BeautifulSoup library
        if page_content["results_html"]:
            content += page_content["results_html"]

        # Update conditions for while loop
        start = page_content["start"] + count

        if page_content.get("total_count"):
            total_count = page_content["total_count"]

    # Pulling content out of theHTML Response with the BeautifulSoup library
    DOMdocument = BeautifulSoup(content, 'html.parser')
    market_listing_rows = DOMdocument.find_all("div", class_="market_listing_row")

    for row in market_listing_rows:
        market_listing_price = row.find("span", class_="market_listing_price").text.strip()
        market_listing_item_name = row.find("span", class_="market_listing_item_name").text.strip()
        market_listing_game_name = row.find("span", class_="market_listing_game_name").text.strip()
        market_listing_gainorloss = row.find("div", class_="market_listing_gainorloss").text.strip()
        market_listing_listed_date = row.find("div", class_="market_listing_listed_date").text.strip()
        market_listing_item_img = row.find("img", class_="market_listing_item_img")["src"]

        # Format data
        if (re.search(r"^\d+,(\d|-){2}$", market_listing_price)):
            market_listing_price = market_listing_price.replace(
                ",--", ".00").replace(",", ".")

        # Format original steam data (market_listing_row) and add it to an array
        if market_listing_gainorloss in ["+", "-"]:
            market_transactions.append({
                "game_name": market_listing_game_name,
                "item_name": market_listing_item_name,
                "listed_date": market_listing_listed_date,
                "price": market_listing_price,
                "gainorloss": market_listing_gainorloss,
                "image_url": market_listing_item_img,
            })

    return market_transactions

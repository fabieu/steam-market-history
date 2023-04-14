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
        price_element = row.find("span", class_="market_listing_price")
        item_name_element = row.find("span", class_="market_listing_item_name")
        game_name_element = row.find("span", class_="market_listing_game_name")
        gainorloss_element = row.find("div", class_="market_listing_gainorloss")
        listed_date_element = row.find("div", class_="market_listing_listed_date")
        item_img_element = row.find("img", class_="market_listing_item_img")

        price = price_element.text.strip() if price_element else None
        item_name = item_name_element.text.strip() if item_name_element else None
        game_name = game_name_element.text.strip() if game_name_element else None
        gainorloss = gainorloss_element.text.strip() if gainorloss_element else None
        listed_date = listed_date_element.text.strip() if listed_date_element else None
        image_url = item_img_element.get("src") if item_img_element else None

        # Format data
        if (re.search(r"^\d+,(\d|-){2}$", price)):
            price = price.replace(",--", ".00").replace(",", ".")

        # Format original steam data (market_listing_row) and add it to an array
        if gainorloss in ["+", "-"]:
            market_transactions.append({
                "game_name": game_name,
                "item_name": item_name,
                "listed_date": listed_date,
                "price": price,
                "gainorloss": gainorloss,
                "image_url": image_url,
            })

    return market_transactions

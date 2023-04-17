# Build-in modules
import json
import os
import re

# PyPi modules
from bs4 import BeautifulSoup
import steam.webauth as wa
import typer

app = typer.Typer()


def login_cli() -> wa.WebAuth:
    """
    Login to Steam via CLI and return the authenticated websession
    """
    username = typer.prompt("Enter Steam username")
    return wa.WebAuth(username).cli_login()


def login_non_interactive() -> wa.WebAuth:
    """
    Login to Steam with username password, email_code and twofactor_code and return the authenticated websession
    """
    username = os.getenv("STEAM_USERNAME")
    password = os.getenv("STEAM_PASSWORD")
    email_code = os.getenv("STEAM_EMAIL_CODE")
    twofactor_code = os.getenv("STEAM_TWOFACTOR_CODE")
    return wa.WebAuth(username).login(password=password, email_code=email_code,
                                      twofactor_code=twofactor_code)


def fetch_market_history(steam_session: wa.WebAuth) -> list:
    """
    Fetch market history from Steam returns an array containing all market listings
    """

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

    # Process market history with the BeautifulSoup library
    document = BeautifulSoup(content, 'html.parser')
    market_listing_rows = document.find_all("div", class_="market_listing_row")

    for row in market_listing_rows:
        price_element = row.find("span", class_="market_listing_price")
        item_name_element = row.find("span", class_="market_listing_item_name")
        game_name_element = row.find("span", class_="market_listing_game_name")
        gain_or_loss_element = row.find("div", class_="market_listing_gainorloss")
        listed_date_element = row.find("div", class_="market_listing_listed_date")
        item_img_element = row.find("img", class_="market_listing_item_img")

        price = price_element.text.strip() if price_element else None
        item_name = item_name_element.text.strip() if item_name_element else None
        game_name = game_name_element.text.strip() if game_name_element else None
        gain_or_loss = gain_or_loss_element.text.strip() if gain_or_loss_element else None
        listed_date = listed_date_element.text.strip() if listed_date_element else None
        image_url = item_img_element.get("src") if item_img_element else None

        # Format price of market listing item
        if re.search(r"^\d+,(\d|-){2}$", price):
            price = price.replace(",--", ".00").replace(",", ".")

        # Format original steam data (market_listing_row) and add it to an array
        if gain_or_loss in ["+", "-"]:
            market_transactions.append({
                "game_name": game_name,
                "item_name": item_name,
                "listed_date": listed_date,
                "price": price,
                "gain_or_loss": gain_or_loss,
                "image_url": image_url,
            })

    return market_transactions

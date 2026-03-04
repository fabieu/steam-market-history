import json
import re

import requests
import steam.webauth as wa
import typer
from bs4 import BeautifulSoup
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn
from steam_market_history.console import CHECKMARK

from steam_market_history.models import MarketTransaction

app = typer.Typer()


def login_cli() -> requests.Session:
    """
    Login to Steam via CLI and return the authenticated web session
    """
    username = typer.prompt("Enter Steam username")
    return wa.WebAuth(username).cli_login()


def fetch_market_history(session: requests.Session) -> list[MarketTransaction]:
    """
    Fetch market history from Steam returns an array containing all market listings
    """

    # Initialize content objects for storing the market history from Steam
    content = ""
    market_transactions = []

    start = 0
    count = 500
    total_count = 1

    with Progress(
            SpinnerColumn(finished_text=CHECKMARK),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
    ) as progress:
        task = progress.add_task("Fetching market history...", total=None)

        while start < total_count:
            page = session.get(f'https://steamcommunity.com/market/myhistory/render/?count={count}&start={start}')
            page_content = json.loads(page.content)

            if page_content["results_html"]:
                content += page_content["results_html"]

            start = page_content["start"] + count

            if page_content.get("total_count"):
                total_count = page_content["total_count"]

            progress.update(task, total=total_count, completed=min(start, total_count))

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
            market_transaction = MarketTransaction(
                game_name=game_name,
                item_name=item_name,
                listed_date=listed_date,
                price=price,
                gain_or_loss=gain_or_loss,
                image_url=image_url,
            )
            market_transactions.append(market_transaction)

    return market_transactions

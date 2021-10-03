# Build-in modules
import sys
import logging
import json
import math
import csv
import re
import os
from decimal import Decimal
import pickle
from datetime import datetime

# Pipenv modules
import webbrowser
import steam.webauth as wa
from bs4 import BeautifulSoup
from jinja2 import Template, select_autoescape
import typer

# Logging configuration
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s %(levelname)s %(message)s'
)

# Global variables
TARGET = None
CACHE = None

# Global variables
market_transactions = None

if CACHE:
    try:
        with open('market_transactions.pkl', 'rb') as temp_file:
            market_transactions = pickle.load(temp_file)
    except FileNotFoundError:
        pass


def auth_steam():
    """
    Login to Steam via CLI and returns the authenticated websession
    """
    print("Login to your Steam Account:")
    username = str(input("Enter username: ")).strip()
    session = wa.WebAuth(username).cli_login()
    return session


def fetch_market_history():
    """
    Fetching market history from Steam with the session created by auth_steam() and returns an array containing all market listings
    """

    steam_session = auth_steam()

    # Initialize content objects for storing the market history from Steam
    content = ""
    market_transactions = []

    # Calculate the number of requests to get all data (pagination!)
    page = steam_session.get('https://steamcommunity.com/market/myhistory/render/?count=500&start=0')
    transaction_count = json.loads(page.content)["total_count"]
    query_count = math.ceil(transaction_count / 500)
    logging.info(f"Total Transactions: {str(transaction_count)} - Sending {str(query_count)} requests...")

    # Fetch market history from Steam with multiple requests
    try:
        for i in range(query_count):
            url = f'https://steamcommunity.com/market/myhistory/render/?count=500&start={str(i * 500)}'
            logging.info(f"({str(i+1)}) HTTP GET: {url}")
            content += json.loads((steam_session.get(url).content).decode("utf-8-sig"))["results_html"]
        logging.info("Fetching Data from Steam successful")
    except:
        logging.exception("Unexpected error")
        raise SystemExit()

    # Pulling content out of theHTML Response with the BeautifulSoup library
    DOMdocument = BeautifulSoup(content, 'html.parser')
    market_listing_rows = DOMdocument.find_all("div", class_="market_listing_row")

    for row in market_listing_rows:
        # Extract data from DOM
        market_listing_price = row.find("span", class_="market_listing_price").text.strip()
        market_listing_item_name = row.find("span", class_="market_listing_item_name").text.strip()
        market_listing_game_name = row.find("span", class_="market_listing_game_name").text.strip()
        market_listing_gainorloss = row.find("div", class_="market_listing_gainorloss").text.strip()
        market_listing_listed_date = row.find("div", class_="market_listing_listed_date").text.strip()
        market_listing_item_img = row.find("img", class_="market_listing_item_img")["src"]

        # Format data
        if (re.search(r"^\d+,(\d|-){2}€$", market_listing_price)):
            market_listing_price = Decimal(market_listing_price.replace(
                ",--", ".00").replace(",", ".").replace("€", ""))

        if (re.search(r"^\d{1,2} \w{3}$", market_listing_listed_date)):
            market_listing_listed_date = datetime \
                .strptime(f"2020 {market_listing_listed_date}", "%Y %d %b") \
                .strftime("%d.%m")

        # Format original steam data (market_listing_row) and add it to an additional array (market_transactions)
        if market_listing_gainorloss in ["+", "-"]:
            market_transactions.append({
                "game_name": market_listing_game_name,
                "item_name": market_listing_item_name,
                "listed_date": market_listing_listed_date,
                "price": market_listing_price,
                "gainorloss": market_listing_gainorloss,
                "image_url": market_listing_item_img,
            })

    if CACHE:
        with open('market_transactions.pkl', 'wb') as temp_file:
            pickle.dump(market_transactions, temp_file)

    return market_transactions


def generate_csv():
    global market_transactions
    if market_transactions is None:
        market_transactions = fetch_market_history()

    # Create output directory if it doesn't exist
    if not os.path.exists(TARGET):
        os.mkdir(TARGET)

    # Save the market listings to a CSV-File
    if (len(market_transactions) > 0):
        logging.info("Creating CSV-File ...")
        with open(f'{TARGET}/market-history.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(market_transactions[0].keys())
            writer.writerows([x.values() for x in market_transactions])
            logging.info(f"CSV-File created successfully: {os.path.realpath(file.name)}")


def generate_html():
    global market_transactions
    if market_transactions is None:
        market_transactions = fetch_market_history()

    if (len(market_transactions) > 0):
        with open('./templates/index.html', encoding="utf-8") as template_file:
            template = Template(template_file.read(), autoescape=select_autoescape())

        with open('market-history.html', 'w', encoding="utf-8") as rendered_file:
            current_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            summary = {
                "totalTransactions": len(market_transactions)
            }
            rendered_file.write(template.render(
                summary=summary, transactions=market_transactions, current_date=current_date))

        # Opening default web browser to view the html file
        webbrowser.open('file://' + os.path.abspath("market-history.html"))
    else:
        logging.warning("Steam Market History is empty!")


def main(
    csv_enable: bool = typer.Option(False, "--csv", help="Generate steam market history as csv file"),
    html_enable: bool = typer.Option(False, "--html", help="Generate steam market history as interactive website"),
    target: str = typer.Option('./data', help="Relative path based on script location for generated files"),
    cache: bool = typer.Option(False, help="Cache steam credentials. Use with caution!")
):
    # Set global variables
    global CACHE, TARGET
    CACHE = cache
    TARGET = target

    if csv_enable:
        generate_csv()

    if html_enable:
        generate_html()

    if not any([csv_enable, html_enable]):
        logging.warning("Please provide at least one option! For more information call 'generate.py --help'")


if __name__ == "__main__":
    typer.run(main)

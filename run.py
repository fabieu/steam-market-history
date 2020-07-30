import steam.webauth as wa #pip install steam
from bs4 import BeautifulSoup #pip install beautifulsoup4
import pandas as pd #pip install pandas
import json
import math
import sys
import subprocess
import csv
import webbrowser
import time
from datetime import datetime

# Check if required Pythons modules are installed, if not install them via pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print("Installing required dependencies ...")
install("beautifulsoup4")
install("steam")
install("pandas")

#Initialize data object for storing the fetched data from Steam
data = ""

# Login to Steam via cli_login - all login steps can be easily performed via the console
print("Log in to Steam ...")
session = wa.WebAuth(str(input("Enter username: "))).cli_login()

#Fetching data from Steam with the session created by the login process
page = session.get('https://steamcommunity.com/market/myhistory/render/?count=500&start=0')
transaction_count = json.loads(page.content)["total_count"] #Number of total transactions - needed to calculate how many requests need to be send (Pagination!)
queries = math.ceil(transaction_count / 500) # Calculated number of queries
print("Total Transactions: " + str(transaction_count) + " - Sending " + str(queries) + " requests ...")

# Fetch data from Steam with multiple requests (count calculated earlier)
try:
    for i in range(queries):
        url = 'https://steamcommunity.com/market/myhistory/render/?count=500&start=' + str(i * 500)
        print (str(i+1) + ": Get " + url)
        data += json.loads(session.get(url).content)["results_html"] #Filter all relevant informations from the resutls_html property
    print("Fetching Data from Steam successful")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

#Manipulating data from the response with the BeautifulSoup Libary and save it in CSV-Format
print("Creating CSV-File ...")
with open('data.csv', 'w', newline='',encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows([["Gain or loss","Date", "Item Name", "Game Name", "Price €"]])
    
    #Pulling data out of HTML Response with the BeautifulSoup Libary
    soup = BeautifulSoup(data, 'html.parser')
    market_listing_rows = soup.find_all("div",class_="market_listing_row")

    for i in market_listing_rows:
        market_listing_price = i.find("span",class_="market_listing_price").text.strip()
        market_listing_price = market_listing_price.replace(",--",".00").replace(",",".").replace("€","")
        market_listing_item_name = i.find("span",class_="market_listing_item_name").text.strip()
        market_listing_game_name = i.find("span",class_="market_listing_game_name").text.strip()
        market_listing_gainorloss = i.find("div",class_="market_listing_gainorloss").text.strip()
        market_listing_listed_date = i.find("div",class_="market_listing_listed_date").text.strip()
        #market_listing_item_img = i.find("img",class_="market_listing_item_img")["src"]
        if market_listing_gainorloss == "+":
            item = ["Bought",market_listing_listed_date, market_listing_item_name, market_listing_game_name, market_listing_price]
            writer.writerows([item])
        elif market_listing_gainorloss == "-":
            item = ["Sold",market_listing_listed_date, market_listing_item_name, market_listing_game_name, market_listing_price]
            writer.writerows([item])
        else:
            pass
    print("File successfully created!")

# Read the csv file in
df = pd.read_csv('data.csv')

# Assign to string
htmlTable = df.to_html(na_rep='-', justify='center',table_id='data')

# Write html file to view the data from the csv file
# Import necessary libaries and other config files
with open('view.html', 'w',encoding="utf-8") as file:
    file.write(" \
        <head> \
        <link rel='stylesheet' type='text/css' href='libary/view.css'> \
        <script src='libary/tablefilter/tablefilter.js'></script> \
        <title>Market History: " + datetime.now().strftime("%d.%m.%Y - %H:%M") + "</title> \
        </head> \
    ")
    file.write(htmlTable)
    file.write("<div id='loader'></div>")
    file.write("<script src='libary/tablefilter/config.js'></script>")

#Opening default web browser to view the html file
print("Opening default web browser to view the results ...")
webbrowser.open('view.html', new=2)

#Wait 5 seconds and then close the terminal
print("Programm Sequence finished - Closing Command Prompt in 5 Seconds")
for i in range(5,0,-1):
    time.sleep(1)
    print("Terminal automatically closing in " + str(i) + " seconds")
exit()
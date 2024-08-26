import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs

# URL to scrape
url = "https://www.buscalibre.pe/libros/search/?q="

# Search the topic you prefer
user_input = input("What topic/author are you interested in?: ")

url_final = url + user_input

response = requests.get(url_final)
soup = bs(response.text, "html.parser")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

response = requests.get(url_final, headers=headers)

# Verify an OK response
if response.status_code == 200:
    soup = bs(response.text, "html.parser")
    print(f"You have searched for the topic {user_input}")  # Imprime el HTML de manera legible
else:
    print(f"Error {response.status_code}: No access to the website")

titles = []
prices_before = []
prices_now = []
discounts = []

for objeto in soup.find_all("div", class_="box-producto"):
    title = objeto.find("h3").text.strip()
    price_before = objeto.find("p", class_="precio-antes").text.strip()
    price_before = price_before.replace("S/  ", "")
    price_before = price_before.replace(",", ".")
    price_before = float(price_before)
    price_now = objeto.find("p", class_="precio-ahora").text.strip()
    price_now = price_now.replace("S/  ", "")
    price_now = price_now.replace(",", ".")
    price_now = float(price_now)

    discount = round((price_before - price_now) / price_before * 100, 2)
    
    titles.append(title)
    prices_before.append(price_before)
    prices_now.append(price_now)
    discounts.append(discount)

df = pd.DataFrame({
    "Title" : titles,
    "Prices before" : prices_before,
    "Prices now" : prices_now,
    "Discount" : discounts
})

# Get the book with the minimum price
min_price_book = df[df['Prices now'] == df['Prices now'].min()]

# Get the book with the maximum discount
max_discount_book = df[df['Discount'] == df['Discount'].max()]

# Print the data
print(f"The book with the minimum price is {min_price_book.iloc[0, 0]} with a cost of S/{min_price_book.iloc[0, 2]}")
print(f"The book with the maximum discount is {max_discount_book.iloc[0, 0]} with a discount of {max_discount_book.iloc[0, 3]}% and a cost of S/{max_discount_book.iloc[0, 2]}")
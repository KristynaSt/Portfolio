"""
Scrapes all <title> on a URL - provided by user input.
"""

import requests
from bs4 import BeautifulSoup

url = input("Zadej URL: ")

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("title")

for t in titles:
    print(t.text)
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
from requests_html import HTMLSession


"""
    Get all quote of SET market and save to file `STOCK_FILE_INPUT`
"""
def get_set_quote():
    prefix_market = "bkk"
    url = "https://www.set.or.th/en/market/get-quote/stock/"
    session = HTMLSession()
    resp = session.get(url)
    resp.html.render()
    soup = BeautifulSoup(resp.html.html, features='html.parser')
    quotes = list(map(lambda x: x.getText().strip(),
                      soup.find_all('li', {'class': 'tag-dropdown-item title-font-family fs-18px py-1 px-2'})))
    last_symbol = os.getenv("LAST_SET_SYMBOL")
    quotes = quotes[:quotes.index(last_symbol) + 1]
    with open(os.getenv("STOCK_FILE_INPUT"), 'w+', encoding='utf-8') as f:
        for q in tqdm(quotes):
            f.write(f"{prefix_market}:{q.lower()}\n")
        f.close()

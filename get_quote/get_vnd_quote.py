from dotenv import load_dotenv
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import logging

from requests_html import HTMLSession

"""
    Get all quote of VND market and save to file `STOCK_FILE_INPUT`
"""


def get_vnd_quote():
    load_dotenv()
    prefix_market = "vnm"
    base_url = "https://www.investing.com/stock-screener/?sp=country::178|sector::a|industry::a|equityType::a|exchange::a%3Ceq_market_cap;"

    quotes = []

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    # try render page 1 by 1 till get error (page end)
    try:
        for page_no in tqdm(range(1,30)):
            for _ in range(5): # retry 5 times before give up
                try:
                    url = base_url + str(page_no)
                    session = HTMLSession()
                    resp = session.get(url)
                    resp.html.render()
                    soup = BeautifulSoup(resp.html.html, features='html.parser')
                    quote_page = list(map(lambda x: x.getText().strip(), soup.find_all('td', {'data-column-name': 'viewData.symbol'})))
                    quotes += quote_page
                except Exception:
                    continue
                break
    except Exception:
        logging.info(f"Done of process get {len(quotes)} quotes the ending page is {page_no}")

    quotes = list(set(quotes))
    # save all quote to file
    with open(os.getenv("STOCK_FILE_INPUT"), 'w+', encoding='utf-8') as f:
        for q in tqdm(quotes):
            f.write(f"{prefix_market}:{q.lower()}\n")
        f.close()

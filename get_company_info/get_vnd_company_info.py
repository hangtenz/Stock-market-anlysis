import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from tqdm import tqdm
import logging
import os
from dotenv import load_dotenv
from internal.helper import Helper

"""
    Get all company information from interesting stock of file `file/VND-interesting-lists.txt`
"""


def get_vnd_company_info():
    market = "VND"
    interesting_stock_file = Helper.get_file_interesting_list(market)
    interesting_stocks = list(map(lambda x: x.split(":")[1], interesting_stock_file.read().split('\n')[:-1]))
    interesting_stock_file.close()
    base_url = "https://www.jitta.com/stock/vnm"

    data = {}
    data['Quote'] = []
    data['Company name'] = []
    data['Company info'] = []
    writer = Helper.get_file_company_info(market)
    for stock in tqdm(interesting_stocks):
        url = f"{base_url}:{stock}"
        for retry_time in range(3): # retry 3 times before give up
            try:
                session = HTMLSession()
                resp = session.get(url)
                resp.html.render()
                soup = BeautifulSoup(resp.html.html, features='html.parser')
                company_name = soup.find_all('h3', {'class': 'Heading-sc-1wavirx-2 SubHeaderCommons__StockCompanyName-sc-10o5l1f-5 gOrGKC'})[0].getText()
                company_info = soup.find_all('div', {'class': 'Text-dn2wcp-1 dvNfdY'})[0].getText()
                data['Quote'].append(stock)
                data['Company name'].append(company_name)
                data['Company info'].append(company_info)
            except Exception:
                logging.warning(f"Cannot find information for {stock}")
                continue
            break
    pd_data = pd.DataFrame.from_dict(data)
    pd_data.to_excel(writer, sheet_name='Company Information', startrow=0, startcol=0, index = False)
    writer.close()

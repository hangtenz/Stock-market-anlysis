import os

import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from tqdm import tqdm
import logging
import os


"""
    Get all company information from interesting stock of file `file/SET-stocks.txt`
"""
if __name__ == "__main__":
    os.chdir('../')
    interesting_stock_file = open(os.getenv(""), 'r',  encoding='utf-8')
    interesting_stocks = interesting_stock_file.read().split('\n')[:-1]
    interesting_stock_file.close()

    data = {}
    data['Quote'] = []
    data['Company name'] = []
    data['Company info'] = []

    with pd.ExcelWriter('../file/stock-output/interesting-company_info.xlsx', engine="xlsxwriter") as writer:
        for stock in tqdm(interesting_stocks):
            url = f"https://www.set.or.th/th/market/product/stock/quote/{stock}/company-profile/information"
            for _ in range(3): # retry 3 times before give up
                try:
                    session = HTMLSession()
                    resp = session.get(url)
                    resp.html.render()
                    soup = BeautifulSoup(resp.html.html, features='html.parser')
                    company_name = soup.find_all('h2', {'class': 'mb-0 me-2'})[0].getText().strip()
                    company_info = soup.find_all('span', {'class': 'mb-3'})[0].getText().strip()
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
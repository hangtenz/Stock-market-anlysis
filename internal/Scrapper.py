from pandas import DataFrame
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

"""
    get the stock name and return DataFrame information 
"""
def scrapper(stock_name: str) -> DataFrame:
    base_url = "https://www.jitta.com/stock/{}/factsheet"
    url = base_url.format(stock_name)
    cookies = {'JDCID': os.getenv('JC_CID')}
    result = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(result.text, features='html.parser')
    data = {}
    row_years = list(map(lambda x: x.getText(), soup.find_all('div', {
        'class': 'Text__TextSM-dn2wcp-2 FactsheetTableHeader__FlexItem-efsh34-3 fbxBgM'})))
    row_names = list(map(lambda x: x.getText(), soup.find_all('div', {
        'style': 'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:8px'})))
    row_datas = list(map(lambda x: x.getText(),
                         soup.find_all('span', {'class': 'FactsheetTableRow__TooltipWrapper-sc-1wziwtk-6 bMjxnb'})))
    chunk_size = len(row_years)
    for idx, row_name in enumerate(row_names):
        data[row_name] = []
        for i in range(idx * chunk_size, (idx + 1) * (chunk_size)):
            data[row_name].append(row_datas[i])
    pd_data = pd.DataFrame(data)
    pd_data.index = row_years
    return pd_data

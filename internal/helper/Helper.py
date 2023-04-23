from typing import TextIO
import pandas as pd
from pandas import ExcelWriter


def get_file_stock_input(market: str, mode='r') -> TextIO:
    return open(f"file/stock-input/{market}-stocks.txt", mode, encoding='utf-8')


def get_file_summary(market: str) -> ExcelWriter:
    return pd.ExcelWriter(f"file/stock-output/summary/{market}-market-summary.xlsx", engine="xlsxwriter")


def get_file_cannot_process(market: str) -> TextIO:
    return open(f'file/stock-output/cannot-process/cannot-process-{market}-list.txt', 'w+', encoding='utf-8')

def get_file_interesting_list(market, mode='r') -> TextIO:
    return open(f"file/stock-output/interesting-stock/{market}/{market}-interesting-lists.txt", mode, encoding='utf-8')


def get_file_company_info(market) -> ExcelWriter:
    return pd.ExcelWriter(f"file/stock-output/interesting-stock/{market}/{market}-interesting-company-info.xlsx", engine="xlsxwriter")

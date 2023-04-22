import os

from dotenv import load_dotenv
import pandas as pd
from internal.Scrapper import scrapper
from internal.Calculate import calculate
from internal.excelhandler.excelhandler import save_data_to_excel
from tqdm import tqdm

"""
    Read stock list in file `STOCK_FILE_INPUT`
"""
if __name__ == "__main__":
    load_dotenv()
    market_name = os.getenv("STOCK_FILE_INPUT").split("/")[-1].split("-")[0]

    # read stock
    stock_list = []
    with open(os.getenv("STOCK_FILE_INPUT"), 'r', encoding='utf-8') as f:
        stock_list = f.read().split('\n')[:-1]
        f.close()

    interesting_stock = set()
    # list of file to stock log of stock which cannot process
    cannot_process_list = open(f'file/stock-output/cannot-process-{market_name}-list.txt', 'w+', encoding='utf-8')

    # find information data
    writer = pd.ExcelWriter(f'file/xlsx/{market_name}-market.xlsx', engine="xlsxwriter")
    for stock in tqdm(stock_list):
        sheet_name = stock.split(':')[1]
        try:
            pd_data = scrapper(stock)
            pd_data = calculate(pd_data)
            save_data_to_excel(pd_data, writer, sheet_name, interesting_stock)
        except Exception:
            cannot_process_list.write(stock + "\n")
    writer.close()
    cannot_process_list.close()

    # write the list of interesting stock
    with open(f'file/stock-output/{market_name}-interesting_stock.txt', 'w', encoding='utf-8') as f:
        for stock in interesting_stock:
            f.write(stock + "\n")
        f.close()

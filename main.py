import os

from dotenv import load_dotenv
from internal.Scrapper import scrapper
from internal.Calculate import calculate
from internal.excelhandler.excelhandler import save_data_to_excel
from tqdm import tqdm
from internal.helper import Helper
from get_quote.get_quote import get_quote
from get_company_info.get_company_info import get_company_info

"""
    Read stock list in file `STOCK_FILE_INPUT`, summary then evaluation
"""
if __name__ == "__main__":
    load_dotenv()
    market = os.getenv("MARKET")

    refresh_stock_input = os.getenv("REFRESH_STOCK_INPUT").lower() == "true"

    if refresh_stock_input:
        print(f"refresh quote stock input for market {market}")
        get_quote()

    # read stock
    f = Helper.get_file_stock_input(market)
    stock_list = f.read().split('\n')[:-1]
    f.close()

    interesting_stock = set()
    # list of file to stock log of stock which cannot process
    cannot_process_list = Helper.get_file_cannot_process(market)

    # find information data
    writer = Helper.get_file_summary(market)
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
    f = Helper.get_file_interesting_list(market, mode='w')
    for stock in interesting_stock:
        f.write(stock + "\n")
    f.close()

    get_company_info()
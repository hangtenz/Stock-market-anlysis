import os
from dotenv import load_dotenv
from get_set_quote import get_set_quote
from get_vnd_quote import get_vnd_quote

"""
    Get all quote of SET market and save to file `STOCK_FILE_INPUT`
"""
if __name__ == "__main__":
    os.chdir('../')
    load_dotenv()
    market_name = os.getenv("STOCK_FILE_INPUT").split("/")[-1].split("-")[0]

    if market_name == "SET":
        get_set_quote()
    elif market_name == "VND":
        get_vnd_quote()
    else:
        raise Exception("Not have this market")
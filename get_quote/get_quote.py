import os
from get_quote.get_set_quote import get_set_quote
from get_quote.get_vnd_quote import get_vnd_quote

"""
    Get all quote of SET market and save to file `STOCK_FILE_INPUT`
"""
def get_quote():
    market_name = os.getenv("MARKET")

    if market_name == "SET":
        get_set_quote()
    elif market_name == "VND":
        get_vnd_quote()
    else:
        raise Exception("Not have this market")
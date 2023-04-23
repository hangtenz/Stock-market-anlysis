import os
from get_company_info.get_set_company_info import get_set_company_info
from get_company_info.get_vnd_company_info import get_vnd_company_info

def get_company_info():
    market_name = os.getenv("MARKET")

    if market_name == "SET":
        get_set_company_info()
    elif market_name == "VND":
        get_vnd_company_info()
    else:
        raise Exception("Not have this market")
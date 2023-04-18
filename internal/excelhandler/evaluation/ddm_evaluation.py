from pandas import DataFrame, ExcelWriter
from internal.excelhandler.helper.helper import split_session
from internal.settings.settings import last_year, current_year
from internal.excelhandler.helper.helper import write_dict_data
import math


def ddm_evaluation(ddm_data: DataFrame,writer: ExcelWriter, workbook: ExcelWriter, worksheet: ExcelWriter, sheet_name: str, interesting_stock: set, marking: bool = True):
    row_start = 88
    split_session(row_start, workbook, worksheet, 'DDM evaluation')
    ddm_data.to_excel(writer, sheet_name=sheet_name, startrow=row_start + 3, startcol=1)

    dividend = ddm_data.loc['เงินปันผลต่อหุ้น', last_year]
    # not get stable dividend, not evaluate with DDM
    if math.isnan(dividend):
        return

    expected_return = 0.1
    growth_rate = 0.03
    price_to_buy = (dividend * (1 + growth_rate)) / (expected_return - growth_rate)
    current_price = ddm_data.loc['ราคา', current_year]

    # cannot find price right now, cannot decide it's a cheap stock or not
    if math.isnan(current_price):
        return

    data_write = {
        'Dividend': dividend,
        'Expected Return': expected_return,
        'Growth Rate': growth_rate,
        'Price to Buy': price_to_buy,
        'Current Price': current_price
    }
    write_dict_data(97, data_write, worksheet)

    if marking:
        # highlight the sheet if it's cheap stock
        if current_price <= price_to_buy:
            interesting_stock.add(sheet_name)
            worksheet.set_tab_color('pink')
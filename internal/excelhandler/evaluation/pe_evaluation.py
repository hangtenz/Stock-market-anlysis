from pandas import DataFrame, ExcelWriter
from internal.excelhandler.helper.helper import split_session
from internal.settings.settings import last_year, current_year
from internal.excelhandler.helper.helper import filter_not_process, write_dict_data
import math


def pe_evaluation(pe_data:DataFrame,writer: ExcelWriter, workbook: ExcelWriter, worksheet: ExcelWriter, sheet_name: str, interesting_stock: set, marking: bool = True):
    row_start = 73
    split_session(row_start,workbook,worksheet,'P/E evaluation')

    expected_earning = pe_data.loc['กำไรต่อหุ้น', last_year]
    pe_data.to_excel(writer, sheet_name=sheet_name, startrow=row_start + 3, startcol=1)

    # not process if don't have enough P/E data or cannot get earning from last year
    if filter_not_process(pe_data, 'อัตราส่วนราคาต่อกำไร') or math.isnan(expected_earning):
        return

    pe = list(pe_data.loc['อัตราส่วนราคาต่อกำไร', :].dropna())
    assert_msg = f"P/E data for {sheet_name} is not enough"
    assert len(pe) >= 5, assert_msg

    pe_sum = sum(pe) - max(pe) - min(pe)
    avg_pe = pe_sum / len(pe) - 2
    fair_price = expected_earning * avg_pe
    mos30_price = 0.7 * fair_price
    current_price = pe_data.loc['ราคา', current_year]

    # cannot find price right now, cannot decide it's a cheap stock or not
    if math.isnan(current_price):
        return

    data_write = {
        'AVG P/E': avg_pe,
        'Fair Price': fair_price,
        'MOS 30 Price': mos30_price,
        'Current price': current_price
    }
    write_dict_data(83, data_write, worksheet)

    if marking:
        # highlight the sheet if it's cheap stock
        if current_price <= mos30_price:
            interesting_stock.add(f"pe:{sheet_name}")
            worksheet.set_tab_color('green')
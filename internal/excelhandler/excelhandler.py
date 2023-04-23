import os

from pandas import DataFrame, ExcelWriter
from internal.excelhandler.plotting.plotfinancedata import plot_finance_data
from internal.excelhandler.evaluation.pe_evaluation import pe_evaluation
from internal.excelhandler.evaluation.ddm_evaluation import ddm_evaluation

"""
    Main function: plot, evaluate and save to excel
"""


def save_data_to_excel(pd_data: DataFrame, writer: ExcelWriter, sheet_name: str, interesting_stock: set):
    pd_data.to_excel(writer, sheet_name=sheet_name)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    mark_pe = os.getenv("MARK_PE").lower() == "true"
    mark_ddm = os.getenv("MARK_DDM").lower() == "true"
    plot_finance_data(pd_data, writer, workbook, worksheet, sheet_name)
    pe_evaluation(pd_data.loc[:, ['อัตราส่วนราคาต่อกำไร', 'กำไรต่อหุ้น', 'ราคา']].T, writer, workbook, worksheet,
                  sheet_name, interesting_stock, marking=mark_pe)
    ddm_evaluation(pd_data.loc[:, ['เงินปันผลต่อหุ้น', 'ราคา']].T, writer, workbook, worksheet, sheet_name,
                   interesting_stock, marking=mark_ddm)

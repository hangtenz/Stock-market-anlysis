from pandas import DataFrame
import pandas as pd

"""
    clean, calculate and filter data then return back
"""
def calculate(pd_data: DataFrame) -> DataFrame:
    # clean
    for column in pd_data.columns:
        pd_data[column] = pd_data[column].str.replace(',', '').str.replace('%', '')
        pd_data[column] = pd.to_numeric(pd_data[column], errors='coerce')
    # calculate
    pd_data.loc[:, 'อัตราค่าใช้จ่ายในการขายและบริหาร'] = pd_data.loc[:,'ค่าใช้จ่ายในการขายและบริหาร'] * 100 / pd_data.loc[:,'รายได้รวม']
    # filter
    interesting_columns = [
        'รายได้รวม',
        'กำไรต่อหุ้น',
        'อัตรากำไรขั้นต้น',
        'อัตราค่าใช้จ่ายในการขายและบริหาร',
        'หนี้สินระยะยาว',
        'หนี้สินต่อส่วนของผู้ถือหุ้น',
        'อัตราผลตอบแทนผู้ถือหุ้น',
        'อัตราการจ่ายเงินปันผล',
        'อัตราส่วนราคาต่อกำไร',
        'ราคา',
        'เงินปันผลต่อหุ้น'
    ]
    pd_data.index.name = 'ปี'
    pd_data = pd_data[interesting_columns]
    return pd_data
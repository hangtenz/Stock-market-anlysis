from pandas import DataFrame, ExcelWriter
import string



column_mapping = list(string.ascii_uppercase) + list(map(lambda x: 'A'+x, string.ascii_uppercase))
# helper function to fill red color for separate
def split_session(row_separate:int, workbook: ExcelWriter, worksheet: ExcelWriter, session_name: str):
    format = workbook.add_format()
    format.set_pattern(1)
    format.set_bg_color('red')
    for column in column_mapping:
        worksheet.write(f'{column}{row_separate}', '',format)
    worksheet.write(f'A{row_separate+1}', session_name)


# helper function to write dict data to Excel
def write_dict_data(current_row: int, data_write: dict, worksheet: ExcelWriter):
    #print(data_write)
    for k, v in data_write.items():
        worksheet.write(f'B{current_row}', k)
        worksheet.write(f'C{current_row}', v)
        current_row += 1

def filter_not_process(data: DataFrame, column: str):
    if len(data.loc[column,:].dropna()) < 5:
        return True
    return False



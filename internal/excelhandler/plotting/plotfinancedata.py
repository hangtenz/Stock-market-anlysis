from pandas import DataFrame, ExcelWriter
from internal.excelhandler.helper.helper import split_session
from internal.settings.settings import bar_chart,line_chart,no_plot_chart, column_mapping


"""
    Plot graph for financial statement
"""
def plot_finance_data(pd_data:DataFrame,writer: ExcelWriter, workbook: ExcelWriter, worksheet: ExcelWriter, sheet_name: str):
    split_session(16, workbook, worksheet, 'Financial Data')
    # column and row offset for each graph
    column_offset, row_offset = 10, 17
    # keep track position of right now of each graph
    start_column = 1
    column_position, row_position = start_column, 20
    # limit col for the graph to not have graph too much on right side
    limit_col = 26
    # start-end row of the data to plot
    start_row, end_row = 1,len(pd_data)
    for column in pd_data.columns:
        col_x = 0
        col_y = pd_data.columns.get_loc(column) + 1
        chart = None
        if column in bar_chart:
            chart = workbook.add_chart({'type': 'column'})
        elif column in line_chart:
            chart = workbook.add_chart({'type': 'line'})
        elif column in no_plot_chart:
            continue
        else:
            raise Exception('cannot decide which graph should show')

        chart.add_series({
            'categories': [sheet_name, start_row, col_x, end_row, col_x],  # ปี
            'values': [sheet_name, start_row, col_y, end_row, col_y],  # data
        })
        # Configure the chart axes.
        chart.set_x_axis({'name': 'ปี', 'position_axis': 'on_tick'})
        chart.set_y_axis({'name': column, 'major_gridlines': {'visible': True}})
        # Turn off chart legend. It is on by default in Excel.
        chart.set_legend({'position': 'off'})
        chart.set_title({'name': f'{column}'})

        # Insert the chart into the worksheet.
        worksheet.insert_chart(f'{column_mapping[column_position]}{row_position}', chart)

        # shift for next graph
        column_position += column_offset
        if column_position >= limit_col:
            column_position = start_column
            row_position += row_offset
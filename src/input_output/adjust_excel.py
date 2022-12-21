import pandas as pd


def adjust_excel(filepath: str, df):
    writer = pd.ExcelWriter(filepath)
    df.to_excel(writer, sheet_name='Plan', index=False, na_rep='NaN')

    for column in df:
        column_length = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['Plan'].set_column(col_idx, col_idx, column_length)

    writer.close()
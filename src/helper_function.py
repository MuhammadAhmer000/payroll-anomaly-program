# import statements
import pandas as pd
import logging

# preamble
logger = logging.getLogger(__name__)


def split_df(employee_dataframe):
    """
    :param employee_dataframe: payroll dataframe grouped by employee
    :return: a tuple, the "historic dataset" and the latest dataset, respectively.
    """
    logger.debug(f"Splitting dataframe into history and latest record")
    return employee_dataframe.iloc[:-1], employee_dataframe.iloc[-1:]


def normalize_column_names(columns: pd.Index) -> pd.Index:
    """
    :param columns: dataframe columns (DataFrame.columns)
    :return: normalized column names
    """
    return (columns.str.lower()
                   .str.replace(' ', '_', regex=False)
                   .str.replace('(', '', regex=False)
                   .str.replace(')', '', regex=False))


def split_sort_employee(df, emp_col, month_col):
    if emp_col in df.columns:
        emp_groups = df.groupby(emp_col)
    else:
        emp_groups = [(emp_col, df)]

    # Sort each employee’s df
    for emp_id, emp_df in emp_groups:
        yield emp_id, emp_df.sort_values(month_col)
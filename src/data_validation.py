# import statements
import logging
from pathlib import Path
import pandas as pd


# preamble
logger = logging.getLogger(__name__)

# To-Do List
# TODO: make a helper function that returns or keeps data at one central position.
# TODO: make nullable, and acceptable value data validation
# TODO: make logging diagnostic tables
# TODO: learn more pandas methods and techniques


def column_verification(dataframe, file_path: str = Path(__file__).parent.parent / "data/other/column_schema.xlsx"):
    """
    Helper Function: Checks using another file "mandatory_columns" to ensure that the dataframe has the appropriate
    columns. Assumes that the columns are unordered, but that the names are exactly the same.

    :param dataframe:
    :param file_path:
    :return:
    """

    column_df = pd.read_excel(file_path)
    column_rows = list(column_df["column_name"])
    columns_missing = [required_column for required_column in column_rows
                       if required_column not in dataframe.columns]

    return columns_missing


def is_duplicate(dataframe):
    counts = dataframe.groupby(["month", "employee_id"])["employee_id"].transform("size")
    return list(dataframe[counts > 1].index)


def data_verification(dataframe):
    logger.info("Starting data verification process")
    if dataframe.empty:
        logger.error("Payroll file is empty or doesn't exist")
        raise ValueError(f"Payroll file is empty or doesn't exist")
    missing_cols = column_verification(dataframe)
    if len(missing_cols) > 0:
        logger.error(f"The following payroll columns are missing or have an error: {missing_cols}")
        raise ValueError(f"The following payroll columns are missing or have an error: ", missing_cols)
    duplicate_cols = is_duplicate(dataframe)
    if len(duplicate_cols) > 0:
        logger.warning(f"The payroll has several duplicate values at: {duplicate_cols}")
        raise ValueError(f"The payroll has several duplicate values at: ", duplicate_cols)

    logger.info(f"Payroll file loaded successfully: {dataframe.shape[0]} rows, {dataframe.shape[1]} columns")
    print(f"Payroll file loaded successfully: {dataframe.shape[0]} rows, {dataframe.shape[1]} columns")

    return True

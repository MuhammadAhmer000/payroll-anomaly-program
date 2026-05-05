# import statements
import logging

import pandas as pd
import logging
from src.helper_function import normalize_column_names
from pathlib import Path

# preamble
logger = logging.getLogger(__name__)

# TODO: Make two test cases: missing file, empty file, and missing columns
# TODO: Organize the imports properly
# TODO: Type-checking columns
# TODO: Develop this to SQL eventually, perhaps make it an option.


def validate_excel(input_file: str):

    file_path = Path(input_file)

    # Check: is the file missing?
    if not file_path.exists():
        print(f"Payroll file not found at {file_path.resolve()}")
        logger.exception(f"Payroll file not found at {file_path.resolve()}")
        return False
    # Check: is the file in .xlsx format
    if file_path.suffix != "xlsx":
        print(f"Payroll file must be in type 'xlsx'. Currently the type is {file_path.suffix}")
        logger.exception(f"Payroll file not found at {file_path.resolve()}")
        return False

    return True


def load_payroll(file_path: str):

    # TODO: required imports: from src.helper_function import normalize_column_names

    # validate non-content-based features (i.e. file-missing)
    validate_excel(file_path)

    # importing excel file to pandas dataframe
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read payroll Excel file: {e}")

    # normalizing column names (if not done already)
    df.columns = normalize_column_names(df.columns)

    return df



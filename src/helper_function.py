# import statements
import pandas as pd

def normalize_column_names(columns: pd.Index) -> pd.Index:
    """
    :param columns: dataframe columns (DataFrame.columns)
    :return: normalized column names
    """
    return (columns.str.lower()
                   .str.replace(' ', '_', regex=False)
                   .str.replace('(', '', regex=False)
                   .str.replace(')', '', regex=False))
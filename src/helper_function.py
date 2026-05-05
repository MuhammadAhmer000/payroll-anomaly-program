# import statements
import pandas as pd

def normalize_column_names(dataframe: pd.DataFrame.columns):
    """
    :param dataframe: dataframe columns; specifically DatFrame.columns
    :return: normalized version of the dataframe column names
    """
    return dataframe.columns.str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

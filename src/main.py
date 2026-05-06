# import statements
import logging
import pandas as pd

from src.config_loader import set_config
from src.data_ingestion import load_payroll
from src.database_ingestion import load_db_credentials
from src.database_ingestion import import_database
from src.helper_function import split_sort_employee
from src.machine_learning_testing import unsupervised_machine_learning_results, get_ensemble_results
from src.payroll_rule_testing import payroll_validation_wrapper
from src.stats_testing import compute_zscore_deviation
import logging
from pathlib import Path

# preamble
logger = logging.getLogger(__name__)


# TODO: add endpoint for /config here...
def SET_CONFIG():

    # required imports: from src.config_loader import set_config
    try:
        config = set_config()
    except EnvironmentError:
        logging.info(f"MAIN: failed to load configuration")
        print(f"MAIN: failed to load configuration")
        raise

    return config


# TODO: add endpoint for /test here...
def LOAD_PAYROLL(file_path: str):
    try:
        dataframe = load_payroll(file_path)
    except Exception as e:                                     # TODO: write better exceptions
        logging.info(f"MAIN: failed to load payroll data")
        print(f"MAIN: failed to load payroll data")
        raise

    return dataframe

def LOAD_DB_CREDENTIALS():
    db_credentials = load_db_credentials()
    return db_credentials


def IMPORT_DATABASE(db_credentials, database_name, simulate_data=False):
    dataframe = import_database(db_credentials, database_name, simulate_data)
    return dataframe

# TODO: implement this, along with querying and stuff
# def CREATE_DATABASE(db_credentials):


def PAYROLL_RULE_TESTING(dataframe, config):
    return payroll_validation_wrapper(dataframe, config)


def STATS_TESTING(dataframe, z_threshold):
    return compute_zscore_deviation(dataframe, z_threshold)


def ML_TESTING(emp_id, dataframe):
    unsupervised_results_df = unsupervised_machine_learning_results(dataframe)
    ensemble_results = []  # eventually remove this
    ensemble_df = get_ensemble_results(emp_id, unsupervised_results_df, ensemble_results)
    return unsupervised_results_df, ensemble_df


def TREND_ANALYSIS_TESTING():
    pass

def ANALYSIS_WRAPPER(DATAFRAME, EMP_COL, MONTH_COL, output_path, config):

    # with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    for emp_id, emp_df in split_sort_employee(DATAFRAME, EMP_COL, MONTH_COL):

            logger.info(f"Beginning analysis process for employee {emp_id}")


            logger.info(f"Beginning: payroll rule testing for {emp_id}")
            rule_df = PAYROLL_RULE_TESTING(DATAFRAME, config)
            # logger.info(f"payroll rule testing completed. Table: {len(rule_df)} records")
            print(rule_df)


            logger.info(f"Beginning: statistics testing for {emp_id}")
            stats_df = STATS_TESTING(DATAFRAME, config["rule_threshold"]["z_score"])
            logger.info(f"Baseline Calculated: {len(stats_df)} records")
            print(stats_df)


            logger.info(f"Beginning: machine learning testing for {emp_id}")
            ensemble_df, unsupervised_df = ML_TESTING(emp_id, DATAFRAME)
            print(unsupervised_df)
            print(ensemble_df)








    # TODO: return back each object at the end
    return None


# Note: main will eventually be left for testing, React will be the "main" frontend
# TODO: add endpoint for /test here...
def main():

    # === config loading ===
    config = SET_CONFIG()

    # === file path from config file
    # TODO: fix input_path so that it automatically appends input_path
    input_path = config["file_path"]["input"]

    output_path = str(Path(__file__).parent.parent) + '/' + config["file_path"]["output"]

    # === loading payroll (selecting excel or database)
    if config["ingestion_method"] == "excel":

        # === load excel payroll ===
        dataframe = LOAD_PAYROLL(input_path)
        print(f"dataframe: {dataframe.shape}")

    elif config["ingestion_method"] == "database":

        # === load database payroll ==
        db_credentials = LOAD_DB_CREDENTIALS().values()
        print(db_credentials)
        payroll_df = IMPORT_DATABASE(db_credentials, "PAYROLL", config["simulate_database"])
        print(payroll_df)

    else:

        # === other option
        print("invalid data ingestion method... please update in configuration.yml")
        raise

    EMP_COL, MONTH_COL = "employee_id", "month"

    # TODO: to remove the "global", add a try/except block
    ANALYSIS_WRAPPER(payroll_df, EMP_COL, MONTH_COL, output_path, config)










if __name__ == "__main__":
    main()

# import statements
import logging

from src.config_loader import set_config
from src.data_ingestion import load_payroll
from src.database_ingestion import load_db_credentials
from src.database_ingestion import import_database
import logging

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

# def CREATE_DATABASE(db_credentials):






# Note: main will eventually be left for testing, React will be the "main" frontend
# TODO: add endpoint for /test here...
def main():

    # === config loading ===
    config = SET_CONFIG()

    input_path = config["file_path"]["input"]
    output_path = config["file_path"]["output"]

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

        print("invalid data ingestion method... please update in configuration.yml")
        raise


if __name__ == "__main__":
    main()

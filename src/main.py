# import statements
import logging

from src.config_loader import set_config
from src.data_ingestion import load_payroll
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
        load_payroll(file_path)
    except Exception as e:                                     # TODO: write better exceptions
        logging.info(f"MAIN: failed to load payroll data")
        print(f"MAIN: failed to load payroll data")
        raise


# Note: main will eventually be left for testing, React will be the "main" frontend
# TODO: add endpoint for /test here...
def main():

    config = SET_CONFIG()
    LOAD_PAYROLL(config["file_path"]["input"])










if __name__ == "__main__":
    main()

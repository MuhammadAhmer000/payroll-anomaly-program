# import statements
from dotenv import dotenv_values, find_dotenv
import logging
import pandas as pd
from pathlib import Path
from src.data_ingestion import load_payroll
from src.data_ingestion import load_payroll
from src.config_loader import set_config

import psycopg2 as db
from psycopg2 import OperationalError
from src.config_loader import set_config

# preamble
logger = logging.getLogger(__name__)
input_path = str(Path(__file__).parent.parent) + "/" + set_config()["file_path"]["input"]


def load_db_credentials():
    config = dotenv_values(find_dotenv(raise_error_if_not_found=True))
    print(f"({__name__})", ".env content: ", config)
    return config


def ping_database(dbname, user, password):
    logger.info(f"Pinging database with database name: {dbname}")
    connection = None
    try:
        connection = db.connect(dbname=dbname, user=user, password=password)  # add password when needed
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("PostgreSQL connection successful!")
        logger.info(f"PostgresSQL pinging for {dbname} connection successful!")
        return True
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        logger.exception("Error when connecting to database")
        raise
    finally:
        if connection:
            connection.close()
            logger.info("Connection closed.")


def connect_database(dbname, user, password):
    logger.info(f"Pinging database with database name: {dbname}")
    try:
        connection = db.connect(dbname=dbname, user=user, password=password)
        logger.info(f"PostgreSQL connection successful with database {dbname}")
        print(f"PostgreSQL connection successful with database {dbname}")
        return connection
    except OperationalError as e:
        logger.exception(f"Error when connecting to database {dbname}")
        print(f"Error when connecting to database {dbname}")
        raise


def create_table(dbname, user, password, table_name, name_column, datatype_column):
    with connect_database(dbname, user, password) as conn:
        with conn.cursor() as cur:
            columns = ""
            for column, datatype in zip(name_column, datatype_column):
                columns += ", " + column + " " + datatype

            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
            print(query)
            try:
                cur.execute(query)
            except OperationalError as err:
                print(f"error while creating table: {err}")
                raise

    print(f"table '{table_name}' created successfully")

# TODO: remove this once the above program is used
def create_table_query(file_path: str = Path(__file__).parent.parent / "data/other/column_schema.xlsx"):
    schema_dataframe = pd.read_excel(file_path)
    fixed_column_name = pd.Series(schema_dataframe['column_name'].str.replace(' ', '_', regex=False).
                                  str.replace('(', '', regex=False).str.replace(')', '', regex=False))
    query_per_row = pd.Series(fixed_column_name + ' ' + schema_dataframe['type'])
    query = "CREATE TABLE IF NOT EXISTS Payroll (" + ", ".join(list(query_per_row)) + ");"
    logger.debug(f"Table query created for simulation: {query} ")
    return query


# TODO: revise this program to make it simpler
# TODO: make this so that it doesn't append, just remakes it
def simulate_dataset(cur, simulate_dataset_flag=True):
    logger.info("Simulating dataset")
    if simulate_dataset_flag:
        payroll_table = create_table_query()
        try:
            res = cur.execute(payroll_table)
        except Exception as e:
            logger.exception(f"Table creation skipped: {e}")
            cur.connection.rollback()  # recover from failed transaction

        df = load_payroll(set_config()["file_path"]["input"])
        logger.debug(f"Simulating {len(df)} records into Payroll table")
        logger.debug(f"df dataframe: {df.to_string()}")
        for index, row in df.iterrows():
            cur.execute("""
                INSERT INTO Payroll (
                    month, employee_id, employee_name, department, designation,
                    month_days, paid_days, lwp, ctc_annual, gross_salary,
                    basic, hra, special_allowance, conveyance, medical,
                    other_allowances, variable_pay, investments_80c,
                    total_earnings, pf, pt, tds, other_deductions,
                    total_deductions, net_payable
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s
                )
                """,
                (row['month'], row['employee_id'], row['employee_name'], row['department'], row['designation'],
                 row['month_days'], row['paid_days'], row['lwp'], row['ctc_annual'], row['gross_salary'],
                 row['basic'], row['hra'], row['special_allowance'], row['conveyance'], row['medical'],
                 row['other_allowances'], row['variable_pay'], row['investments_80c'],
                 row['total_earnings'], row['pf'], row['pt'], row['tds'], row['other_deductions'],
                 row['total_deductions'], row['net_payable'])
            )
    logger.info("Dataset simulation complete")


# TODO: move to main wrapper
def import_database(database_cred, database_name, simulate_data=False) -> pd.DataFrame:
    dbname, user, password = database_cred
    logger.info(f"Importing database from {dbname}")
    with connect_database(dbname, user, password) as conn:
        with conn.cursor() as cur:
            if simulate_data:
                simulate_dataset(cur, simulate_data)
            query = f"SELECT * FROM {database_name}"
            try:
                result = pd.read_sql_query(query, conn)
            except Exception as e:
                print(f"some error when trying to import database: {e}")
                raise

            logger.info(f"Results are imported and stored: {len(result)}")
            logger.debug(f"results dataframe: {result.to_string()}")

    return result


# TODO: add insert, delete, or just query
def connect_database_api(credentials):
    logger.info(f"Pinging database with database name: {credentials.database}")
    try:
        connection = db.connect(
            host=credentials.host,
            port=credentials.port,
            dbname=credentials.database,
            user=credentials.username,
            password=credentials.password
        )
        logger.info(f"PostgreSQL connection successful with database {credentials.database}")
        return connection
    except OperationalError as e:
        logger.exception(f"Error when connecting to database {credentials.database}")
        raise


def import_database_api(credentials, database_name, simulate_data=False) -> pd.DataFrame:
    logger.info(f"Importing database from {credentials.database}")
    with connect_database_api(credentials) as conn:
        with conn.cursor() as cur:
            if simulate_data:
                simulate_dataset(cur, simulate_data)
            query = f"SELECT * FROM {database_name}"
            try:
                result = pd.read_sql_query(query, conn)
            except Exception as e:
                print(f"some error when trying to import database: {e}")
                raise

            logger.info(f"Results are imported and stored: {len(result)}")
            logger.debug(f"results dataframe: {result.to_string()}")

    return result
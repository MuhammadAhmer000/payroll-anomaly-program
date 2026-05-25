# Standard library
import io
import logging
from pathlib import Path

# Third party
from fastapi import FastAPI, HTTPException, APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# Local
from src.routes import router
from src.trend_analysis import get_trend_analysis, root_cause_formatter
from src.wrapper import (
    SET_CONFIG, LOAD_PAYROLL, LOAD_DB_CREDENTIALS,
    IMPORT_DATABASE, ANALYSIS_WRAPPER, EXPORT_WRAPPER, EXPORT_DATABASE
)

# App initialisation
logger = logging.getLogger(__name__)
app = FastAPI()

origins = [
    "https://payroll-anomaly-program.onrender.com",
    "http://localhost:5173",  # keep for local dev (Vite)
]

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://payroll-anomaly-program.onrender.com",
        "http://localhost:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(router)


def main():

    # === config loading ===
    global db_credentials
    config = SET_CONFIG()

    # === file path from config file
    # TODO: fix input_path so that it automatically appends input_path
    input_path = config["file_path"]["input"]

    output_path = str(Path(__file__).parent.parent) + '/' + config["file_path"]["output"]

    # === loading payroll (selecting excel or database)
    if config["ingestion_method"] == "excel":

        # === load excel payroll ===
        payroll_df = LOAD_PAYROLL(input_path)
        print(f"dataframe: {payroll_df.shape}")

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
    df_container = ANALYSIS_WRAPPER(payroll_df, EMP_COL, MONTH_COL, config, output_path)

    if config["exportation_method"] == "excel":
        EXPORT_WRAPPER(df_container, output_path)
        logger.info("Exportation has been completed in main()")

    elif config["exportation_method"] == "database":
        EXPORT_DATABASE(df_container, db_credentials)



if __name__ == "__main__":
    main()

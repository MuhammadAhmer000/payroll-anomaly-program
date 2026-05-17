# Standard library
import io
import logging

# Third party
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile
from starlette.responses import JSONResponse, StreamingResponse

# Local
import src.state as state
from src.config_loader import set_config_api
from src.data_exportation import compute_zscore_output
from src.data_ingestion import load_payroll_api
from src.database_ingestion import import_database, import_database_api
from src.wrapper import ANALYSIS_WRAPPER

# App setup
router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/download")
def download_endpoint():
    stored_results = state.stored_results_df

    if not state.stored_results_df:
        raise HTTPException(status_code=400, detail="No results available. Run analysis first.")

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for r in state.stored_results_df:
            compute_zscore_output(
                writer,
                r["emp_id"],
                r["rule_df"],
                r["stats_df"],
                r["unsupervised_df"],
                r["ensemble_df"],
                r["root_cause_df"],
                r["root_cause_summary"],
            )
    logger.info("Exportation has been completed in download_endpoint")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                             headers={"Content-Disposition": "attachment; filename=results.xlsx"})


# TODO: change in the future to /payroll, not /upload
@router.post("/upload")
def upload_endpoint(file: UploadFile):
    state.stored_df = load_payroll_api(file)
    return {"status": "uploaded"}


@router.post("/config")
def config_endpoint(file: UploadFile):
    state.stored_config = set_config_api(file)
    return {"status": "config uploaded"}


# Note: main will eventually be left for testing, React will be the "main" frontend
# TODO: add endpoint for /test here...
@router.post("/analyze")
def analyze():

    config = state.stored_config
    payroll_df = state.stored_df
    output_path = "output.xlsx"

    EMP_COL, MONTH_COL = "employee_id", "month"

    # TODO: to remove the "global", add a try/except block
    df_container = ANALYSIS_WRAPPER(payroll_df, EMP_COL, MONTH_COL, config, output_path)

    state.stored_results_df = df_container

    return JSONResponse(content=[
        {
            "emp_id": r["emp_id"],
            "rule_df": r["rule_df"].to_dict(orient="records"),
            "stats_df": r["stats_df"].to_dict(orient="records"),
            "unsupervised_df": r["unsupervised_df"].to_dict(orient="records"),
            "ensemble_df": r["ensemble_df"].to_dict(orient="records"),
            "root_cause_df": r["root_cause_df"].to_dict(orient="records"),
            "root_cause_summary": r["root_cause_summary"].to_dict(orient="records"),
            "overall": bool(r["overall"]),
        }
        for r in df_container
    ])


from pydantic import BaseModel


class DBCredentials(BaseModel):
    host: str
    port: str
    database: str
    username: str
    password: str


@router.post("/upload-db")
def upload_db_endpoint(credentials: DBCredentials):
    state.stored_df = import_database_api(credentials, "PAYROLL", False)
    return {"status": "database loaded"}






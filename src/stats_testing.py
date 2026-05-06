import logging

import numpy as np
import pandas as pd
import scipy.stats as stats

from src.data_ingestion import load_payroll
from src.helper_function import split_df

logger = logging.getLogger(__name__)


def numerical_df(dataframe): # TODO: add this to column_schema.xlsx
    numeric_cols = [
        'month_days', 'paid_days', 'lwp', 'ctc_annual', 'gross_salary',
        'basic', 'hra', 'special_allowance', 'conveyance', 'medical',
        'other_allowances', 'variable_pay', 'investments_80c',
        'total_earnings', 'pf', 'pt', 'tds', 'other_deductions',
        'total_deductions', 'net_payable'
    ]
    numeric_cols_existing = [col for col in numeric_cols if col in dataframe.columns]
    return dataframe[numeric_cols_existing].copy()


def compute_baseline(dataframe):
    logger.info("Computing baseline")
    dataframe_numeric = numerical_df(dataframe)

    means = dataframe_numeric.mean()
    stds = dataframe_numeric.std()

    valid_cols = stds[(stds > 0) & stds.notna()].index
    skipped_cols = stds[~stds.index.isin(valid_cols)].index.tolist()

    if skipped_cols:
        logger.warning(f"Columns skipped (NaN or std = 0): {skipped_cols}")

    logger.info("Baseline computation completed")
    return pd.DataFrame({
        "baseline_mean": means[valid_cols],
        "baseline_standard_deviation": stds[valid_cols]
    }).T


def compute_zscore_deviation(employee_dataframe, Z_THRESHOLD):
    logger.info("Computing z-score deviation")
    historical_df, target_df = split_df(employee_dataframe)
    baseline_df = compute_baseline(historical_df)

    common_cols = [col for col in baseline_df.columns if col in target_df.columns]
    target_values = target_df[common_cols].iloc[0].to_numpy()
    baseline_means = baseline_df.loc["baseline_mean", common_cols]
    baseline_stds = baseline_df.loc["baseline_standard_deviation", common_cols]

    z_scores = (target_values - baseline_means) / baseline_stds

    logger.info("Z-score deviation computation completed")
    return pd.DataFrame({
        "z_score": z_scores,
        "z_score_deviation (%)": stats.norm.cdf(z_scores) * 100,
        "anomaly": np.abs(z_scores) > Z_THRESHOLD
    })
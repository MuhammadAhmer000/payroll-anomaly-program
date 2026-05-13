import pandas as pd
import logging
from src.helper_function import split_df

# preamble & global variables
logger = logging.getLogger(__name__)
VALIDATIONS = []


def payroll_validation_wrapper(dataframe, config_data):

    logger.info("Payroll rule-based validation program running")

    historical_df, latest_df = split_df(dataframe)
    results = []

    for validation in VALIDATIONS:
        flag, actual, expected = validation["fn"](
            historical_df,
            latest_df,
            hra_threshold=config_data["rule_threshold"]["hra"],
            pf_rate=config_data["rate_data"]["pf"],
            pf_threshold=config_data["rule_threshold"]["pf"],
            net_pay_threshold=config_data["rule_threshold"]["net_payable"]
        )
        if flag:
            logger.info(f"{validation['name']} Validation: Anomaly Detected...")
        else:
            logger.info(f"{validation['name']} Validation: No Anomaly Detected!")

        results.append({"Name": validation["name"], "Actual": actual, "Expected": expected, "Anomaly": flag})
        print('\n')

    logger.info("Payroll rule-based validation program completed")
    return pd.DataFrame(results)


def register(name):
    def decorator(fn):
        VALIDATIONS.append({"name": name, "fn": fn})
        return fn
    return decorator


@register("PF")
def pf_validation(historical_df, latest_df, *, pf_rate=0.12, pf_threshold=0.1, **kwargs):
    logger.info("PF validation program running")
    expected_pf = latest_df["basic"].iloc[0] * pf_rate
    actual_pf = latest_df["pf"].iloc[0]
    logger.info(f"PF validation results: {(abs(actual_pf - expected_pf) > pf_threshold), actual_pf, expected_pf}")
    return (abs(actual_pf - expected_pf) > pf_threshold), actual_pf, expected_pf


@register("HRA")
def HRA_validation(historical_df, latest_df, *, hra_threshold=0.05, **kwargs):
    logger.info("HRA validation program running")
    hra_to_basic_historical = historical_df["hra"] / historical_df["basic"]
    hra_to_basic_latest = (latest_df["hra"] / latest_df["basic"]).iloc[0].round(4)
    hra_to_basic_deviation = abs(hra_to_basic_historical.mean() - hra_to_basic_latest).round(4)
    logger.info(f"HRA validation results: {(hra_to_basic_deviation > hra_threshold), hra_to_basic_latest, hra_to_basic_deviation}")
    return (hra_to_basic_deviation > hra_threshold), hra_to_basic_latest, hra_to_basic_deviation


@register("Net_Payable")
def net_pay_validation(historical_df, latest_df, *, net_pay_threshold=0.01, **kwargs):
    logger.info("Net Payable validation program running")
    expected_net_payable = (latest_df["total_earnings"] - latest_df["total_deductions"]).iloc[0]
    actual_net_payable = latest_df["net_payable"].iloc[0]
    logger.info(f"Net Payable validation results: {(abs(actual_net_payable - expected_net_payable) > net_pay_threshold), actual_net_payable, expected_net_payable}")
    return (abs(actual_net_payable - expected_net_payable) > net_pay_threshold), actual_net_payable, expected_net_payable
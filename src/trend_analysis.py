import logging
import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
import pandas as pd
logger = logging.getLogger(__name__)

def get_trend_analysis(emp_id, emp_df, field_root_cause, numeric_cols):
    logger.info("Running trend analysis program")
    pca_result = pca_column_severity_last_row(emp_df, numeric_cols)
    trend_result = trend_column_severity_last_row(emp_df, numeric_cols)

    final_output = {
        "PCA": pca_result,
        "Trend": trend_result
    }

    for col, sev in pca_result["severity"].items():
        field_root_cause.append({
            "Employee": emp_id,
            "Method": "PCA",
            "Field": col,
            "Severity": sev
        })

    for col, sev in trend_result["severity"].items():
        field_root_cause.append({
            "Employee": emp_id,
            "Method": "Trend",
            "Field": col,
            "Severity": sev
        })

    root_cause_df = pd.DataFrame(field_root_cause)
    logger.debug(root_cause_df)
    return root_cause_df


def pca_column_severity_last_row(
    df,
    numeric_cols,
    n_components=0.95,
    percentile_threshold=95,
    eps=1e-6
):

    train_df = df.iloc[:-1][numeric_cols]
    test_row = df.iloc[-1][numeric_cols].values.reshape(1, -1)

    pca = PCA(n_components=n_components, random_state=42)
    pca.fit(train_df)

    # Reconstruction
    reconstructed = pca.inverse_transform(
        pca.transform(train_df)
    )

    # Per-feature reconstruction error (train)
    train_errors = (train_df.values - reconstructed) ** 2

    # Threshold per feature (robust)
    thresholds = np.percentile(train_errors, percentile_threshold, axis=0)

    # Test row reconstruction
    test_reconstructed = pca.inverse_transform(
        pca.transform(test_row)
    )

    test_error = (test_row - test_reconstructed) ** 2
    test_error = test_error.flatten()

    flagged_cols = []
    severity_scores = {}

    for i, col in enumerate(numeric_cols):
        if test_error[i] > thresholds[i]:
            severity = round(
                test_error[i] / (thresholds[i] + eps), 2
            )
            flagged_cols.append(col)
            severity_scores[col] = severity

    return {
        "columns": flagged_cols,
        "severity": severity_scores
    }



def trend_column_severity_last_row(
        df,
        numeric_cols,
        threshold_multiplier=2.0,
        eps=1e-6
):
    """
    Returns:
        {
          "columns": [...],
          "severity": {col: severity_score}
        }
    """


    train_df = df.iloc[:-1]
    test_row = df.iloc[-1]

    flagged_cols = []
    severity_scores = {}

    for col in numeric_cols:
        y = train_df[col].values
        X = np.arange(1, len(y) + 1).reshape(-1, 1)

        model = LinearRegression()
        model.fit(X, y)

        expected = model.predict([[len(y) + 1]])[0]
        actual = test_row[col]

        deviation = abs(actual - expected)
        threshold = threshold_multiplier * np.std(y)

        severity = round(deviation / (threshold + eps), 2)

        logger.debug(
            f"{col}: actual={actual}, expected={expected:.2f}, deviation={deviation:.2f}, threshold={threshold:.2f}, severity={severity}")

        if deviation > threshold:
            flagged_cols.append(col)
            severity_scores[col] = severity

    logger.debug(f"{flagged_cols}, {severity_scores}")

    return {
        "columns": flagged_cols,
        "severity": severity_scores
    }


def root_cause_formatter(root_cause_df):
    if root_cause_df.empty:
        logger.info("No anomalies detected by root cause analysis")
        # Create an EMPTY summary with correct schema
        root_cause_summary = pd.DataFrame(
            columns=["Employee", "Field", "Methods", "Max_Severity", "Detected_By_Both"]
        )
    else:
        root_cause_summary = (
            root_cause_df
            .groupby(["Employee", "Field"])
            .agg(
                Methods=("Method", list),
                Max_Severity=("Severity", "max")
            )
            .reset_index()
        )
        root_cause_summary["Detected_By_Both"] = (
            root_cause_summary["Methods"]
            .apply(lambda x: set(x) == {"PCA", "Trend"})
        )

    return root_cause_df, root_cause_summary

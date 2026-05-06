import logging

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import numpy as np
from src.helper_function import get_numerical_cols

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import numpy as np
logger = logging.getLogger(__name__)

# TODO: add hyperparameters to the logging functions

def get_ensemble_results(emp_id, unsupervised_results, ensemble_results):
    iso_anomaly = unsupervised_results["Latest Record Anomaly? (Y/N)"].iloc[0]
    iso_reduced_anomaly = unsupervised_results["Latest Record Anomaly? (Y/N)"].iloc[1]
    lof_anomaly = unsupervised_results["Latest Record Anomaly? (Y/N)"].iloc[2]
    pca_anomaly = unsupervised_results["Latest Record Anomaly? (Y/N)"].iloc[3]

    votes = sum([pca_anomaly, iso_anomaly, lof_anomaly, iso_reduced_anomaly])

    ensemble_results.append({
        "Employee": emp_id,
        "PCA_Anomaly": pca_anomaly,
        "IsolationForest_Anomaly": iso_anomaly,
        "IsolationForest_Reduced_Anomaly": iso_reduced_anomaly,
        "LOF_Anomaly": lof_anomaly,
        "Ensemble_Anomaly": votes >= 2
    })
    ensemble_df = pd.DataFrame(ensemble_results)

    return ensemble_df


def unsupervised_machine_learning_results(emp_df):
    logger.info("Running unsupervised ML models")
    unsupervised_results = pd.DataFrame() # TODO: I don't think I need to concatenate anymore, so remove this later

    machine_learning_rows = [
        unsupervised_isolationforest(emp_df),
        unsupervised_reduced_isolationforest(emp_df),
        unsupervised_lof(emp_df),
        unsupervised_pca(emp_df),
    ]

    unsupervised_results = pd.concat(
        [unsupervised_results, pd.DataFrame(machine_learning_rows)],
        ignore_index=True
    )
    logger.info("Unsupervised ML complete")
    return unsupervised_results

def unsupervised_isolationforest(X):
    """
    Detect anomaly in the last row using Isolation Forest with decision_function.
    Uses global numeric_cols to select numeric features.
    Returns a dict in the same format as your ensemble expects.
    """
    logger.debug("Running Isolation Forest")
    # -----------------------------
    # 1. Train / test split
    # -----------------------------
    train_df = X.iloc[:-1]
    test_df  = X.iloc[[-1]]

    # -----------------------------
    # 2. Select numeric columns using global numeric_cols
    # -----------------------------
    numeric_cols = get_numerical_cols()
    train_num = train_df[numeric_cols]
    test_num  = test_df[numeric_cols]

    # -----------------------------
    # 3. Scale numeric features
    # -----------------------------
    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train_num)
    test_scaled  = scaler.transform(test_num)

    # -----------------------------
    # 4. Isolation Forest
    # -----------------------------
    iso = IsolationForest(contamination=0.05, random_state=42)  # higher for small datasets
    iso.fit(train_scaled)

    # -----------------------------
    # 5. Decision function for anomaly detection
    # -----------------------------
    train_scores = iso.decision_function(train_scaled)
    latest_score = iso.decision_function(test_scaled)[0]

    # Lower score = more anomalous
    is_anomaly = latest_score < train_scores.min()

    # -----------------------------
    # 6. Return result
    # -----------------------------
    logger.debug(f"Isolation Forest result: {is_anomaly}")
    return {
        "Model": "Isolation Forest",
        "Latest Record Anomaly? (Y/N)": True if is_anomaly else False
    }


def unsupervised_reduced_isolationforest(X, corr_threshold=0.9):
    """
    Detects anomaly in the latest row using Isolation Forest
    after dropping highly correlated features.
    Returns True/False for "Latest Record Anomaly? (Y/N)".
    """
    logger.debug("Running Dimensionality-Reduced Isolation Forest")

    train_df = X.iloc[:-1]
    test_df  = X.iloc[[-1]]

    numeric_cols = get_numerical_cols()
    train_num = train_df[numeric_cols]
    test_num  = test_df[numeric_cols]

    # Drop highly correlated features
    corr_matrix = train_num.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    to_drop = [col for col in upper.columns if any(upper[col] > corr_threshold)]

    train_reduced = train_num.drop(columns=to_drop)
    test_reduced  = test_num.drop(columns=to_drop)

    # Scale
    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train_reduced)
    test_scaled  = scaler.transform(test_reduced)

    # Contamination relative to training size
    # contamination = 1 / len(train_df)

    iso = IsolationForest(contamination='auto', random_state=42)
    iso.fit(train_scaled)

    # Decision function
    train_scores = iso.decision_function(train_scaled)
    latest_score = iso.decision_function(test_scaled)[0]

    # Flag anomaly
    is_anomaly = latest_score < train_scores.min()

    logger.debug(f"Dimensionality-Reduced Isolation Forest result: {is_anomaly}")

    row = {
        "Model": "Isolation Forest (Reduced)",
        "Latest Record Anomaly? (Y/N)": True if is_anomaly else False
    }

    return row

from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import RobustScaler
import numpy as np

def unsupervised_lof(X, contamination=0.1):
    logger.debug("Running Local Outlier Factor")
    """
    Uses continuous LOF scores to decide
    if the latest record is anomalous (Y/N).
    """

    # -----------------------------
    # 1. Train / test split
    # -----------------------------
    train_df = X.iloc[:-1]
    test_df  = X.iloc[[-1]]

    numeric_cols = get_numerical_cols()
    train_num = train_df[numeric_cols]
    test_num  = test_df[numeric_cols]

    # -----------------------------
    # 2. Scale
    # -----------------------------
    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train_num)
    test_scaled  = scaler.transform(test_num)

    # -----------------------------
    # 3. Fit LOF (novelty mode)
    # -----------------------------
    lof = LocalOutlierFactor(
        n_neighbors=15,
        novelty=True
    )

    lof.fit(train_scaled)

    # -----------------------------
    # 4. Continuous scores
    # -----------------------------
    train_scores = lof.decision_function(train_scaled)
    latest_score = lof.decision_function(test_scaled)[0]

    # Lower score = more anomalous
    threshold = np.percentile(train_scores, contamination * 100)

    is_anomaly = latest_score < threshold

    # -----------------------------
    # 5. Return result
    # -----------------------------
    logger.debug(f"Local Outlier Factor result: {is_anomaly}")

    row = {
        "Model": "Local Outlier Factor",
        "Latest Record Anomaly? (Y/N)": True if is_anomaly else False,
    }

    return row

from sklearn.decomposition import PCA
from sklearn.preprocessing import RobustScaler
import numpy as np
import pandas as pd

def unsupervised_pca(X):

    logger.debug("Running Principle Component Analysis (PCA)")

    # -----------------------------
    # 1. Train / test split (last row = decision point)
    # -----------------------------
    train_df = X.iloc[:-1]
    test_df  = X.iloc[[-1]]

    numeric_cols = get_numerical_cols()
    train_num = train_df[numeric_cols]
    test_num = test_df[numeric_cols]

    # -----------------------------
    # 2. Scale using TRAIN only
    # -----------------------------
    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train_num)
    test_scaled  = scaler.transform(test_num)

    # -----------------------------
    # 3. Fit PCA on TRAIN
    # -----------------------------
    pca = PCA(n_components=0.9, random_state=42)
    train_pca = pca.fit_transform(train_scaled)

    # -----------------------------
    # 4. Reconstruction error (TRAIN)
    # -----------------------------
    train_recon = pca.inverse_transform(train_pca)
    train_error = np.linalg.norm(train_scaled - train_recon, axis=1)

    # Threshold (business-controlled)
    threshold = np.percentile(train_error, 90)

    # -----------------------------
    # 5. Evaluate LAST ROW
    # -----------------------------
    test_pca = pca.transform(test_scaled)
    test_recon = pca.inverse_transform(test_pca)
    test_error = np.linalg.norm(test_scaled - test_recon, axis=1)[0]

    is_anomaly = test_error > threshold

    logger.debug(f"Principle Component Analysis (PCA) result: {is_anomaly}")
    # -----------------------------
    # 6. Diagnostics
    # -----------------------------
    # print("\nUnsupervised PCA")
    # print("Reconstruction error (latest):", round(test_error, 3))
    # print("Threshold:", round(threshold, 3))
    # print("Latest record anomaly?:", "YES" if is_anomaly else "NO")

    row = {
        "Model": "PCA",
        "Latest Record Anomaly? (Y/N)": True if is_anomaly else False,
    }

    return row


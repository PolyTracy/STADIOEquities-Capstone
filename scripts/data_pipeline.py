"""
Shared data pipeline for the STADIOEquities SS2 viability study.

This module handles PREPROCESSING and FEATURE ENGINEERING for the public
UCI Bank Marketing dataset (bank-additional-full.csv), which is used as a
viability stand-in for STADIOEquities' account-activation problem:
predicting whether a bank client subscribes to a term deposit (y = yes/no)
is analogous to predicting whether a registered account funds/activates.

Both model scripts (model1_logistic_regression.py, model2_random_forest.py)
import from here so that preprocessing and feature engineering are identical
across models — the only thing that changes between them is the estimator.

Run directly to print a summary of the cleaned, engineered dataset:
    python scripts/data_pipeline.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# --- paths -------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "external" / "bank-additional-full.csv"
RANDOM_STATE = 42

# Columns after feature engineering
NUMERIC_FEATURES = [
    "age", "campaign", "pdays", "previous",
    "emp.var.rate", "cons.price.idx", "cons.conf.idx", "euribor3m",
    "nr.employed", "was_prev_contacted",
]
CATEGORICAL_FEATURES = [
    "job", "marital", "education", "default", "housing", "loan",
    "contact", "month", "day_of_week", "poutcome",
]


def load_raw(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the raw semicolon-delimited UCI Bank Marketing CSV."""
    df = pd.read_csv(path, sep=";")
    return df


def clean_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    """
    PREPROCESSING + FEATURE ENGINEERING.

    Key, deliberate decisions (documented in Preprocessing.MD /
    FeatureEngineering.MD):

    1. DROP `duration`. The dataset authors (Moro et al., 2014) warn that the
       last-contact duration is not known before a call is made and leaks the
       target almost perfectly (duration = 0 => y = 'no'). Keeping it would
       inflate performance and produce a model that cannot be used in practice.
       This mirrors the label-leakage risk (R2) flagged in the SS1 RAAIDD log.

    2. `pdays` uses 999 as a sentinel meaning "client was not previously
       contacted". We engineer a binary flag `was_prev_contacted` and recode
       the 999 sentinel to 0 so the numeric scale is not distorted.

    3. The target `y` ('yes'/'no') is mapped to 1/0.

    'unknown' values in categorical columns are treated as their own category
    (they are informative missingness), so no rows are dropped for them.
    """
    df = df.copy()

    # 1. Drop the leaky duration column
    if "duration" in df.columns:
        df = df.drop(columns=["duration"])

    # 2. pdays sentinel handling + engineered flag
    df["was_prev_contacted"] = (df["pdays"] != 999).astype(int)
    df["pdays"] = df["pdays"].replace(999, 0)

    # 3. Encode target
    df["target"] = (df["y"] == "yes").astype(int)
    df = df.drop(columns=["y"])

    return df


def build_preprocessor() -> ColumnTransformer:
    """
    ColumnTransformer applied inside each model pipeline:
      - numeric  -> median imputation + standardisation (needed by LR; harmless for RF)
      - categorical -> most-frequent imputation + one-hot encoding
    Fitting happens on the training fold only, avoiding data leakage.
    """
    numeric_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical_pipe = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([
        ("num", numeric_pipe, NUMERIC_FEATURES),
        ("cat", categorical_pipe, CATEGORICAL_FEATURES),
    ])


def get_train_test(test_size: float = 0.2):
    """Return X_train, X_test, y_train, y_test (stratified split)."""
    df = clean_and_engineer(load_raw())
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df["target"]
    return train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=RANDOM_STATE
    )


def feature_names_after_transform(preprocessor: ColumnTransformer):
    """Recover readable feature names after fitting the ColumnTransformer."""
    ohe = preprocessor.named_transformers_["cat"].named_steps["onehot"]
    cat_names = ohe.get_feature_names_out(CATEGORICAL_FEATURES)
    return list(NUMERIC_FEATURES) + list(cat_names)


if __name__ == "__main__":
    df_raw = load_raw()
    df = clean_and_engineer(df_raw)
    print("Raw shape:            ", df_raw.shape)
    print("Engineered shape:     ", df.shape)
    print("Dropped 'duration':   ", "duration" not in df.columns)
    print("Target balance (%):")
    print((df["target"].value_counts(normalize=True) * 100).round(2))
    print("\nEngineered columns:")
    print(list(df.columns))

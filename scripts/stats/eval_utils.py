"""
Statistical helper & model-comparison utilities for SS2.

Provides a single place to compute the classification metrics used across
Model 1, Model 2 and the comparison, so every result is calculated the same way.
"""
import json
from pathlib import Path
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix,
    balanced_accuracy_score,
)

ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT / "experiments" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def compute_metrics(y_true, y_pred, y_proba) -> dict:
    """Return the standard metric set for an imbalanced binary classifier."""
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "balanced_accuracy": round(balanced_accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 4),
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_true, y_proba), 4),
        "pr_auc": round(average_precision_score(y_true, y_proba), 4),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp),
                             "fn": int(fn), "tp": int(tp)},
    }


def save_metrics(name: str, metrics: dict) -> Path:
    path = RESULTS_DIR / f"{name}_metrics.json"
    with open(path, "w") as f:
        json.dump(metrics, f, indent=2)
    return path


def load_metrics(name: str) -> dict:
    with open(RESULTS_DIR / f"{name}_metrics.json") as f:
        return json.load(f)


def print_report(title: str, metrics: dict):
    print(f"\n{'='*54}\n{title}\n{'='*54}")
    for k, v in metrics.items():
        if k == "confusion_matrix":
            cm = v
            print(f"  confusion_matrix : TN={cm['tn']}  FP={cm['fp']}  "
                  f"FN={cm['fn']}  TP={cm['tp']}")
        else:
            print(f"  {k:18s}: {v}")

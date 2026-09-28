"""
Comparison of Model 1 (Logistic Regression) and Model 2 (Random Forest).

Reads the saved metrics and ROC/PR curve data from both models and produces:
  - a side-by-side metrics table (printed + saved as CSV)
  - a combined ROC curve figure
  - a combined precision-recall curve figure

Run AFTER model1_logistic_regression.py and model2_random_forest.py:
    python scripts/comparison.py
Outputs (experiments/results/):
    comparison_metrics.csv
    comparison_roc.png
    comparison_pr.png
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).resolve().parent / "stats"))
from eval_utils import load_metrics, RESULTS_DIR

METRIC_KEYS = ["accuracy", "balanced_accuracy", "precision", "recall",
               "f1", "roc_auc", "pr_auc"]


def main():
    m1 = load_metrics("model1_logistic")
    m2 = load_metrics("model2_rf")

    table = pd.DataFrame({
        "Metric": METRIC_KEYS,
        "Model 1 – Logistic Regression": [m1[k] for k in METRIC_KEYS],
        "Model 2 – Random Forest": [m2[k] for k in METRIC_KEYS],
    })
    table["Winner"] = np.where(
        table["Model 2 – Random Forest"] > table["Model 1 – Logistic Regression"],
        "Random Forest",
        np.where(table["Model 2 – Random Forest"] < table["Model 1 – Logistic Regression"],
                 "Logistic Regression", "Tie"))
    print(table.to_string(index=False))
    table.to_csv(RESULTS_DIR / "comparison_metrics.csv", index=False)

    # Combined ROC
    d1 = np.load(RESULTS_DIR / "model1_roc_pr.npz")
    d2 = np.load(RESULTS_DIR / "model2_roc_pr.npz")
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(d1["fpr"], d1["tpr"],
            label=f"Logistic Regression (AUC={m1['roc_auc']})", color="#4A76B8")
    ax.plot(d2["fpr"], d2["tpr"],
            label=f"Random Forest (AUC={m2['roc_auc']})", color="#2E7D32")
    ax.plot([0, 1], [0, 1], "--", color="grey", linewidth=0.8, label="Random")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve — Model 1 vs Model 2")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "comparison_roc.png", dpi=130)
    plt.close(fig)

    # Combined PR
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(d1["recall"], d1["precision"],
            label=f"Logistic Regression (PR-AUC={m1['pr_auc']})", color="#4A76B8")
    ax.plot(d2["recall"], d2["precision"],
            label=f"Random Forest (PR-AUC={m2['pr_auc']})", color="#2E7D32")
    ax.axhline(0.1127, ls="--", color="grey", linewidth=0.8,
               label="Base rate (11.3%)")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curve — Model 1 vs Model 2")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "comparison_pr.png", dpi=130)
    plt.close(fig)

    print("\nSaved comparison table + figures to experiments/results/")


if __name__ == "__main__":
    main()

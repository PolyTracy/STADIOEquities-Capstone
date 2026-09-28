"""
Model 1 — Logistic Regression (interpretable linear baseline).

Trains a class-weight-balanced logistic regression on the public UCI Bank
Marketing dataset, with hyper-parameter C selected by 3-fold cross-validated
ROC-AUC. Saves test-set metrics, a confusion matrix, and the top coefficients.

Usage:
    python scripts/model1_logistic_regression.py
Outputs (experiments/results/):
    model1_logistic_metrics.json
    model1_confusion_matrix.png
    model1_coefficients.png
    model1_roc_pr.npz   (fpr/tpr/precision/recall for the comparison plot)
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_curve, precision_recall_curve, ConfusionMatrixDisplay

sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parent / "stats"))
from data_pipeline import (get_train_test, build_preprocessor,
                           feature_names_after_transform, RANDOM_STATE)
from eval_utils import compute_metrics, save_metrics, print_report, RESULTS_DIR

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"
MODELS_DIR.mkdir(exist_ok=True)


def main():
    X_train, X_test, y_train, y_test = get_train_test()

    pipe = Pipeline([
        ("prep", build_preprocessor()),
        ("clf", LogisticRegression(
            max_iter=2000, class_weight="balanced",
            solver="liblinear", random_state=RANDOM_STATE)),
    ])

    # Hyper-parameter search over regularisation strength C
    grid = {"clf__C": [0.01, 0.1, 1.0, 10.0], "clf__penalty": ["l2"]}
    search = GridSearchCV(pipe, grid, scoring="roc_auc", cv=3, n_jobs=-1)
    search.fit(X_train, y_train)
    best = search.best_estimator_
    print("Best params:", search.best_params_)
    print("Best CV ROC-AUC:", round(search.best_score_, 4))

    # Evaluate on the held-out test set
    y_pred = best.predict(X_test)
    y_proba = best.predict_proba(X_test)[:, 1]
    metrics = compute_metrics(y_test, y_pred, y_proba)
    metrics["best_params"] = search.best_params_
    metrics["cv_roc_auc"] = round(search.best_score_, 4)
    print_report("MODEL 1 — LOGISTIC REGRESSION (test set)", metrics)
    save_metrics("model1_logistic", metrics)

    # Persist model
    joblib.dump(best, MODELS_DIR / "model1_logistic_regression.joblib")

    # Confusion matrix figure
    fig, ax = plt.subplots(figsize=(4.5, 4))
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred, display_labels=["no", "yes"], cmap="Blues", ax=ax)
    ax.set_title("Model 1 (Logistic Regression) — Confusion Matrix")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "model1_confusion_matrix.png", dpi=130)
    plt.close(fig)

    # Coefficient importance (log-odds)
    feat_names = feature_names_after_transform(best.named_steps["prep"])
    coefs = best.named_steps["clf"].coef_[0]
    order = np.argsort(np.abs(coefs))[::-1][:15]
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#4A76B8" if coefs[i] > 0 else "#C0504D" for i in order]
    ax.barh([feat_names[i] for i in order][::-1],
            [coefs[i] for i in order][::-1], color=colors[::-1])
    ax.set_title("Model 1 — Top 15 coefficients (log-odds of subscribing)")
    ax.axvline(0, color="black", linewidth=0.6)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "model1_coefficients.png", dpi=130)
    plt.close(fig)

    # Save ROC/PR curve data for the comparison plot
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    prec, rec, _ = precision_recall_curve(y_test, y_proba)
    np.savez(RESULTS_DIR / "model1_roc_pr.npz",
             fpr=fpr, tpr=tpr, precision=prec, recall=rec)

    print("\nSaved model + figures to experiments/results/ and models/")


if __name__ == "__main__":
    main()

"""
Model 2 — Random Forest (ensemble of decision trees).

Trains a class-weight-balanced random forest on the public UCI Bank Marketing
dataset, with key hyper-parameters (tree depth, leaf size) selected by 3-fold
cross-validated ROC-AUC. Saves test-set metrics, a confusion matrix, and
feature importances.

Usage:
    python scripts/model2_random_forest.py
Outputs (experiments/results/):
    model2_rf_metrics.json
    model2_confusion_matrix.png
    model2_feature_importance.png
    model2_roc_pr.npz
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import joblib
from sklearn.ensemble import RandomForestClassifier
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
        ("clf", RandomForestClassifier(
            n_estimators=300, class_weight="balanced_subsample",
            random_state=RANDOM_STATE, n_jobs=-1)),
    ])

    grid = {
        "clf__max_depth": [10, 20, None],
        "clf__min_samples_leaf": [5, 20],
    }
    search = GridSearchCV(pipe, grid, scoring="roc_auc", cv=3, n_jobs=-1)
    search.fit(X_train, y_train)
    best = search.best_estimator_
    print("Best params:", search.best_params_)
    print("Best CV ROC-AUC:", round(search.best_score_, 4))

    y_pred = best.predict(X_test)
    y_proba = best.predict_proba(X_test)[:, 1]
    metrics = compute_metrics(y_test, y_pred, y_proba)
    metrics["best_params"] = search.best_params_
    metrics["cv_roc_auc"] = round(search.best_score_, 4)
    print_report("MODEL 2 — RANDOM FOREST (test set)", metrics)
    save_metrics("model2_rf", metrics)

    joblib.dump(best, MODELS_DIR / "model2_random_forest.joblib")

    # Confusion matrix
    fig, ax = plt.subplots(figsize=(4.5, 4))
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred, display_labels=["no", "yes"], cmap="Greens", ax=ax)
    ax.set_title("Model 2 (Random Forest) — Confusion Matrix")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "model2_confusion_matrix.png", dpi=130)
    plt.close(fig)

    # Feature importances
    feat_names = feature_names_after_transform(best.named_steps["prep"])
    importances = best.named_steps["clf"].feature_importances_
    order = np.argsort(importances)[::-1][:15]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh([feat_names[i] for i in order][::-1],
            [importances[i] for i in order][::-1], color="#2E7D32")
    ax.set_title("Model 2 — Top 15 feature importances")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "model2_feature_importance.png", dpi=130)
    plt.close(fig)

    fpr, tpr, _ = roc_curve(y_test, y_proba)
    prec, rec, _ = precision_recall_curve(y_test, y_proba)
    np.savez(RESULTS_DIR / "model2_roc_pr.npz",
             fpr=fpr, tpr=tpr, precision=prec, recall=rec)

    print("\nSaved model + figures to experiments/results/ and models/")


if __name__ == "__main__":
    main()

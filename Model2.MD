# Model 2 — Random Forest

**Relevant script:** [`scripts/model2_random_forest.py`](scripts/model2_random_forest.py)

**How to run**
```bash
pip install -r requirements.txt
python scripts/model2_random_forest.py
```
This trains the model, runs the hyper-parameter search, evaluates on the held-out
test set, saves the trained model to `models/model2_random_forest.joblib`, and
writes metrics + figures to `experiments/results/`. Results are documented in
[Model2Performance.MD](Model2Performance.MD).

---

## Technique

**Random forest** — a supervised **ensemble of decision trees**. Each tree is
trained on a bootstrap sample of the data using a random subset of features, and
predictions are averaged. This reduces the high variance of a single decision
tree while capturing **non-linear relationships and feature interactions** that a
linear model cannot. It is chosen as the higher-capacity counterpart to Model 1,
letting us test the interpretability-vs-accuracy trade-off central to the module.

## Preprocessing & feature engineering used

Uses the same shared pipeline as Model 1 (see [Preprocessing.MD](Preprocessing.MD)
and [FeatureEngineering.MD](FeatureEngineering.MD)). Scaling is not strictly
required for a tree model but is retained for a like-for-like comparison; the
dropped-`duration` leakage fix and the engineered `was_prev_contacted` flag are
applied identically.

## Model details & hyper-parameters

| Setting | Value | Reason |
|---------|-------|--------|
| Estimator | `RandomForestClassifier` (scikit-learn) | Ensemble of decision trees; strong on tabular data. |
| `n_estimators` | 300 | Enough trees for stable averaging. |
| `class_weight` | `balanced_subsample` | Handles the class imbalance within each bootstrap sample. |
| `max_depth` | **selected by search** | Tuned over `{10, 20, None}` to control overfitting. |
| `min_samples_leaf` | **selected by search** | Tuned over `{5, 20}` to smooth predictions. |
| `random_state` | 42 | Reproducibility. |
| Selection | `GridSearchCV`, 3-fold, scored on **ROC-AUC** | Same selection metric as Model 1 for fairness. |

**Selected hyper-parameters:** `max_depth = 10`, `min_samples_leaf = 5`
(best 3-fold CV ROC-AUC ≈ **0.7955**). The shallow depth confirms that a
constrained forest generalises better than deep, unconstrained trees on this data.

## Outputs produced

- `models/model2_random_forest.joblib` — the trained pipeline.
- `experiments/results/model2_rf_metrics.json` — test metrics.
- `experiments/results/model2_confusion_matrix.png`
- `experiments/results/model2_feature_importance.png` — top 15 feature importances.

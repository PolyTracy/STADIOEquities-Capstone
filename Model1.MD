# Model 1 — Logistic Regression

**Relevant script:** [`scripts/model1_logistic_regression.py`](scripts/model1_logistic_regression.py)

**How to run**
```bash
pip install -r requirements.txt
python scripts/model1_logistic_regression.py
```
This trains the model, runs the hyper-parameter search, evaluates on the held-out
test set, saves the trained model to `models/model1_logistic_regression.joblib`,
and writes metrics + figures to `experiments/results/`. Results are documented in
[Model1Performance.MD](Model1Performance.MD).

---

## Technique

**Logistic regression** — a supervised, linear classifier that models the
log-odds of the positive class (subscription/activation) as a weighted sum of the
input features. It is chosen as the **interpretable baseline**: its coefficients
state the direction and strength of each feature's effect, which matters when the
findings must be explained to non-technical decision-makers (a core SS1/SS2 aim).

## Preprocessing & feature engineering used

Uses the shared pipeline (see [Preprocessing.MD](Preprocessing.MD) and
[FeatureEngineering.MD](FeatureEngineering.MD)): median/most-frequent imputation,
**standard scaling** of numerics (important for a linear model), one-hot encoding
of categoricals, and the dropped-`duration` leakage fix. All steps are fitted
inside cross-validation via an sklearn `Pipeline`, so no test data leaks in.

## Model details & hyper-parameters

| Setting | Value | Reason |
|---------|-------|--------|
| Estimator | `LogisticRegression` (scikit-learn) | Linear, interpretable baseline. |
| `class_weight` | `balanced` | Counters the 11.3% / 88.7% class imbalance by up-weighting the minority "yes" class. |
| `solver` | `liblinear` | Efficient and supports L2 penalty on this data size. |
| `penalty` | `l2` | Ridge regularisation to control variance. |
| `C` (inverse reg. strength) | **selected by search** | Tuned over `{0.01, 0.1, 1.0, 10.0}`. |
| `max_iter` | 2000 | Ensures convergence. |
| Selection | `GridSearchCV`, 3-fold, scored on **ROC-AUC** | Threshold-independent, imbalance-appropriate selection metric. |

**Selected hyper-parameter:** `C = 0.1` (best 3-fold CV ROC-AUC ≈ **0.79**),
indicating fairly strong regularisation generalises best here.

## Outputs produced

- `models/model1_logistic_regression.joblib` — the trained pipeline.
- `experiments/results/model1_logistic_metrics.json` — test metrics.
- `experiments/results/model1_confusion_matrix.png`
- `experiments/results/model1_coefficients.png` — top 15 coefficients (log-odds).

# Feature Engineering

**Relevant script:** [`scripts/data_pipeline.py`](scripts/data_pipeline.py)
(function `clean_and_engineer()` for the engineered variables, and
`build_preprocessor()` / `feature_names_after_transform()` for the encoding).

**How to run**
```bash
python scripts/data_pipeline.py   # prints engineered columns and target balance
```

---

## Engineered and selected features

| Feature | Type | How it was engineered | Rationale |
|---------|------|-----------------------|-----------|
| `was_prev_contacted` | Engineered binary | `1` if `pdays != 999`, else `0`. | Separates "contacted before" from the 999 sentinel; whether a client was reached in a prior campaign is a strong signal (analogous to whether a STADIOEquities account had prior engagement). |
| `pdays` (recoded) | Numeric | 999 sentinel → 0, kept as recency-in-days otherwise. | Makes the numeric scale meaningful for the linear model. |
| `duration` | **Removed** | Dropped entirely. | Target leakage — see [Preprocessing.MD](Preprocessing.MD). This is a deliberate feature-*selection* decision, not an oversight. |
| One-hot categoricals | Engineered | `job, marital, education, default, housing, loan, contact, month, day_of_week, poutcome` → indicator columns. | Converts nominal categories into model-ready numeric features. |
| Standardised numerics | Transformed | `age, campaign, pdays, previous, emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed, was_prev_contacted`. | Puts features on a common scale for logistic regression. |

**Final feature space:** 10 numeric + 10 categorical (one-hot expanded to ~50+
indicator columns after encoding). The original `duration` feature is excluded.

## Feature groups

- **Client attributes:** `age`, `job`, `marital`, `education`, `default`,
  `housing`, `loan`.
- **Campaign contact:** `contact`, `month`, `day_of_week`, `campaign`,
  `pdays`, `previous`, `poutcome`, `was_prev_contacted`.
- **Macro-economic context:** `emp.var.rate`, `cons.price.idx`,
  `cons.conf.idx`, `euribor3m`, `nr.employed`.

## Note on encoding choice

One-hot encoding was chosen over ordinal/label encoding because most categorical
variables are nominal (e.g. `job`, `contact`) and imposing an artificial order
would mislead the linear model. `handle_unknown='ignore'` guarantees the pipeline
still runs if an unseen category appears at inference — important when the same
approach is later adapted to STADIOEquities' own data (see the Part D report).

## Mapping back to STADIOEquities

Each engineered feature has a direct counterpart in the SS1 data request:
campaign-contact features ↔ acquisition channel / nudges; client attributes ↔
demographics; `poutcome`/`was_prev_contacted` ↔ prior onboarding engagement.
This alignment is what makes the public dataset a credible viability test.

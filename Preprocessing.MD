# Preprocessing

**Relevant script:** [`scripts/data_pipeline.py`](scripts/data_pipeline.py)
(functions `load_raw()` and `clean_and_engineer()`, plus the numeric/categorical
transformers in `build_preprocessor()`).

**How to run**
```bash
pip install -r requirements.txt
python scripts/data_pipeline.py      # prints a summary of the cleaned dataset
```
Preprocessing is not applied as a standalone step that writes a file — it is
imported by both model scripts so that the *identical* preprocessing is applied
inside each model's cross-validation, which prevents data leakage from the test
fold into the training fold.

---

## Dataset

The public **UCI Bank Marketing** dataset (`bank-additional-full.csv`, 41,188
rows, 20 input variables) is used as a viability stand-in for the STADIOEquities
account-activation problem: predicting whether a client subscribes to a term
deposit (`y` = yes/no) is directly analogous to predicting whether a registered
account funds/activates. See the Part A report for the full dataset description.

## Preprocessing steps

| Step | What is done | Why |
|------|--------------|-----|
| **Load** | Read the semicolon-delimited CSV with `pandas`. | Native format of the UCI file. |
| **Drop `duration`** | The last-contact call duration column is removed. | The dataset authors (Moro *et al.*, 2014) state `duration` is not known before a call and leaks the target almost perfectly (`duration = 0 ⇒ y = no`). Keeping it produces an unusable, over-optimistic model. This directly addresses the **label-leakage risk (R2)** from the SS1 RAAIDD log. |
| **`pdays` sentinel** | `pdays = 999` ("never previously contacted") is recoded to `0`, and a new binary flag `was_prev_contacted` is created. | 999 is a sentinel, not a real "days" value; leaving it in would distort scaling and distance. |
| **Encode target** | `y` ('yes'/'no') → `target` (1/0). | Required numeric target for classification. |
| **Missing-value imputation** | Numeric → median; categorical → most-frequent (fitted inside each CV fold). | Robust, leakage-safe imputation. |
| **`unknown` categories** | Kept as their own category rather than dropped. | The presence of `unknown` (e.g. undisclosed default status) is itself informative. |
| **Scaling** | Numeric features standardised (`StandardScaler`). | Required by logistic regression; harmless to the random forest. |
| **One-hot encoding** | Categorical features one-hot encoded with `handle_unknown='ignore'`. | Converts categories to a numeric matrix; ignores unseen categories at inference. |

## Class balance

The target is **imbalanced**: ~11.3% "yes" vs ~88.7% "no". This is handled at
the modelling stage with class weighting (see [Model1.MD](Model1.MD) and
[Model2.MD](Model2.MD)) and evaluated with imbalance-aware metrics
(see [Model1Performance.MD](Model1Performance.MD)).

## Reproducibility

A fixed `RANDOM_STATE = 42` is used for the train/test split and both models.
The dataset is committed under `data/external/`; alternatively
[`scripts/download_data.py`](scripts/download_data.py) re-downloads it from UCI.

# SS3 Part B: Applying the Final Model to Client Data

**Notebook:** [`SS3_PartB.ipynb`](SS3_PartB.ipynb)
**Final method:** Random Forest classifier (the model chosen in SS2)
**Target:** `activated_30d` — did a newly registered account make a qualifying first deposit
within 30 days of registration?

This README explains how the notebook applies the SS2 method to the **newly received STADIOEquities
client data**, and where each required component lives.

---

## How to run

```bash
pip install -r requirements.txt
jupyter notebook SS3_PartB.ipynb      # then Run All
```
Run the notebook **from the repository root** so the relative data path resolves (the first code
cell also searches a few sensible locations automatically). The notebook runs top-to-bottom with no
manual steps and takes about a minute.

## Client data

The client extract (fulfilling the SS1 data request) is committed under
[`data/client/`](data/client/) as four CSVs joined on the surrogate key `account_id`:

| File | Grain | Role |
|------|-------|------|
| `table1_account_registration_funding.csv` | one row / account | registration, KYC, onboarding, **target** |
| `table2_onboarding_first_session_events.csv` | one row / event | first-3-day behaviour (aggregated per account) |
| `table3_client_basic_information.csv` | one row / account | demographics |
| `table4_marketing_acquisition.csv` | one row / account | acquisition channel, cost, nudges |

The original client `README.md` (data dictionary + data-quality notes) is kept alongside them in
`data/client/README.md`.

## Where each component is in the notebook

The notebook is divided into five clearly-headed sections, matching the SS3 Part B rubric:

| # | Component | What it does |
|---|-----------|--------------|
| **1** | **Dataset loading** | Loads the four tables, removes 7 duplicate accounts, reports instances (2,517), classes (2) and imbalance (~43% activated). |
| **2** | **Dataset preprocessing** | Cleans messy categoricals (whitespace/casing), engineers behavioural features from the event log, drops **leakage** columns and the fairness-sensitive `age`, and makes a **60/20/20 train/validation/test** split. Each choice is justified in a markdown block. |
| **3** | **Model training** | Trains the **Random Forest** (SS2 method); `max_depth` and `min_samples_leaf` are selected on the **validation** set; hyper-parameters are justified and aligned with SS2. |
| **4** | **Model validation** | Applies the model to the **held-out, unseen test set**; reports accuracy, balanced accuracy, precision, recall, F1, ROC-AUC and PR-AUC; confirms no leakage and ties results back to the business problem. |
| **5** | **Results visualisation** | Class balance, train-vs-test metric comparison, confusion matrix, ROC and PR curves, and feature importances. |

## Key design decisions (aligned with SS1 & SS2)

- **Leakage control.** `first_deposit_timestamp`, `first_deposit_amount`, `qualifying_deposit_flag`
  and `account_status` are dropped — they are outcome-building or measured after the window. This
  repeats the SS2 discipline of dropping the leaky `duration` feature and addresses risk **R2** in
  the SS1 RAAIDD log.
- **Fairness / POPIA.** `age_at_registration` is deliberately excluded from the model, as the client
  README flags it as a fairness-sensitive attribute.
- **No look-ahead.** Behavioural features use only the first-3-day event window supplied by the client.

## Headline result (unseen test set)

Random Forest — **ROC-AUC ≈ 0.90**, **recall ≈ 0.98**, **F1 ≈ 0.82**, **balanced accuracy ≈ 0.83**.
The strongest predictors are onboarding completion and KYC verification — actionable, non-leaky
signals the growth team can use to target onboarding support at accounts likely to stall.


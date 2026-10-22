# STADIOEquities — Early Account Activation: Data Extract

**Four years of registrations, September 2022 to July 2026** — matching the four years of app and web history — with every account matured past its 30-day activation window. Grain is as specified: **one row per account** in tables 1, 3 and 4; **one row per event** in table 2. `account_id` is a **surrogate key**, not a client identifier, and is the single stable join key across all four tables. Datetimes are `yyyy-MM-dd HH:mm:ss`. **All monetary amounts are integers in cents** (5000 = R50.00). Booleans are lowercase `true`/`false`.

## Files

### `table1_account_registration_funding.csv`
One row per account. Contains the target.  
Rows: 2,524

| Column | Description |
|---|---|
| `account_id` | String |
| `registration_timestamp` | Datetime |
| `registration_platform` | Categorical |
| `kyc_status` | Categorical |
| `kyc_completion_timestamp` | Datetime |
| `onboarding_steps_completed` | Integer |
| `onboarding_steps_total` | Integer |
| `onboarding_abandoned_flag` | Boolean |
| `first_deposit_timestamp` | Datetime |
| `first_deposit_amount` | Integer |
| `qualifying_deposit_flag` | Boolean |
| `activated_30d` | Boolean |
| `account_status` | Categorical |

### `table2_onboarding_first_session_events.csv`
One row per event, first 3 days after registration.  
Rows: 35,495

| Column | Description |
|---|---|
| `site_id` | Categorical |
| `account_id` | String |
| `session_id` | String |
| `event_timestamp` | Datetime |
| `event_type` | Categorical |
| `screen_feature_name` | Categorical |
| `session_platform` | Categorical |
| `session_sequence_number` | Integer |
| `event_duration_seconds` | Integer |

### `table3_client_basic_information.csv`
One row per account, captured at sign-up.  
Rows: 2,517

| Column | Description |
|---|---|
| `account_id` | String |
| `age_at_registration` | Integer |
| `province` | Categorical |
| `stated_investment_goal` | Categorical |
| `stated_risk_appetite` | Categorical |
| `preferred_language` | Categorical |

### `table4_marketing_acquisition.csv`
One row per account.  
Rows: 2,517

| Column | Description |
|---|---|
| `account_id` | String |
| `acquisition_channel` | Categorical |
| `campaign_id` | String |
| `acquisition_cost` | Integer |
| `referral_flag` | Boolean |
| `first_30day_nudges_sent` | Integer |
| `first_30day_nudge_opens` | Integer |

## Data quality notes

This is an extract from live operational systems and has **not** been cleaned. Expect:

- Missing values in optional / conditionally-populated fields
- Inconsistent casing and stray whitespace in some free-text and categorical fields
- A small number of duplicate records
- Occasional out-of-range or implausible values from data-capture errors
- Some date fields captured in inconsistent formats

**Target:** `activated_30d` in `table1_account_registration_funding.csv`.

**Issue I1 resolved — the qualifying-deposit definition.** A deposit qualifies when it is successful, of any amount above zero, and **not reversed within 14 days of settlement**. `qualifying_deposit_flag` states this per account. `activated_30d` is true only where a qualifying deposit landed within 30 days of `registration_timestamp`. A small number of accounts have a `first_deposit_timestamp` populated but `activated_30d = false` — either the deposit was reversed, or it fell outside the 30-day window. Both are deliberate, and are exactly the edge cases the definition needed to settle.

**Negative cases are fully included.** Accounts that never funded are in the extract with a null `first_deposit_timestamp` and `account_status = registered_unfunded`. They are the majority of the negative class and would be invisible if the extract were filtered to funded accounts.

**Look-ahead prevented in table 2.** Behavioural events are limited to the **first 3 days after registration**, as required. No event in that table postdates the activation decision window in a way that could leak the outcome.

**Identity fragmentation is visible, not hidden.** `session_platform` in table 2 can differ from `registration_platform` in table 1 — roughly 18% of accounts have at least one session on the other platform. `account_id` resolves them, so app and web sessions for the same account are already stitched.

**Leakage warning:** `first_deposit_timestamp`, `first_deposit_amount` and `qualifying_deposit_flag` are outcome-building fields. `account_status` is stated in the request as **validation only, not a model feature** — it is measured at extract time, long after the window.

**POPIA:** no names, identity numbers, email addresses, phone numbers or free text anywhere. Location is province only. Note that `age_at_registration` is supplied as requested but is a fairness-sensitive attribute — consider whether it belongs in the final model.

**Format:** CSV supplied for all four tables. Parquet for table 2 is available on request as preferred; the CSV is well within a workable size at this extract volume.

_Synthetic data supplied for the CAP182 capstone project. Not real client data._
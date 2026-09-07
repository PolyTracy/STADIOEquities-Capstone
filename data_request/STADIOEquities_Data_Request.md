# STADIOEquites - Data Request
**Project:** Early Account Activation Prediction
**Module:** CAP182 Capestone Project SS1
**Prepared by:** Tracy-lee (Student number: 21620896)

---

## Purpose of this request

To create a model to predict if a newly registered account will make its first deposit
By 30 days after registration, we need historical data as a part of the account (not per user), like how many logins each account has, or how many transactions each account has conducted.
Who interacted with it, how it went from the point of being picked up, what it did during its first session, etc.
Whether and when it was first funded and the client is.

Storing grain and its past.

For the account-level tables (Tables 1, 3, 4), only one row per registered account.
For the behavioural table (Table 2), keyed to `account_id`, one row per event is required from:
  The following features will be abstracted from first-session.
Please provide at least the past 4 years of registrations which corresponds to the 4 years of the app/web.
  Negative cases are absolutely necessary, as they are found in behaviour history, including accounts that *never* funded these.
Each table must have a single, stable `account_id` that is used as the join key, resolving the app and
  web sessions per account.

Data handling / privacy (POPIA)

Please include data pseudonymised – no names, no ID numbers, no email addresses, no phone numbers or
  free-text that could identify an individual. The account_id should NOT be a surrogate key, but rather a
  real client identifier.
The region at province level is enough; no street level location is needed.
Data can be provided in either CSV or Parquet format. For the behavioural event table the preferred method is parquet.
  given its volume.

---

## Table 1. The Account Registration & Funding data consists of one row for each account, and includes the target.

Name | Type | Example | Comment |
|---|---|---|---|
| Account ID | String (surrogate key) | `ACC0000481923` | Unique per account. Single key that is shared by all tables. Must not be an actual client identifier.
| Registration timestamp | String, datetime | `2024-03-11 08:42:19` | Format `yyyy-MM-dd HH:mm:ss`. Indicates the beginning of a 30-day activation period.
Registration platform (categorical) | app | Valid values: app, web.
Indicates whether KYC is complete or ongoing.Indicates the state of KYC - it can be not started, in progress, verified, abandoned or rejected.
| KYC completion timestamp | String, datetime | `2024-03-11 09:15:02` | Format `yyyy-MM-dd HH:mm:ss`. If KYC does not complete, then returns null.
Onboarding steps completed | Numeric, integer | `5` | Number of steps completed in onboarding (0 – total steps). Also provide the number of steps altogether.
Steps in onboarding flow total | Numeric, integer | `7` | Total number of steps in onboarding flow entered at that time.
Onboarding abandoned flag | Boolean | `false` | `true` if the client abandoned onboarding before it is completed.
| First deposit timestamp | String, datetime | `2024-03-14 19:03:55` | Format `yyyy-MM-dd HH:mm:ss`. If the account did not make any deposits, then this value is null. |
| First deposit amount | Numeric, integer | `5000` | Amount in **cents** (e.g. `5000` = R50.00). If there was never a deposit, then it will be null.
Boolean | true | true if the deposit was successful and not reversed and constituted a qualifying deposit. Clarifies Issue I1. |
Boolean | `true` | **Target variable.** Boolean value which is set to `true` if a qualifying first deposit was made in the last 30 days after registration, else `false`. If you can't calculate this, provide timestamps above, we will calculate for you.
Account status (current) | string, categorical | funded_active | valid values: registered_unfunded, funded_active, dormant, closed. For validation purposes only, not a feature of the model.

---

## Table 2. Onboarding & first-session behaviour (one row per event, keyed to account_id)

| "site_id" | UUID | 123e47e8-a1df-4b2e-9cde-bd426442785f | This is the unique identifier for the site. |
|---|---|---|---|
| Account ID | String | `ACC0000481923` | Foreign key to Table 1. |
Session ID | String | `SESS_9f21ab` | Groups events together in the same session.
| Event timestamp | String, datetime | `2024-03-11 08:44:07` | Format `yyyy-MM-dd HH:mm:ss`. The first 3 days after registration are strictly required (to avoid look-ahead), more is welcome.
A string or categorical event type.A string or categorical event type which could be any valid string such as screen_view, feature_use, onboarding_step, deposit_attempt, search, error etc.
Screen / feature name | String, categorical | `deposit_screen` | Name of the screen or feature that the event occurred in.
Session platform | The type of platform over which the session occurs, either a string or a categorical | app | Valid values: app, web. Facilitates solving web/app identity fragmentation.
Session sequence number | Numeric, integer | `1` | 1 = the client's first ever session, 2 = second, etc.
Event duration (seconds) – Numeric, integer; `12` – Time spent on the screen/feature, if applicable. If not tracked, then null.

---

## Table 3. Basic information about the client (one row per client; captured at sign-up)

Name | Type | Examples | More info |
|---|---|---|---|
| Account ID | String | `ACC0000481923` | Foreign key to Table 1. |
Age at registration: Numeric, integer, 29: In years. Valid range roughly 18 – 100. Care must be taken with use in relation to re: POPIA/fairness.
| Province | String, categorical | `GP` | Nine provinces: `GP`, `EC`, `FS`, `KZN`, `LP`, `MP`, `NC`, `NW`, `WC`. |
| Stated investment goal | String, categorical | `long_term_growth` | Valid values e.g. `long_term_growth`, `save_regularly`, `short_term_trading`, `learning`, `unspecified`. |
Whether the stated risk appetite is string, categorical; `moderate` | Valid values: `low`, `moderate`, `high`, or `unspecified`. |
The language the user prefers.The user's preferred language (e.g. en, af, zu, xh, which is an ISO-style code). Optional. |

---

## Table 4. *Marketing acquisition (One row per account)*

| Column name | Data type | Example | Additional information |
|---|---|---|---|
| Account ID | String | `ACC0000481923` | Foreign key to Table 1. |
| Acquisition channel | String, categorical | `paid_social` | Valid values e.g. `paid_social`, `paid_search`, `organic`, `referral`, `influencer`, `email`, `other`. |
| Campaign ID | String | `CMP_2024Q1_042` | Identifier of the campaign that acquired the account. Null for organic. |
| Acquisition cost | Numeric, integer | `18000` | Cost to acquire this account in **cents** (e.g. `18000` = R180.00). |
| Referral flag | Boolean | `false` | `true` if the account was acquired via an existing client referral. |
| First 30-day nudges sent | Numeric, integer | `4` | Count of onboarding emails/nudges sent in the first 30 days. Context for current fixed-schedule approach. |
| First 30-day nudge opens | Numeric, integer | `1` | Count of those nudges opened/engaged with. |

---

## Notes on data type choices

Data type choices follow the conventions in the IDS182 and WWD182 study guides: identifiers and
categoricals as **strings**, dates/times as **datetime strings** in `yyyy-MM-dd HH:mm:ss` format,
counts and monetary amounts as **integers** (money in cents to avoid floating-point rounding), and
yes/no fields as **booleans**. Where a column has a fixed set of valid values, these are listed in
the *Additional information* column so the data can be validated on delivery.

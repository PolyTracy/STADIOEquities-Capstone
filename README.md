# STADIOEquities Capstone Project — Early Account Activation Prediction

**Module:** CAP182 Capstone Project
**Client:** STADIOEquities (digital retail-investing platform, South Africa)
**Submissions:** SS1 — Project Proposal · SS2 — Viability Study · SS3 — Final Model on Client Data
**Author:** Tracy-lee (Student number: 21620896)

---

## SS3 — Final model on client data (quick links)

SS3 applies the **final SS2 method (Random Forest)** to the **newly received STADIOEquities client
data** to predict early account activation (`activated_30d`).

| Part | Deliverable | Link |
|------|-------------|------|
| B | Notebook — apply final model to client data | [`SS3_PartB.ipynb`](SS3_PartB.ipynb) |
| B | How-to / component guide | [`SS3_PartB_README.md`](SS3_PartB_README.md) |
| B | Client data extract | [`data/client/`](data/client/) |
| C | Presentation deck | [`presentation/SS3_PartC_Presentation.pptx`](presentation/SS3_PartC_Presentation.pptx) |
| C | Speaker script & recording guide | [`presentation/SS3_PartC_Speaker_Script.md`](presentation/SS3_PartC_Speaker_Script.md) |
| C | **Video presentation** | https://youtu.be/vZkZuEcCPlc|

**Headline result (unseen test set):** Random Forest — ROC-AUC ≈ 0.90, recall ≈ 0.98, F1 ≈ 0.82.
Run with `pip install -r requirements.txt` then open `SS3_PartB.ipynb` and *Run All* from the repo root.

> **Part D (client Q&A on GitHub)** is completed separately — its questions are only posted after the
> submission deadline. Enable GitHub **Discussions** to earn Part D marks.

---

## SS2 — Viability study (quick links)

SS2 proves the modelling approach on a **public dataset** (UCI Bank Marketing —
predicting term-deposit subscription, the public analogue of account activation)
before requesting STADIOEquities' sensitive data.

| Part | Deliverable | Link |
|------|-------------|------|
| A | Related work + dataset description (report) | [`literature_review/SS2_Related_Work.pdf`](literature_review/SS2_Related_Work.pdf) |
| B | Preprocessing | [Preprocessing.MD](Preprocessing.MD) |
| B | Feature engineering | [FeatureEngineering.MD](FeatureEngineering.MD) |
| B | Model 1 — Logistic Regression | [Model1.MD](Model1.MD) |
| B | Model 2 — Random Forest | [Model2.MD](Model2.MD) |
| C | Model 1 performance | [Model1Performance.MD](Model1Performance.MD) |
| C | Model 2 performance | [Model2Performance.MD](Model2Performance.MD) |
| C | Model comparison | [Comparison.MD](Comparison.MD) |
| D | Recommendations (report) | [`reports/SS2_Recommendations.pdf`](reports/SS2_Recommendations.pdf) |

**Run the full pipeline** (see [requirements.txt](requirements.txt)):
```bash
pip install -r requirements.txt
python scripts/model1_logistic_regression.py   # Model 1 + metrics/figures
python scripts/model2_random_forest.py          # Model 2 + metrics/figures
python scripts/comparison.py                     # comparison table + curves
```
Code lives in [`scripts/`](scripts/); results and figures are written to
[`experiments/results/`](experiments/results/). **Headline result:** Random Forest
is the stronger model (ROC-AUC 0.813 vs 0.801; F1 0.503 vs 0.468).

---

## Table of contents (SS1)

1. [Motivation (Part A)](#1-motivation-part-a)
2. [Problem statement (Part B)](#2-problem-statement-part-b)
3. [Repository structure (Part D)](#3-repository-structure-part-d)
4. [RAAIDD log (Part E)](#4-raaidd-log-part-e)
5. [Data request (Part C)](#5-data-request-part-c)

---

## 1. Motivation (Part A)

STADIOEquities has succeeded at the hard, expensive job of acquisition: roughly **2.3 million
registered accounts** on the promise that anyone can own a fraction of the market for the price
of a cup of coffee. Yet the company's own information pack is blunt about where that success
stops. **41% of registered accounts have never deposited a cent**, and the sign-up → first-deposit
conversion rate has fallen from **64% two years ago to 59% today**. Because the platform "earns
almost nothing from an empty account," this gap between *registering* and *funding* is not a soft
engagement metric — it is, in the company's own words, "the entire economic model."

The financial logic makes the problem concrete. Each account costs about **R180 to acquire**, and
that spend is "recovered only if the account activates." With four in ten accounts never funding,
a large share of the marketing budget is being spent to acquire clients who never generate a
single cent of revenue across any of the platform's five revenue lines — all of which, as the pack
notes, "depend on the same thing: getting clients to fund their accounts and keep using them."
The activation gap is listed **first** among the board's 2030 strategic priorities ("Activate the
accounts we already have") and **first** among the headwinds leadership returns to most often
("The activation gap … the funnel leaks worst right after registration").

Crucially, the briefing pack tells us the drop-off is **not random**: it "clusters by how the
client arrived, how far they got in onboarding, what they did in their first session and how long
the first deposit took." In other words, the very signals that separate an account that is about
to fund from one that is about to disappear are *already being recorded* — STADIOEquities "records
the full journey — every screen viewed, every deposit, every trade, every abandoned sign-up step."
Despite this, "the onboarding emails and nudges currently go out on a fixed schedule to everyone,
blind to who is about to activate and who is about to disappear." The company is, in its own
phrase, **"data rich, insight poor."**

This project adds value by closing exactly that loop. If STADIOEquities can reliably predict, in
the days immediately after registration, which accounts are likely to fund and which are likely to
stall, then the fixed-schedule blanket nudges can be replaced with **targeted, timely intervention**
— reserving costly, high-touch onboarding (personal prompts, incentives, assisted KYC) for the
accounts most at risk of never funding, and avoiding wasted contact with those who will activate
anyway. Given the scale of the base, even a **small lift in the conversion rate** translates into a
large number of newly funded accounts and a materially better return on the acquisition spend
already committed. The work is directly relevant to STADIOEquities' present state — a leaking
funnel, rising KYC abandonment (13% → 18%), and a marketing engine that acquires far faster than
it activates — and it uses data the platform already holds, making it both high-impact and
achievable within the tools of this capstone.

---

## 2. Problem statement (Part B)

STADIOEquities cannot currently predict which newly registered accounts will convert into funded,
active clients, and which will stall without ever depositing. As a result, onboarding
communication is delivered on a fixed schedule to every new registration regardless of intent,
while **41% of accounts never fund** and sign-up → first-deposit conversion has declined from 64%
to 59% over two years. The people affected are STADIOEquities' **growth, marketing and product
teams** — who are spending an R180-per-account acquisition budget without a way to protect its
return — and, ultimately, the **first-time investors** who register but are never effectively
guided across the funding threshold.

The knowledge gap is this: although the platform records the full onboarding journey (acquisition
channel, KYC progress, first-session behaviour and deposit timing), it has no model that turns
those signals into an early, per-account estimate of activation likelihood. **Which registration,
onboarding and first-session characteristics distinguish accounts that make a first deposit from
those that do not, and can these signals predict — within the first few days after registration —
whether a given account will fund within 30 days?**

This project will address that gap by developing a **supervised binary classification model** whose
target is whether a registered account makes its first qualifying deposit within **30 days of
registration** (`activated` = 1 / 0). The model will be trained on historical account-level data
covering acquisition channel and campaign, KYC and onboarding step completion, first-session app
and web behaviour, and client demographics captured at sign-up (detailed in the
[Data Request](data_request/STADIOEquities_Data_Request.pdf)). Predicted activation probabilities
can then be used to prioritise onboarding interventions toward the accounts most likely to stall,
replacing the current one-size-fits-all schedule. Success will be evaluated with classification
metrics appropriate to an imbalanced, decision-driving target — primarily **recall and precision on
the "will not activate" class, F1-score, and ROC-AUC** — validated on a time-based hold-out set so
that performance reflects the platform's changing behaviour over time.

---

## 3. Repository structure (Part D)

There is no data or code committed yet at proposal stage; the structure below is scaffolded so that
every artefact required across the capstone has a clearly documented home. Empty folders are held
in version control with `.gitkeep` files and each carries a short `README.md` describing its
purpose.

```
STADIOEquities-Capstone/
├── README.md                     # This file: Motivation, Problem statement, Repo structure, RAAIDD log
├── .gitignore                    # Excludes large data files, secrets, and environment artefacts
│
├── data/                         # DATASETS (raw is never edited; see data/README.md)
│   ├── raw/                      #   Data as received from STADIOEquities (read-only)
│   ├── processed/                #   Cleaned, feature-engineered, model-ready datasets
│   └── external/                 #   Any supplementary/reference data
│
├── data_request/                 # Part C deliverable
│   └── STADIOEquities_Data_Request.pdf
│
├── models/                       # MODELS: serialised trained models and model cards
│
├── experiments/                  # EXPERIMENTAL SETUP & RESULTS
│   ├── setup/                    #   Experiment configs, train/test split definitions, run parameters
│   └── results/                  #   Metrics, evaluation outputs, confusion matrices, logs
│
├── scripts/                      # REUSABLE CODE
│   ├── stats/                    #   Statistical helper & model-comparison scripts
│   └── visualisation/            #   Visualisation scripts (EDA and results figures)
│
├── notebooks/                    # Exploratory and analysis notebooks (EDA, prototyping)
│
└── docs/                         # Supporting documentation (data dictionary, decisions, notes)
```

**Mapping to the SS1 Part D required artefacts:**

| Required artefact | Location in this repository |
|---|---|
| Datasets | `data/` (`raw/`, `processed/`, `external/`) |
| Models | `models/` |
| Experimental setup | `experiments/setup/` |
| Experimental results | `experiments/results/` |
| Statistical helper and comparison scripts | `scripts/stats/` |
| Visualisation scripts | `scripts/visualisation/` |

> **Lecturer access:** the lecturer (`mia-gerber-stadio`) has been invited as a collaborator so the
> repository and its commit history are visible. The repository link has been posted in the Canvas
> text-entry box for this assignment.

---

## 4. RAAIDD log (Part E)

All entries are specific to the STADIOEquities early-activation prediction project.

### Risks — *Unexpected possibilities that could compromise successful completion of the project.*

| # | Risk | Why it matters to this project |
|---|------|--------------------------------|
| R1 | **Class imbalance in the activation window.** With conversion at ~59% overall but likely far lower inside a tight 30-day window (and 41% never funding), the "will not activate" class may dominate or be under-represented depending on window definition, biasing a naïve classifier toward the majority class. |
| R2 | **Label leakage.** Fields generated *after* or *because of* funding (e.g. first-trade date, balance, premium take-up) could leak the outcome into the features and inflate performance, then fail in production where those fields don't yet exist at scoring time. |
| R3 | **Identity fragmentation.** The pack notes identity "spans app and web sessions." If behavioural events cannot be reliably stitched to a single account, first-session features will be incomplete or wrong, weakening the model. |
| R4 | **Concept drift.** Conversion has already moved 64% → 59% in two years; a model trained on older behaviour may not generalise to current registrations, degrading silently over time. |
| R5 | **Regulatory / fairness risk (POPIA).** Using demographic fields (age, region) to decide who gets onboarding support could introduce unfair discrimination or breach POPIA if handled carelessly. |
| R6 | **Data delivery risk.** The project cannot start modelling until STADIOEquities fulfils the Part C data request; incomplete or delayed data delivery would compress the modelling timeline. |

### Actions — *Tasks to be done throughout the project's lifecycle.*

| # | Action |
|---|--------|
| A1 | Submit the Part C data request and confirm the account-level grain, join keys and history depth with the client. |
| A2 | Perform exploratory data analysis (EDA): distributions, missingness, funnel drop-off by channel and onboarding step, base activation rate. |
| A3 | Formally define the target: `activated` = first qualifying deposit within 30 days of registration; document the rule in `docs/`. |
| A4 | Engineer features strictly from information available *at or before* the scoring point (acquisition, KYC progress, first-session behaviour, demographics). |
| A5 | Create a **time-based** train/validation/test split to respect drift and avoid look-ahead bias. |
| A6 | Train and compare candidate algorithms (e.g. logistic regression, decision tree, KNN) and select on recall/precision/F1/ROC-AUC. |
| A7 | Build statistical helper and comparison scripts (`scripts/stats/`) and visualisation scripts (`scripts/visualisation/`). |
| A8 | Document the repository, data dictionary and model card; commit regularly with meaningful messages. |

### Assumptions — *Conditions assumed to be true, but currently unproven.*

| # | Assumption |
|---|------------|
| AS1 | Historical registration and onboarding behaviour is representative of future registrations well enough for a model to generalise. |
| AS2 | The registration timestamp and first-deposit timestamp are accurate and reliable enough to define the 30-day activation label. |
| AS3 | Behavioural, funding and demographic records can be joined to a single, stable account identifier despite app/web session fragmentation. |
| AS4 | A 30-day window is a business-meaningful definition of "activation" for STADIOEquities' economics and intervention cadence. |
| AS5 | The data STADIOEquities provides in response to the Part C request is complete and covers the stated history depth. |

### Issues — *Problems that transpire throughout the problem's lifecycle.*

| # | Issue |
|---|-------|
| I1 | The exact business definition of a "qualifying deposit" (minimum amount? excludes reversed/failed deposits?) is not yet confirmed with the client and must be resolved before the target can be finalised. |

### Decisions — *Choices that you (and stakeholders) make throughout the project.*

| # | Decision |
|---|----------|
| D1 | Scope the capstone on **early account activation** (over dormancy, segmentation or compliance), because it is STADIOEquities' first-ranked strategic priority and its largest source of wasted spend, and it is framed cleanly as a supervised binary classification problem suited to this module's algorithms. A 30-day prediction window and a recall-focused evaluation approach were chosen to match the intervention use case. |

### Dependencies — *Relationships between actions that indicate the chronology of completion.*

| # | Dependency |
|---|------------|
| DP1 | Modelling (A2–A6) depends on the Part C data request being fulfilled (A1). |
| DP2 | Feature engineering (A4) depends on EDA (A2) and the finalised target definition (A3), which in turn depends on resolving Issue I1. |
| DP3 | Model training and comparison (A6) depends on the time-based split (A5) and the engineered feature set (A4). |
| DP4 | Evaluation and model selection depend on the helper/comparison scripts (A7). |
| DP5 | Committing artefacts and inviting the lecturer (A8) depends on the repository being created and structured (Part D). |

---

## 5. Data request (Part C)

The full, formatted data request is provided as a PDF in this repository:
**[`data_request/STADIOEquities_Data_Request.pdf`](data_request/STADIOEquities_Data_Request.pdf)**.

---

*This proposal was prepared for the CAP182 Capstone module. Client facts and figures are drawn from
the STADIOEquities Company Information Pack.*

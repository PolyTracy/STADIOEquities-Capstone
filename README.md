# STADIOEquities Capstone Project — Early Account Activation Prediction

**Module:** CAP182 Capstone Project
**Client:** STADIOEquities
**Submission:** SS1 Project Proposal
**Author:** Tracy-lee (Student number: 21620896)

---

## Table of contents

1. [Motivation (Part A)](#1-motivation-part-a)
2. [Problem statement (Part B)](#2-problem-statement-part-b)
3. [Repository structure (Part D)](#3-repository-structure-part-d)
4. [RAAIDD log (Part E)](#4-raaidd-log-part-e)
5. [Data request (Part C)](#5-data-request-part-c)

---

##1. Motivation (Part A)
STADIOEquities has performed a highly challenging and expensive task in the process of acquisition: to acquire 2.3 million registered accounts by allowing anyone to own a piece of the market for the price of a cup of coffee. But the company's own information pack doesn't get all that much subtle when it comes to where that success ends. Just 41% of registered accounts have deposited and the registered-to-first-deposit rate has fallen from 64% two years ago to 59%. That's a discrepancy between registering and funding that's not a soft measure of engagement, in the company's own words, it's the "whole economic model.

The issue comes real when anyone thinks of money. The cost of each account is approximately R180 and the money is "recovered only if the account activates. A staggering 40% of accounts aren't funded at all, and a big portion of the marketing budget is being used to get clients to fund accounts and encourage continued usage all of which "depend on the same thing: getting clients to fund their accounts and keep using them," says the pack. The activation gap also falls in the board's list of the 2030 strategic priorities, and is among the top 15 board-paused items when they rate their leads and followers ('The activation gap – the funnel leaks worst right after sign-up').

Importantly, the briefing pack provides information as to how the drop-off is not random; it 'clusters by how the client arrived, how far they got in onboarding, what they did in their first session and how long the first deposit took.' All of this means that the onboarding emails and nudges are being sent regularly to all users, irrespective of whether they are set to become active or inactive. It's a company that's “data rich, insight poor,” says the company in its own words.

This project fills just that gap. The onboarding can be personalized and costly, and can include personal prompts, incentives, assisted KYC etc., and will be useful for accounts that have a low chance of funding, with targeted, timely nudges (not blanket nudges) being offered to those that have a good chance of funding; the days after registration can be used for knowing which accounts are likely to fund and which are not. Even a small bump in conversion rate translates to a real boost in the number of accounts funded, and return on investment from the acquired investment. The work is directly relevant because it is relevant to the current situation that STADIOEquities is a leaking funnel, KYC abandonment is on the rise (13% to 18%) and their marketing engine is working at a faster pace than they are getting it done.

##2. A problem statement (Part B)
STADIOEquities cannot accurately forecast which accounts that are newly registered will turn into funded, active clients and which will languish without depositing any funds. As a result, onboarding communication is pushed to all new signups, regardless of intent, and the conversion rate for signups to deposits has decreased from 64% to 59% in two years for all accounts.This means that onboarding communication is sent to everybody that signs up, regardless of having an intent, and over two years, sign up-to-first deposit conversion fell from 64% to 59% for all accounts. The individuals involved are the growth team, marketing team, product team, they're spending R180 per person on an acquisition budget, but they don't really have anything to protect the return on their investment, and the first-time investors who register, but then are not walked across the funding line.

That is, the platform stores all the stages of the process of becoming an activated player (acquisition channel, KYC progress, player activity during the first session, the timing of the first deposit), but there is no model that can provide a preliminary assessment of the probability of activation, player by player. What makes accounts that do make their first deposit different from accounts that don't make the first deposit, and can these differences be captured within the first few days after account registration to determine if a given account will make its first deposit within the next 30 days?## 3. The structure of the repository (Part D)
 
At proposal stage there is no data or code committed – the structure below is scaffolded so that
It is known that each artefact has a known home throughout the capstone. Folders with no contents are retained.
Have a short README.md file for each describing how they use their version control system, and include .gitkeep files.
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
 
For this mapping to the SS1 Part D: artefacts are needed:
 
The artifact is required. | The position of the artifact in this repository. |
|---|---|
| Datasets | `data/` (`raw/`, `processed/`, `external/`) |
| Models | `models/` |
| Experimental setup | `experiments/setup/` |
| Experimental results | `experiments/results/` |
Scripts to help with statistics and comparison.Scripts to assist with statistics and comparison.
| Visualisation scripts | `scripts/visualisation/` |
 
 
 
##4. RAAIDD log (Part E)
 
All entries are to be for the prediction project STADIOEquities early-activation.
 
 Risks - Unexpected possibilities that could compromise successful completion of the project.
 
The project is at risk | This project is a risk for the following reasons: |
|---|------|--------------------------------|
R1 | Class imbalance in activation window. The "will not activate" class may be heavily or underrepresented in a short time window (say, 30 days) and even more underrepresented in a very short time window (say, 12 hours) and, given the high percentage of “will not activate” and the low percentage of “will activate” that is likely a biased class (biasing a naïve classifier toward the majority class), depending on the definition of the time window.
| R2 | Label leakage. Generated fields (e.g. firstTradeDate, balance, premiumTakeUp) after/as a result of funding may leak into the features and impact on performance at runtime in production, but may not be present at scoring time.
| R3 | Identity fragmentation. Pack notes are "spans app and web sessions. Inconsistencies and/or omissions of first session features will result in incomplete or incorrect models, which will significantly weaken the model.
| R4 | Concept drift. A model that was trained on the past behaviour


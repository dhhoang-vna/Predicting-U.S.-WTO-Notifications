# Predicting Restrictive U.S. SPS/TBT Notifications

## Overview
This repository contains the data, code, and outputs for my Big Data / NLP term poster on whether the text of U.S. SPS/TBT notifications predicts import-reducing outcomes for Southeast Asian exporters.

## Repository structure
- `data/`: raw and cleaned data
- `code/`: scripts for cleaning, modeling, and analysis
- `fig/`: figures and tables
- `poster/`: poster PDF and appendix

## Main files
- Poster: `poster/poster.pdf`
- Main training script: `code/5_analysis_master.ipynb`
- Replication order: see below

## Replication steps
1. Install packages from `requirements.txt`
2. Place raw data in `data/raw/`
3. Run:
   - `1_notifs_data.ipynb`
   - `2_usitc_data.ipynb`
   - `3_merging.ipynb`
   - `4_labeling.ipynb`
   - `5_analysis_master.ipynb`
   - `6_IO_extension.ipynb`
   - `7_robustness_outcome.ipynb`
4. Main outputs are saved in `data/cleaned_data/` and figures in `fig/`.

## Data sources
- ePing WTO SPS/TBT notifications
- US International Trade Commission import data
- IO exposure data from Mancini et al. (2024), which is computed from different sources (ADB, WIOD, OECD TiVA, etc.)
- Concordance from Liao et al. (2022)

## Author
Hung D. Hoang
Université Paris 1 Panthéon-Sorbonne

# Progress Log

## 2026-11-21
- Done: Phase 0 + Phase 1.
  - Phase 0: pivoted Project 2 from the fake review detector to an intent-aware product discovery engine (fashion search + cold-start recommendations on H&M data); charter in docs/01-charter.md
  - Phase 1: created the repo, folder structure, Python 3.13 virtual environment, pinned requirements.txt, .gitignore rules (data, CLAUDE.md, model/index files), .env + .env.example
- Finding:
  - Pivot reason: wanted the project to match the e-commerce problems I'd discuss in my Depict interview (first week of Jan)
  - Used Python 3.13, not my default 3.14, since ML libraries (PyTorch, FAISS) lag on new Python versions. Docker will use the same version.
  - pip installed nothing the first time because requirements.txt wasn't saved. Turned on auto-save.
  - Verified .env is ignored with git check-ignore (.gitignore line 153) before the first commit


## 2026-11-22
Done: downloaded data (official source), read the license, EDA notebook, EDA report, data README, charter license update
Finding: top-12 overlap 0/12 → recent-popularity baseline; cold start = 3.98% of final-week purchases; split dates decided; pyarrow reader drops leading zeros


## 2026-11-23
- Done: Phase 2 Steps 3–4
  - src/prepare_data.py: kept the last 12 weeks of purchases (3,386,963, 10.7% of all) and built one search_text per product (105,542 products, 0 empty, median 34 words)
  - src/split_data.py: train 2,891,411 (Jul 1 – Sep 8) / val 255,241 (Sep 9 – 15) / test 240,311 (Sep 16 – 22), test saved to data/processed/locked/
- Finding:
  - Only ~39% of the catalog (40,772 of 105,542) was bought in the last 12 weeks
  - Learned argparse (command-line options) and pandas' & for combining conditions
  - Committed to main by accident; fixed by creating the branch from that commit and moving main back with git branch -f


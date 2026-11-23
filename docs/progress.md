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



11/22/2026
Done: downloaded data (official source), read the license, EDA notebook, EDA report, data README, charter license update
Finding: top-12 overlap 0/12 → recent-popularity baseline; cold start = 3.98% of final-week purchases; split dates decided; pyarrow reader drops leading zeros
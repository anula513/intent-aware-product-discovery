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
  - Timeline: ~20 hrs/week isn't enough for everything before the interview, so fine-tuning, the final test eval, and the A/B test moved to after it
- Next: Phase 2: download the H&M dataset from Kaggle, explore it (EDA), then subsample and do the time-based split
- Blockers: none
- AI usage: Claude drafted the charter (I reviewed it section by section), wrote the .gitignore project rules and pinned versions at my request, and explained each concept and command. I ran all commands and made the decisions (pivot, Python version, timeline).
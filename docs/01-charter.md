# Project Charter: Intent-Aware Product Discovery Engine

**Author:** Anula Dinesh
**Type:** Solo portfolio project
**Status:** Phase 0 (framing)
**Date:** 2026-11-21

> Targets in this charter are proposals made before looking at any data.
> If a target changes, I record the old value, the new value, and the
> reason in docs/progress.md.

---

## 1. Problem
Shoppers often know the aesthetic they want but not what the item is called, so they describe it in their own words ("flowy dress for my Spain trip, no black"), but most store search engines only match keywords. Product text rarely contains the shopper's words, and keyword search can't handle intent, occasions, or exclusions, so results are irrelevant and high-intent shoppers leave. Recommendations have a second gap: "customers also bought" needs purchase history, so new arrivals, which fast-fashion brands release every week, have no history and don't get recommended. Large retailers solve both with massive data and big ML teams. Small and mid-size fashion stores have neither.

## 2. Users
- **End user: the shopper.** Someone on a fashion store's site who types what they mean and wants relevant products in the first screen of results.
  > "A shopper packing for a Spain trip wants to describe the look in plain words and see matching items immediately, so that they don't give up and leave the site."
- **Customer (who would pay): the store's e-commerce / merchandising team.** They want more searches turning into purchases and new arrivals actually getting seen.

v1 is built and evaluated for the shopper. The store's view appears only as the metrics page.

## 3. Solution
A search and recommendation engine over a real fashion catalog (H&M), with a web UI. The system:
1. **Understands the query.** An LLM agent turns natural language into structured filters (category, color, exclusions) plus a search phrase.
2. **Searches by meaning.** Hybrid retrieval: BM25 keyword search + embedding search (text, plus CLIP image embeddings), combined with reciprocal rank fusion.
3. **Recommends similar items**, including new items with zero purchase history (cold start), using content and image similarity.
4. **Explains** each result in one line, and shows the user how it understood the query ("Here's what I understood" chips).
5. **Guards its output.** Code checks that every product ID the agent returns exists in the catalog and that no result violates an explicit exclusion.
6. Served through **FastAPI**, packaged with **Docker**, **deployed** with a rate limit and spend limit, with latency/cost logging and a **Streamlit** UI, including a side-by-side "keyword vs engine" demo mode.
7. **Catalog-agnostic.** The catalog is one swappable input. H&M data is used privately for all training and evaluation; the **public demo runs on a separate, openly licensed fashion catalog**, because H&M's terms don't allow redistribution (decided 2026-11-21, see Section 7).

## 4. What this project can and cannot claim
**Data:** H&M Personalized Fashion Recommendations (Kaggle): product metadata and images, customers, and about two years of transactions. Exact sizes are confirmed in Phase 2.

**Can claim (once measured):**
- How retrieval methods compare on my eval query set (BM25 vs embeddings vs hybrid vs fine-tuned).
- How recommendation methods compare on a held-out future week of real H&M purchases, overall and for cold-start items.
- How often the agent extracts filters correctly, and that invalid IDs / exclusion violations were checked by code.
- What real users preferred in a blind A/B test (small sample, stated as such).

**Cannot claim:**
- Revenue or conversion impact. Offline metrics are not live business results.
- That search results match how real H&M shoppers search. H&M did not release search queries; my queries are LLM-generated from product attributes, with a hand-checked sample.
- Real prices. Prices in the dataset are scaled, so "under $50" style filters are out of scope.
- Results on other stores, languages, or product categories outside the dataset.
- Metrics for the public demo catalog. All reported numbers come from H&M; the demo catalog has no purchase history, so it is for demonstration only.

## 5. Scope
**In scope (v1)**
- Data: EDA, subsampling, cleaning, time-based split (train / val week / test week). **The test week and test queries stay locked until the final evaluation.**
- Eval query set: ~300 LLM-generated shopper queries with attribute-based relevance, split into dev and test, with ~50 hand-checked
- Search: BM25 baseline, text embeddings, CLIP image-text embeddings, FAISS index, hybrid with reciprocal rank fusion
- Fine-tuning a text embedding model on (query, product) pairs in Google Colab
- Recommendations: popularity baseline, co-purchase ("bought together"), content/image similarity for cold start
- Agent with tool calling: `search_catalog`, `get_similar_items`, `explain_match`
- FastAPI endpoints with input limits and honest errors (422 / 502 / 503)
- Tests I write myself (unit tests for metrics and retrieval + API tests with mocking)
- Docker, deployment with rate limit + spend limit, latency/token/cost logging
- Streamlit UI: search, product page with similar items, side-by-side demo mode, metrics page
- Blind A/B with real users, feedback recorded
- README I write myself, including "How I used AI" and "Limitations"
- Public demo catalog: choose an openly licensed fashion catalog and verify its license on the original source page (Week 5)

**Out of scope (v1)**
- Personalization per logged-in customer (user accounts, history-based ranking for a specific user)
- Live store integration (Shopify plugin, real traffic)
- Real-price filtering
- Training a model from scratch
- Non-English queries

**Stretch (only after everything in scope is done)**
- A reranker (cross-encoder) on top of hybrid retrieval
- Using query spelling correction / synonyms
- Comparing my MAP@12 against the public competition leaderboard, with the differences in setup stated

## 6. Success metrics
Every number gets labeled by its split:
- **Dev queries / Val week**: for choosing methods and settings.
- **Test queries / Test week**: touched **once**, at the end.
- **Cold-start**: items with no purchases before the test week.

| # | Metric | Target (proposal) | Split | How measured |
|---|--------|-------------------|-------|--------------|
| 1 | BM25 search recall@10 and NDCG@10 | No target. The bar to beat | Dev, then Test | My metric functions (unit-tested) |
| 2 | Hybrid search recall@10 | Beats BM25 and beats either single method on dev | Dev, then Test | Same script, same queries |
| 3 | Fine-tuned vs off-the-shelf embeddings | Report the change, positive or not | Dev, then Test | Same script, same queries |
| 4 | Results violating an explicit exclusion ("not black") | 0 | Test queries | Code checks every returned item's attributes |
| 5 | Agent filter-extraction accuracy | ≥ 85% | ~50 hand-labeled queries | Compare extracted filters to my labels |
| 6 | Invalid product IDs returned by agent | 0 | All agent eval runs | Code checks IDs against the catalog |
| 7 | Recommendations MAP@12: popularity vs co-purchase vs content | No target for baseline; best method beats popularity | Val week, then Test week | Real purchases in the held-out week |
| 8 | Cold-start MAP@12 / recall@12 | No pass/fail target. Measured and reported vs popularity | Test week, cold-start items | Same as #7, restricted to new items |
| 9 | Latency (p95) | Search ≤ 1 s; full agent request ≤ 6 s | Deployed app | Logged per request |
| 10 | Cost per agent request | ≤ $0.005 | Deployed app | Tokens × price, logged per request |
| 11 | Blind A/B preference | Reported, with sample size (target ≥ 10 users) | Real users | Users pick the better of two unlabeled result columns |
| 12 | Delivery | Public URL, rate + spend limit on, tests pass | — | Live link, pytest output |

## 7. Risks and mitigations
| Risk | Why it matters | Mitigation |
|------|----------------|------------|
| Synthetic queries are generated from product text, so they share words with it | BM25 looks unfairly good, or the eval is circular | Generate queries in shopper language (paraphrased, no copied attribute words); hand-check ~50; report the limitation |
| Leakage: using future purchases to predict the test week | Inflated recommendation scores | Strict time-based split; all features built from training weeks only |
| Test contamination (happened in Project 1 with held-out question h6) | Numbers stop being honest | Test queries and test week locked until final eval; tuning only on dev/val |
| Dataset size (tens of millions of transactions, many GB of images) | Laptop/Colab crashes, slow iteration | Subsample by time window and product set; embed images in Colab, save vectors |
| Dataset license / image rights | **Confirmed 2026-11-21:** H&M data is for non-commercial use and academic research only and may not be redistributed (Kaggle rules, section 7) | Never commit raw data or notebook outputs; eval files store only my synthetic queries + product IDs; public demo uses a separate openly licensed catalog |
| Popularity baseline is very strong in fashion | "Fancy" methods may not beat it | Report honestly; that's a valid finding |
| LLM agent misreads queries or invents products | Wrong results, broken trust | Structured outputs, ID check (#6), exclusion check (#4) |
| API credits burned by strangers | Real money | Spend limit on provider, rate limit + input limits on the API |
| Colab GPU limits / disconnects | Lost training runs | Small models, checkpoints saved to Google Drive |
| Timeline slip (Project 1 deploy landed ~3 weeks late) | Deploy and eval skipped again | Rule: cut stretch work (CLIP extras, reranker), never deploy or eval |

## 8. Timeline
**Pace:** up to 2 hours per weekday and up to 5 hours per weekend day, about 20 hours per week. If winter break frees up more weekday time, the extra goes to buffer, not new features.

**Hard date:** Depict CEO interview, first week of January 2027 (exact date TBD). Everything marked "interview-critical" must be live by **Jan 1**.

| Week | Dates | Phases | Interview-critical? |
|------|-------|--------|---------------------|
| 1 | Nov 21 - Nov 27 | 0 Framing, 1 Setup, 2 Data (EDA, subsample, time split). Thanksgiving week, lighter | Yes |
| 2 | Nov 28 - Dec 4 | Eval query set, metric functions + tests, BM25 + popularity baselines, **first dev/val numbers** | Yes |
| 3 | Dec 5 - Dec 11 | Text embeddings, FAISS, hybrid search, co-purchase recs. Finals, lighter | Yes |
| 4 | Dec 12 - Dec 18 | CLIP image embeddings, content-based recs, cold-start eval (val week), error analysis | Yes |
| 5 | Dec 19 - Dec 25 | 6 Agent (filters, exclusions, ID check), 7 FastAPI, 8 Tests | Yes |
| 6 | Dec 26 - Jan 1 | 9 Docker, 10 Deploy, 11 Logging, 12 Streamlit with side-by-side demo, short README | Yes |
| Interview week | Jan 2 - ~Jan 8 | 2-minute walkthrough, demo rehearsal, likely questions | Yes |
| After interview | January | 4 Fine-tuning, **final test-set evaluation** (once, after fine-tuning), 13 blind A/B with real users, 14 full README, 15 resume bullets | No |

**Why the final test evaluation waits until after fine-tuning:** the test set is used once. If it were used in December and fine-tuning came later, the fine-tuned model would need a second look at the test set. So the interview demo uses **dev/val numbers, labeled as dev/val**, and the locked test numbers come in January.

**If a week slips:** cut in this order: CLIP extras → co-purchase recs → agent explanation line. Never cut: the baselines, the eval, the deploy, or the side-by-side demo.

## 9. Tech stack
- **Python, pandas:** data work
- **rank_bm25:** keyword baseline
- **sentence-transformers (Hugging Face):** text embeddings + fine-tuning
- **CLIP (Hugging Face):** image-text embeddings
- **FAISS:** vector index
- **Google Colab GPU:** embedding images, fine-tuning
- **LLM API with tool calling:** agent (same provider as Project 1 unless there's a reason to switch)
- **FastAPI + pydantic:** API and input validation
- **pytest:** tests (I write them)
- **Docker:** packaging
- **Render (or similar):** deployment
- **Streamlit:** UI
- **Git + GitHub:** feature branches, merged to main the same day

## 10. Definition of done (whole project)
The project is done when:
- Every metric in Section 6 has a measured value, labeled with its split, in `docs/` reports
- Test queries and the test week were used once, at the end
- The app is live at a public URL with a rate limit and spend limit on
- The test suite passes, and I wrote the tests
- At least 10 real users did the blind A/B, and results + feedback are recorded
- I wrote the README, including "How I used AI" and "Limitations"
- Resume bullets use only measured numbers, each labeled correctly
- I can explain every file in the repo, and give a 2-minute walkthrough, without notes

A phase is done when: its goal works, it's committed on a feature branch and merged, progress.md is updated, and I've explained the step back in my own words.

## 11. AI usage policy
- **Claude may:** explain concepts, describe what code needs to do, review and correct code I write, help debug (after the 30-minute stuck rule), suggest wording edits.
- **Claude may not:** write my tests, write my README, or produce any number that goes on my resume.
- **LLM-generated eval queries** are labeled as synthetic everywhere they're used.
- **This charter:** first draft written by Claude at my request. I reviewed it, changed it, and can defend every line.
- Every session's AI usage is logged in docs/progress.md.
- Keys and CLAUDE.md are never committed. Raw H&M data is never committed.
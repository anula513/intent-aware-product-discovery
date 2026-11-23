# EDA Report: H&M Personalized Fashion Recommendations

**Author:** Anula Dinesh
**Date:** 2026-11-22
**Notebook:** `notebooks/01_eda.ipynb` (outputs cleared before commit: H&M data may not be redistributed, Kaggle rule 7B)
**Data:** official H&M Kaggle competition files (see `data/README.md`)

> Numbers marked ⟨fill⟩ come from the Section 4 summary of the notebook. Every number in this report was produced by code I ran on the full dataset.

---

## 1. Files

| File | Size on disk | Rows | What one row is |
|------|-------------|------|-----------------|
| articles.csv | ~34 MB | 105,542 | one product variant (e.g. one top in one color) |
| customers.csv | ~198 MB | ⟨fill⟩ | one customer |
| transactions_train.csv | ~3.25 GB | ⟨fill⟩ | one item bought by one customer on one day |

## 2. Articles (the catalog)

- **105,542 products, 25 columns.** Most attributes come in pairs: a number code (`colour_group_code`) and a readable name (`colour_group_name`). Search and the agent use the `_name` columns.
- **Leading-zero bug:** pandas reads `article_id` as a number by default and drops the leading 0 (`0108775015` → `108775015`). The notebook reads it as text and asserts every ID has 10 characters. Image files use the 10-character ID, so this matters.
- **Missing descriptions:** 416 products (0.39%) have no `detail_desc`. They can only be found by name, attributes, or image (CLIP).
- **Variants vs families:** ⟨fill⟩ product families (`product_code`) for 105,542 variants, ⟨fill⟩ variants per family on average. Several color variants of one item could fill the top 10 results, so search results may need to be grouped by family.
- **Messy names:** product names don't always match their type (e.g. "OP T-shirt (Idro)" is typed as "Bra"). Searching by meaning matters more than matching names.
- **Description length:** median ⟨fill⟩ words.

## 3. Customers

- ⟨fill⟩ customers; ⟨fill⟩ (⟨fill⟩%) bought at least once in the data.
- Missing values: ⟨fill: which columns, how much⟩.
- Quirks: ⟨fill: e.g. inconsistent categories in `fashion_news_frequency`⟩.
- Customer data matters less for v1, because per-customer personalization is out of scope (charter, Section 5).

## 4. Transactions

- **Date range:** ⟨fill⟩ to ⟨fill⟩ (~⟨fill⟩ weeks).
- **Weekly pattern:** ⟨fill: describe spikes/dips in the weekly chart⟩.
- **Purchases per customer:** median ⟨fill⟩, 90th percentile ⟨fill⟩. Most customers buy few items, which is the core difficulty for recommendations.
- **Articles:** ⟨fill⟩ bought at least once; ⟨fill⟩ never bought.
- **Duplicates:** ⟨fill⟩ exact duplicate rows (⟨fill⟩%). In this dataset, a duplicate row usually means the customer bought more than one unit of the same item that day, so duplicates are **kept**.
- **Data integrity:** ⟨fill⟩% of transactions point to a known article, ⟨fill⟩% to a known customer.
- **Price** is scaled by H&M (not dollars), so real-price filters are out of scope.

## 5. Findings that change the plan

1. **Popularity baseline:** the top-12 most-bought items overall and in the final week overlap ⟨fill⟩ of 12. ⟨If low: fashion popularity changes fast, so the baseline should be "most bought in the most recent week(s)," not "most bought ever."⟩
2. **Cold start is real:** in the final week, ⟨fill⟩ items sold for the first time, and ⟨fill⟩% of that week's purchases were on brand-new items. No method based only on purchase history can recommend these. This is the gap image/content similarity is meant to cover.
3. **Time-based split:** the test week will be the final 7 days (⟨fill⟩ to ⟨fill⟩), the validation week the 7 days before it, and training uses only the weeks before that.
4. **Subsample by time:** ~⟨fill⟩ weeks of data is far more than needed to iterate quickly. Recent weeks matter most in fashion, so the working dataset is the most recent weeks (see Phase 2, Step 3).

## 6. Limitations

- Prices are scaled; there are no search queries in the data (eval queries will be synthetic).
- The data ends in ⟨fill⟩; trends after that are unknown.
- Offline purchase data shows what people bought from what H&M showed them, not what they would have bought from a different ranking.

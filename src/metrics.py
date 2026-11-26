"""Ranking metrics for search and recommendations.

All three functions take:
    recommended: ranked list of product IDs, best first
    relevant:    set of product IDs that are correct
    k:           how many top results to look at
and return a score between 0.0 and 1.0.
"""

import math


def recall_at_k(recommended: list, relevant: set, k: int) -> float:
    """Share of the relevant items that appear in the top k recommended.

    Example: 4 relevant items, 3 of them in the top 10 → 0.75
    """
    if not relevant:
        return 0.0
    relevant_in_top_k = len(relevant & set(recommended[:k]))
    return relevant_in_top_k / len(relevant)


def ndcg_at_k(recommended: list, relevant: set, k: int) -> float:
    """Ranking quality of the top k: 1.0 = all relevant items at the very top.

    A relevant item at position p (starting at 1) earns 1 / log2(p + 1).
    Example (from day one): 2 relevant items at positions 1 and 3 → 0.92
    """
    if not relevant:
        return 0.0

    dcg = 0.0
    seen = set()
    for index, item in enumerate(recommended[:k]):     # index starts at 0, position = index + 1
        if item in relevant and item not in seen:     # count each relevant item once
            dcg += 1 / math.log2(index + 2)
            seen.add(item)

    n_ideal = min(len(relevant), k)                   # best case: relevant items fill the top slots
    ideal_dcg = sum(1 / math.log2(index + 2) for index in range(n_ideal))
    return dcg / ideal_dcg


def average_precision_at_k(recommended: list, relevant: set, k: int) -> float:
    """AP@k for one customer/query: precision at each hit, averaged.

    Walk down the top k; at every hit, precision = hits so far / position.
    Sum those, then divide by min(len(relevant), k).
    Example (from day one): bought 2 items, hits at positions 1 and 4 → (1.0 + 0.5) / 2 = 0.75
    """
    if not relevant:
        return 0.0

    hits = 0
    score = 0.0
    seen = set()
    for index, item in enumerate(recommended[:k]):
        if item in relevant and item not in seen:
            hits += 1
            score += hits / (index + 1)
            seen.add(item)
    return score / min(len(relevant), k)


def map_at_k(all_recommended: list[list], all_relevant: list[set], k: int = 12) -> float:
    """Mean of AP@k over many customers/queries (the H&M competition metric is MAP@12).

    all_recommended[i] and all_relevant[i] belong to the same customer/query.
    """
    if len(all_recommended) != len(all_relevant):
        raise ValueError("all_recommended and all_relevant must be the same length")
    if not all_recommended:
        return 0.0
    scores = [average_precision_at_k(rec, rel, k) for rec, rel in zip(all_recommended, all_relevant)]
    return sum(scores) / len(scores)
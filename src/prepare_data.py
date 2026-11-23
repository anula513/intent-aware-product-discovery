"""Phase 2, Step 3: subsample + clean the H&M data.

Reads data/raw/, writes two files to data/processed/:
  - articles_clean.parquet       the full catalog, cleaned, with one `search_text` column per product
  - transactions_recent.parquet  only the most recent N weeks of purchases

Run from the project root:
    python src/prepare_data.py            (default: 12 weeks)
    python src/prepare_data.py --weeks 8
"""

import argparse
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]   # src/ -> project root
RAW = PROJECT_ROOT / "data" / "raw"
PROCESSED = PROJECT_ROOT / "data" / "processed"

# Readable columns we keep from the catalog (the *_no / *_code duplicates are dropped)
ARTICLE_COLUMNS = [
    "article_id", "product_code", "prod_name",
    "product_type_name", "product_group_name", "graphical_appearance_name",
    "colour_group_name", "perceived_colour_master_name",
    "department_name", "index_group_name", "section_name", "garment_group_name",
    "detail_desc",
]

# The parts that make up search_text, in this order.
# BM25 and the embedding models will all search this same text, so the comparison is fair.
SEARCH_TEXT_PARTS = [
    "prod_name", "product_type_name", "product_group_name",
    "colour_group_name", "graphical_appearance_name",
    "index_group_name", "garment_group_name", "detail_desc",
]

TRANSACTION_DTYPES = {
    "customer_id": str, "article_id": str, "price": "float32", "sales_channel_id": "int8",
}


def build_search_text(articles: pd.DataFrame) -> pd.Series:
    """Join the descriptive columns into one sentence-like string per product.

    Empty parts are skipped, so a product with no description doesn't end in '. .'
    Example: "Strap top. Vest top. Garment Upper body. Black. Solid. Ladieswear. Jersey Basic. Jersey top with ..."
    """
    parts = articles[SEARCH_TEXT_PARTS].fillna("").astype(str)
    return parts.apply(
        lambda row: ". ".join(p.strip().rstrip(".") for p in row if p.strip()),
        axis=1,
    )


def prepare_articles() -> pd.DataFrame:
    articles = pd.read_csv(RAW / "articles.csv", dtype={"article_id": str})
    assert articles["article_id"].str.len().eq(10).all(), "article_id lost its leading 0!"

    articles = articles[ARTICLE_COLUMNS].copy()
    articles["detail_desc"] = articles["detail_desc"].fillna("")
    articles["search_text"] = build_search_text(articles)
    return articles


def load_transactions() -> pd.DataFrame:
    """Use the Parquet cache from the EDA notebook if it exists (seconds), else the CSV (minutes)."""
    cache = PROCESSED / "transactions_full.parquet"
    if cache.exists():
        print(f"loading cached {cache.name}")
        transactions = pd.read_parquet(cache)
    else:
        print("loading transactions_train.csv (this takes a few minutes)")
        transactions = pd.read_csv(
            RAW / "transactions_train.csv", dtype=TRANSACTION_DTYPES, parse_dates=["t_dat"]
        )
    assert transactions["article_id"].str.len().eq(10).all(), "article_id lost its leading 0!"
    return transactions


def keep_recent_weeks(transactions: pd.DataFrame, weeks: int) -> pd.DataFrame:
    """Keep only the last `weeks` full weeks, counting back from the final date in the data."""
    end = transactions["t_dat"].max()
    start = end - pd.Timedelta(days=weeks * 7 - 1)
    return transactions[transactions["t_dat"] >= start].reset_index(drop=True)


def main(weeks: int) -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)

    articles = prepare_articles()
    articles.to_parquet(PROCESSED / "articles_clean.parquet", index=False)
    print(f"articles_clean.parquet: {len(articles):,} products, {articles.shape[1]} columns")
    print(f"  empty search_text: {(articles['search_text'] == '').sum()}")
    print(f"  search_text words: median {articles['search_text'].str.split().str.len().median():.0f}")

    transactions = load_transactions()
    recent = keep_recent_weeks(transactions, weeks)
    recent.to_parquet(PROCESSED / "transactions_recent.parquet", index=False)
    print(f"transactions_recent.parquet: {len(recent):,} purchases "
          f"({len(recent) / len(transactions):.1%} of all), "
          f"{recent['t_dat'].min().date()} to {recent['t_dat'].max().date()}")
    print(f"  customers: {recent['customer_id'].nunique():,} | articles: {recent['article_id'].nunique():,}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subsample and clean the H&M data.")
    parser.add_argument("--weeks", type=int, default=12, help="how many recent weeks of purchases to keep")
    main(parser.parse_args().weeks)
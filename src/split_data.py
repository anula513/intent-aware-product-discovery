"""Phase 2, Step 4: split recent transactions by time into train / val / test."""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED = PROJECT_ROOT / "data" / "processed"
LOCKED = PROCESSED / "locked"          # test lives in its own folder, so it's never loaded by accident
LOCKED.mkdir(exist_ok=True)

VAL_START = pd.Timestamp("2020-09-09")
TEST_START = pd.Timestamp("2020-09-16")

tx = pd.read_parquet(PROCESSED / "transactions_recent.parquet")

train = tx[tx["t_dat"] < VAL_START]
val = tx[(tx["t_dat"] >= VAL_START) & (tx["t_dat"] < TEST_START)]
test = tx[tx["t_dat"] >= TEST_START]

# Safety check: no purchase lost and none counted twice
assert len(train) + len(val) + len(test) == len(tx)

train.to_parquet(PROCESSED / "train.parquet", index=False)
val.to_parquet(PROCESSED / "val.parquet", index=False)
test.to_parquet(LOCKED / "test.parquet", index=False)

for name, df in [("train", train), ("val", val), ("test", test)]:
    print(f"{name:5s} {len(df):>9,} purchases | {df['t_dat'].min().date()} to {df['t_dat'].max().date()}")
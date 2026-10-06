"""Phase 1 (NetFlow v3): load NF-CICIDS2018-v3 and NF-UNSW-NB15-v3, clean, save.

These two datasets share one standardized 55-column NetFlow schema, so there is no hand-mapping:
we drop identifier columns (IPs, ports, timestamps, attack-category) that leak dataset identity,
keep the ~47 flow-statistic features and the binary Label, and save a unified parquet per dataset.

    python src/data_loader.py build      # writes data/processed/{cic,unsw}.parquet
    python src/data_loader.py inspect data/raw/<file>.csv
    python src/data_loader.py demo        # self-check, no real data

CIC is subsampled (frac below) because it has ~20M rows. Scaling is deferred to the train split
(baseline.py), so nothing is normalized here.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")

# Identifier / leakage columns to drop (environment-specific, memorized across a single dataset).
ID_DROP = ["FLOW_START_MILLISECONDS", "FLOW_END_MILLISECONDS", "IPV4_SRC_ADDR", "IPV4_DST_ADDR",
           "L4_SRC_PORT", "L4_DST_PORT", "Attack"]
LABEL = "Label"

# (glob pattern, sampling fraction). CIC is huge, so subsample it.
JOBS = [("cic", "cic*.csv", 0.10), ("unsw", "unsw*.csv", 1.0)]


def inspect(csv_path: str) -> None:
    df = pd.read_csv(csv_path, nrows=5000)
    print(f"\n{csv_path}: {df.shape[1]} columns")
    for c in df.columns:
        print(f"  {c!r}")
    if LABEL in df.columns:
        print(f"\n{LABEL} values: {df[LABEL].value_counts().to_dict()}")


def _read(path: Path, frac: float, seed: int = 42) -> pd.DataFrame:
    """Chunked read, dropping ID columns; sample big files down to a manageable size."""
    use = [c for c in pd.read_csv(path, nrows=0).columns if c not in ID_DROP]
    parts = []
    for chunk in pd.read_csv(path, usecols=use, chunksize=2_000_000, low_memory=False):
        if frac < 1.0:
            chunk = chunk.sample(frac=frac, random_state=seed)
        parts.append(chunk)
    return pd.concat(parts, ignore_index=True)


def to_unified(df: pd.DataFrame) -> pd.DataFrame:
    """Numeric features + binary attack label (1=attack); drop inf/NaN."""
    if LABEL not in df.columns:
        raise KeyError(f"{LABEL!r} column not found")
    y = df[LABEL].astype(int)
    X = df.drop(columns=[LABEL]).apply(pd.to_numeric, errors="coerce")
    out = X.assign(attack=y).replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    return out


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, pattern, frac in JOBS:
        files = sorted(RAW.glob(pattern))
        if not files:
            raise FileNotFoundError(f"no files match {RAW}/{pattern} — download the dataset first")
        df = to_unified(_read(files[0], frac))
        path = OUT / f"{name}.parquet"
        df.to_parquet(path, index=False)
        print(f"{name}: {len(df):,} rows, {df.shape[1]-1} features, "
              f"attack rate {df['attack'].mean():.3f} -> {path}")


def demo() -> None:
    """Runnable self-check, no real data: fake NetFlow-like frame -> unified -> asserts."""
    rng = np.random.default_rng(0)
    df = pd.DataFrame({
        "IPV4_SRC_ADDR": ["1.2.3.4"] * 6, "L4_SRC_PORT": rng.integers(0, 9999, 6),
        "IN_BYTES": rng.integers(1, 9999, 6), "IN_PKTS": rng.integers(1, 99, 6),
        "FLOW_DURATION_MILLISECONDS": rng.integers(1, 9999, 6),
        "Attack": ["Benign", "DoS"] * 3, "Label": [0, 1, 0, 1, 0, 1],
    })
    out = to_unified(df.drop(columns=[c for c in ID_DROP if c in df.columns]))
    assert "attack" in out.columns and set(out["attack"]) == {0, 1}, "binary label must survive"
    assert "IPV4_SRC_ADDR" not in out.columns, "ID columns must be dropped before this point"
    assert out.drop(columns="attack").select_dtypes("number").shape[1] == out.shape[1] - 1, "features numeric"
    print("demo OK: NetFlow rows unify to numeric features + binary attack label")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"
    if cmd == "inspect":
        inspect(sys.argv[2])
    elif cmd == "build":
        build()
    else:
        demo()

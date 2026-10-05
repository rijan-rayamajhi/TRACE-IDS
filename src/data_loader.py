"""Phase 1: load CIC-IDS2017 and UNSW-NB15, map to a shared schema, clean, save.

The whole obstacle of this project is that the two datasets DO NOT share column
names or feature sets. This module does not pretend to know your exact columns —
the two *_MAP dicts below are a starting point you MUST verify against your real
downloaded CSVs:

    python src/data_loader.py inspect data/raw/<some_file>.csv

That prints the actual column names + label values. Fix the maps to match, then:

    python src/data_loader.py build

No scaling/normalization happens here on purpose — scalers get fit on the TRAIN
split only (Phase 2), otherwise you leak across the cross-dataset test.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")

# Unified feature schema: the conceptual flow features common to both datasets.
UNIFIED = ["duration", "fwd_packets", "bwd_packets", "fwd_bytes", "bwd_bytes"]

# unified_name -> source column name. VERIFY every one against `inspect` output;
# CIC-IDS2017 (CICFlowMeter) column names often carry leading spaces and vary by release.
CIC_MAP = {
    "duration": "Flow Duration",
    "fwd_packets": "Total Fwd Packets",
    "bwd_packets": "Total Backward Packets",
    "fwd_bytes": "Total Length of Fwd Packets",
    "bwd_bytes": "Total Length of Bwd Packets",
}
UNSW_MAP = {
    "duration": "dur",
    "fwd_packets": "spkts",
    "bwd_packets": "dpkts",
    "fwd_bytes": "sbytes",
    "bwd_bytes": "dbytes",
}

# (label column, value meaning "benign"). UNSW ships a 0/1 `label`; CIC ships text.
CIC_LABEL = ("Label", "BENIGN")
UNSW_LABEL = ("label", 0)


def inspect(csv_path: str) -> None:
    df = pd.read_csv(csv_path, nrows=5000)
    df.columns = df.columns.str.strip()
    print(f"\n{csv_path}: {df.shape[1]} columns")
    for c in df.columns:
        print(f"  {c!r}")
    for cand in ("Label", "label", "attack_cat"):
        if cand in df.columns:
            print(f"\n{cand} values: {df[cand].value_counts().to_dict()}")


def to_unified(df: pd.DataFrame, feat_map: dict, label: tuple) -> pd.DataFrame:
    """Rename source columns to the unified schema and build a binary attack label (1=attack)."""
    df = df.copy()
    df.columns = df.columns.str.strip()
    label_col, benign_val = label
    missing = [src for src in list(feat_map.values()) + [label_col] if src not in df.columns]
    if missing:
        raise KeyError(f"columns not found (fix the map via `inspect`): {missing}")
    out = pd.DataFrame({u: pd.to_numeric(df[src], errors="coerce") for u, src in feat_map.items()})
    out["attack"] = (df[label_col] != benign_val).astype(int)
    return out


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop inf/NaN rows. No scaling here (fit scalers on train split only)."""
    df = df.replace([np.inf, -np.inf], np.nan).dropna().reset_index(drop=True)
    return df


def _load_many(pattern: str) -> pd.DataFrame:
    files = sorted(RAW.glob(pattern))
    if not files:
        raise FileNotFoundError(f"no files match {RAW}/{pattern} — download the dataset first")
    return pd.concat((pd.read_csv(f, low_memory=False) for f in files), ignore_index=True)


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [
        ("cic", "cic*.csv", CIC_MAP, CIC_LABEL),
        ("unsw", "unsw*.csv", UNSW_MAP, UNSW_LABEL),
    ]
    for name, pattern, feat_map, label in jobs:
        df = clean(to_unified(_load_many(pattern), feat_map, label))
        path = OUT / f"{name}.parquet"
        df.to_parquet(path, index=False)
        print(f"{name}: {len(df):,} rows, attack rate {df['attack'].mean():.3f} -> {path}")


def demo() -> None:
    """Runnable self-check, no real data: fake source frames -> unified -> asserts."""
    cic = pd.DataFrame({**{src: [1.0, 2.0] for src in CIC_MAP.values()}, "Label": ["BENIGN", "DoS"]})
    unsw = pd.DataFrame({**{src: [1, 2] for src in UNSW_MAP.values()}, "label": [0, 1]})
    a, b = to_unified(cic, CIC_MAP, CIC_LABEL), to_unified(unsw, UNSW_MAP, UNSW_LABEL)
    assert list(a.columns) == list(b.columns) == UNIFIED + ["attack"], "schemas must match"
    assert set(a["attack"]) == set(b["attack"]) == {0, 1}, "both classes must survive mapping"
    assert clean(a).shape == a.shape, "clean dropped rows it shouldn't have"
    print("demo OK: unified schema aligns and binary label is correct across both datasets")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"
    if cmd == "inspect":
        inspect(sys.argv[2])
    elif cmd == "build":
        build()
    else:
        demo()

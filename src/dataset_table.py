"""Table 1 of the paper: the four processed NetFlow v3 datasets (printed by code).

    python src/dataset_table.py

Reads data/processed/{name}.parquet and {name}_family.parquet (from data_loader.py build / families).
Writes results/dataset_table.csv.
"""
from __future__ import annotations
import pandas as pd
from common import load, OUT, RES
from data_loader import JOBS, KEEP_ALL_BENIGN
from e5_mechanism import category

NAMES = {"cic": "NF-CICIDS2018-v3", "unsw": "NF-UNSW-NB15-v3", "ton": "NF-ToN-IoT-v3", "bot": "NF-BoT-IoT-v3"}


def main():
    rows = []
    for name, _, frac in JOBS:
        X, y = load(name)
        fam = pd.read_parquet(OUT / f"{name}_family.parquet")["family"]
        atk = fam[y.to_numpy() == 1]
        cats = sorted(set(atk.map(category)))
        rows.append({"dataset": NAMES[name], "key": name, "flows": len(y), "features": X.shape[1],
                     "attack_flows": int(y.sum()), "attack_rate": round(float(y.mean()), 4),
                     "attack_families": atk.nunique(), "attack_categories": len(cats),
                     "categories": ", ".join(cats),
                     "sampling": "all benign + attacks at 12%" if name in KEEP_ALL_BENIGN
                                 else ("all flows" if frac == 1.0 else f"{frac:.1%} uniform")})
    t = pd.DataFrame(rows)
    RES.mkdir(exist_ok=True)
    t.to_csv(RES / "dataset_table.csv", index=False)
    print(t.drop(columns="categories").to_string(index=False))
    print("\nshared attack categories:\n", t.set_index("key")["categories"].to_string())


if __name__ == "__main__":
    main()

"""Create D1-BV: D1 with requirement BV re-drawn Uniform{2..89}, seed=20260101."""
import numpy as np, pandas as pd

SEED = 20260101
SRC = "Datasets/mapped-dataset-248-80.xlsx"
OUT = "Sensitivity Analysis/Task 3/D1-BV.xlsx"
d = pd.read_excel(SRC)
assert d.groupby("us_id").us_businessvalue.nunique().max() == 1
reqs = np.sort(d.us_id.unique())
rng = np.random.default_rng(SEED)
new = dict(zip(reqs, rng.integers(2, 90, size=len(reqs))))  # high exclusive -> 2..89
n = d.copy()
n["us_businessvalue"] = n.us_id.map(new).astype("int64")
n.to_excel(OUT, index=False)

# stats
def st(df):
    b = df.drop_duplicates("us_id").us_businessvalue
    return dict(
        n_requirements=len(b),
        min=b.min(),
        max=b.max(),
        mean=b.mean(),
        median=b.median(),
        std_sample=b.std(ddof=1),
        std_population=b.std(ddof=0),
        skewness=b.skew(),
        total_BV=b.sum(),
    )


cmp = pd.DataFrame({"Original D1": st(d), "D1-BV": st(n)}).round(4)
cmp.to_csv("Sensitivity Analysis/Task 3/bv_stats_comparison.csv")
print(cmp)
# verification
r = pd.read_excel(OUT)
assert list(r.columns) == list(d.columns) and len(r) == len(d)
for c in ["tc_id", "us_id", "tc_executiontime"]:
    assert (r[c] == d[c]).all(), c
assert set(map(tuple, r[["us_id", "tc_id"]].values)) == set(
    map(tuple, d[["us_id", "tc_id"]].values)
)
assert r.us_id.nunique() == 248 and r.tc_id.nunique() == 80
assert r.groupby("us_id").us_businessvalue.nunique().max() == 1
assert r.us_businessvalue.between(2, 89).all()
diff = [c for c in d.columns if not (r[c] == d[c]).all()]
assert diff == ["us_businessvalue"], diff
print(
    "All checks passed; differing columns:",
    diff,
    "| distinct BV values:",
    r.us_businessvalue.nunique(),
)

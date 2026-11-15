import pandas as pd, numpy as np, itertools, random

SEED = 42
NTRADES = 5000
SRC = "../../Datasets/mapped-dataset-248-80.xlsx"
OUT = "D1-M.xlsx"
d = pd.read_excel(SRC)
tt = d.groupby("tc_id").tc_executiontime.first()
bv = d.groupby("us_id").us_businessvalue.first()
S = {t: set(g) for t, g in d.groupby("tc_id").us_id}  # test -> requirement set


def mpj(S):  # same as Task 1 RR_Toy.ipynb: mean over test pairs of |A&B|/|A|B|
    return float(
        np.mean(
            [
                len(S[a] & S[b]) / len(S[a] | S[b])
                for a, b in itertools.combinations(S, 2)
            ]
        )
    )


rng = random.Random(SEED)
T = sorted(S)
M = {t: set(s) for t, s in S.items()}
for _ in range(NTRADES):  # Curveball trade: preserves all row & column sums
    a, b = rng.sample(T, 2)
    A, B = M[a] - M[b], M[b] - M[a]
    if not A or not B:
        continue
    k = rng.randint(0, min(len(A), len(B)))  # allow identity too
    pool = list(A | B)
    rng.shuffle(pool)
    na = set(pool[: len(A)])
    nb = set(pool[len(A) :])
    M[a] = (M[a] - A) | na
    M[b] = (M[b] - B) | nb
rows = [
    (t, u, tt[t], bv[u])
    for u in sorted(bv.index)
    for t in sorted(t for t in M if u in M[t])
]
n = pd.DataFrame(rows, columns=d.columns)
n.to_excel(OUT, index=False)

# validation
E0 = {(t, u) for t, s in S.items() for u in s}
E1 = {(t, u) for t, s in M.items() for u in s}
diff = len(E0 - E1)
ru = lambda X: pd.Series([u for _, u in X]).value_counts().sort_index()
rd0, rd1 = ru(E0).reindex(bv.index, fill_value=0), ru(E1).reindex(bv.index, fill_value=0)
td0 = pd.Series({t: len(s) for t, s in S.items()}).sort_index()
td1 = pd.Series({t: len(s) for t, s in M.items()}).sort_index()
n2 = pd.read_excel(OUT)
tt1 = n2.groupby("tc_id").tc_executiontime.first()
bv1 = n2.groupby("us_id").us_businessvalue.first()
j0, j1 = mpj(S), mpj(M)
rep = f"""D1-M VALIDATION REPORT
Method: no mapping generator exists in the repo -> Curveball (degree-preserving binary-matrix randomization), seed={SEED}, {NTRADES} trades
Jaccard definition (from Sensitivity Analysis/Task 1/RR_Toy.ipynb): mean over all unordered test pairs of |R_a ∩ R_b| / |R_a ∪ R_b|, R_t = requirement set of test t
Requirements: {bv.size} vs {n2.us_id.nunique()}
Tests: {tt.size} vs {n2.tc_id.nunique()}
Total links: {len(E0)} vs {len(E1)} (rows in file: {len(n2)})
Requirement-degree identical: {rd0.equals(rd1)} (max abs diff {int((rd0-rd1).abs().max())})
Test-degree identical: {td0.equals(td1)} (max abs diff {int((td0-td1).abs().max())})
ID sets identical: reqs {set(bv.index)==set(bv1.index)}, tests {set(tt.index)==set(tt1.index)}
Test execution time equal: {tt.sort_index().equals(tt1.sort_index())}
Requirement BV equal: {bv.sort_index().equals(bv1.sort_index())}
Mean pairwise Jaccard: original {100*j0:.4f}% (reported ~14.09%) vs D1-M {100*j1:.4f}%
Edges differing: {diff} of {len(E0)} original edges removed/replaced ({100*diff/len(E0):.2f}%); {len(E1-E0)} new edges
"""
open("D1-M_validation_report.txt", "w").write(rep)
print(rep)

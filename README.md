# SPE_2026
Cumulative Regression Test Selection in Time-Bounded Agile Environments

---

## Repository Structure
```
SPE_2026
├── Codes
│   ├── Aging.ipynb
│   ├── DRR.ipynb
│   ├── MemLess.ipynb
│   ├── Pipeline.ipynb
│   ├── RR.ipynb
│   └── WRR.ipynb
├── Datasets
│   ├── generating_test_execution_data_for_D2.md
│   ├── mapped-dataset-124-40.xlsx
│   ├── mapped-dataset-248-80.xlsx
│   └── mapped-dataset-36-20.xlsx
├── Pipeline
│   ├── DRR.ipynb
│   ├── MemLess.ipynb
│   ├── Pipeline.ipynb
│   └── Pipeline_AG.ipynb
├── Results
│   ├── RTW_Analysis.ipynb      ← run for analysis/visualisation
│   ├── Results_D1.xlsx
│   ├── Results_D1_Analysis.xlsx
│   ├── Results_D2.xlsx
│   ├── Results_D2_Analysis.xlsx
│   ├── Results_D3.xlsx
│   ├── Results_D3_Analysis_.xlsx
│   └── analysis.png
└── Sensitivity Analysis
    ├── Task 1
    │   ├── RR_Toy.ipynb
    │   ├── RR_toy_final.csv
    │   └── RR_toy_final.xlsx
    ├── Task 2
    │   ├── D1-M.xlsx
    │   ├── D1-M_validation_report.txt
    │   ├── Results
    │   │   ├── Algorithm_Repetition_Report.xlsx
    │   │   └── analysis.png
    │   └── make_d1m.py
    └── Task 3
        ├── D1-BV.xlsx
        ├── Results
        │   ├── Algorithm_Repetition_Report.xlsx
        │   └── analysis.png
        ├── bv_stats_comparison.csv
        └── make_d1_bv.py
```

**To run the full pipeline:** Open `Pipeline/Pipeline.ipynb` (or `Pipeline_AG.ipynb` for the aging variant) and execute all cells. When prompted, select the relevant `mapped-dataset-{size}.xlsx`. The Excel report and `analysis.png` are written to `RESULTS/`.

**To run individual algorithms:** Open any notebook under `Codes/` independently. Each prompts for the dataset file on its own.

**To reproduce analysis:** Open `Results/RTW_Analysis.ipynb` after results files are populated. When prompted, select the `Results_Dx.xlsx` file to analyse. The analysis workbook is written to `RESULTS/`.

## Sensitivity Analysis

The `Sensitivity Analysis/` folder tests how robust the algorithm results are to changes in the input data. It has three tasks. Each task changes one aspect of the data, and Tasks 2 and 3 are based on dataset D1 (`Datasets/mapped-dataset-248-80.xlsx`: 248 requirements, 80 tests).

### Task 1: Toy example for RR
A small hand-checkable example (4 tests, 10 requirements) that walks through the cumulative Round Robin (RR) algorithm step by step.

| File | Description |
|------|-------------|
| `RR_Toy.ipynb` | Defines the toy test-to-requirement mapping, test execution times and right-skewed Fibonacci business values (seed 42). It computes the mean pairwise Jaccard similarity between tests. It then runs RR over RTW fractions 10%–80%, printing each pass's decision, and exports the final table. |
| `RR_toy_final.csv` / `RR_toy_final.xlsx` | Output table with one row per RTW: budget, starting RR head, selected tests, selected requirements, selected BV, requirement coverage (%) and ending RR head. |

### Task 2: D1-M (modified test-requirement mapping)
Tests sensitivity to the mapping structure. The links between tests and requirements are randomised, while everything else stays the same.

| File | Description |
|------|-------------|
| `make_d1m.py` | Generates D1-M from D1 with Curveball randomisation (seed 42, 5000 trades). This keeps every requirement's and test's number of links, and shuffles which test covers which requirement. It also writes the validation report. Run it from `Task 2/`. |
| `D1-M.xlsx` | The resulting dataset, in the same format as D1 (`tc_id`, `us_id`, `tc_executiontime`, `us_businessvalue`). |
| `D1-M_validation_report.txt` | Checks that the degrees, IDs, execution times and BV are unchanged. It also compares mean pairwise Jaccard similarity (14.08% for D1 and 15.03% for D1-M) and reports that 354 of 488 links (72.54%) changed. |
| `Results/Algorithm_Repetition_Report.xlsx` | Results of running the algorithms (MemLess, Aging, DRR, RR, WRR) on D1-M. The Summary sheet has BV and coverage per algorithm and RTW fraction. The `Sel_*` and `Wait_*` sheets hold per-requirement and per-test selection counts and waiting times. |
| `Results/analysis.png` | Plot of the results. |

### Task 3: D1-BV (re-drawn business values)
Tests sensitivity to the business-value distribution. The mapping and execution times are unchanged, and only the BV of each requirement is re-drawn.

| File | Description |
|------|-------------|
| `make_d1_bv.py` | Generates D1-BV by re-drawing each requirement's BV from Uniform{2..89} (seed 20260101). It verifies that only `us_businessvalue` changed and writes the statistics comparison. Run it from the repository root, since its paths are relative to it. |
| `D1-BV.xlsx` | The resulting dataset, in the same format as D1. |
| `bv_stats_comparison.csv` | BV statistics for original D1 and D1-BV. Skewness changes from 2.51 (right-skewed) to -0.05 (about symmetric), and mean BV from 15.27 to 46.71. |
| `Results/Algorithm_Repetition_Report.xlsx` | Same report structure as in Task 2, for D1-BV. |
| `Results/analysis.png` | Plot of the results. |

---

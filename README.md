# Multi-Criteria Framework for Algoritimy

# Replication materials — Multi-Criteria Framework for Algorithmic Auditing and Governance in Autonomous Urban Air Mobility

This repository contains the code and (anonymized) parameters needed to reproduce the results reported in the paper, including the robustness/sensitivity analysis in Section 4.5.

## Contents

```
ahp_weight_elicitation.py       # Section 3.1 — AHP weight elicitation from survey responses
electre_tri_classification.py   # Section 3.3-4 — ELECTRE TRI classification engine + baseline results
sensitivity_analysis.py         # Section 4.5 — lambda sweep, veto-threshold sweep, Monte Carlo
data/parameters.json            # All weights, thresholds, boundary profiles, archetype scores, panel demographics
results/                        # Saved output logs from running the scripts above
```

## Status of this repository

This repository accompanies a paper that is a **conceptual proof-of-concept**, not an empirically validated regulatory instrument. The archetype performance scores in `data/parameters.json` are **hypothetical and illustrative** — they are not derived from disclosed data belonging to any real manufacturer or aircraft system. See Section 4 of the paper for the full disclaimer, and Section 5 (Limitations) for a discussion of what would be required before this framework could be used operationally.

## Reproducing the results

1. **AHP weights** (`ahp_weight_elicitation.py`): This script was originally run against a live Google Sheet containing the 6 survey responses. The raw responses are not included here because the original instrument collected respondents' e-mail addresses, which were deleted after data collection per the paper's Research Ethics and Informed Consent Statement; only the resulting anonymized weight vector and demographic counts are published, in `data/parameters.json`.
2. **ELECTRE TRI classification** (`electre_tri_classification.py`): Runs directly — uses the illustrative archetype matrix and baseline weights hard-coded in the script (matching `data/parameters.json`). Output saved in `results/baseline_classification_output.txt`.
3. **Sensitivity analysis** (`sensitivity_analysis.py`): Runs directly — reproduces the λ sweep, veto-threshold sweep, and 5,000-draw Monte Carlo analysis reported in Section 4.5. Output saved in `results/sensitivity_analysis_output.txt`.

## Key finding reproduced by `sensitivity_analysis.py`

Three of the four illustrative archetypes are stable across all tested parameter perturbations. One (`SYS-BLACK-BOX`) is not: its classification changes from "Rejected" to "Regulatory Sandbox" under small, realistic changes to the criteria weights, the λ cutting level, or the Explainability veto threshold — in a Monte Carlo test centered on the AHP-elicited weights, it fell into "Sandbox" in 70% of 5,000 draws and "Rejected" in the remaining 30%. This finding is discussed in Section 4.5 and Section 5 of the paper and motivates treating the paper's contribution as methodological/conceptual rather than as a validated empirical result.

## Requirements

```
numpy
pandas
```

(`gspread`, `google-colab` are only required for the original live-Google-Sheets version of `ahp_weight_elicitation.py` and are not needed to inspect or adapt the AHP logic itself.)

## Citation

If you use this code, please cite the paper (full citation to be added upon publication/preprint availability).

## License

Add a license (e.g., MIT) before making this repository public, if you intend for others to reuse the code.



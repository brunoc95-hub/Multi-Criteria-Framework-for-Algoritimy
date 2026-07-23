# Replication materials — Multi-Criteria Framework for Algorithmic Auditing and Governance in Autonomous Urban Air Mobility

This repository contains the code, anonymized raw survey data, and parameters needed to reproduce the results reported in the paper, including the robustness/sensitivity analysis in Section 4.5.

**Update (N=9):** the expert panel grew from 6 to 9 respondents after the initial submission. This version of the repository reflects the full 9-respondent panel and applies Harker's (1987) correction to the two criterion pairs that were never queried in the survey instrument — a correction that was only approximated illustratively in earlier drafts and is now computed directly from the raw individual responses. See `CHANGELOG` below for what changed and why.

## Contents

```
data/survey_responses.csv       # Anonymized raw responses (N=9; e-mail addresses removed)
data/parameters.json            # All weights, thresholds, boundary profiles, archetype scores, panel demographics
ahp_weight_elicitation.py       # Section 3.1 — AHP weight elicitation, default-1 vs Harker-corrected
electre_tri_classification.py   # Section 3.3-4 — ELECTRE TRI engine + baseline results under 3 weight vectors
sensitivity_analysis.py         # Section 4.5 — lambda sweep, veto-threshold sweep, bootstrap Monte Carlo
smaa_tri.py                     # Section 4.5 — formal SMAA-TRI (Tervonen et al., 2009): category
                                 #   acceptability indices + central weight vectors, weights and
                                 #   lambda resampled jointly
subgroup_analysis.py            # Section 3.1 — legal/policy vs. technical subgroup weight
                                 #   comparison and re-classification (panel-composition-bias check)
figures.py                      # Regenerates all 4 paper figures from the computed results above
results/                        # Saved output logs from running the scripts above
```

## Status of this repository

This repository accompanies a paper that is a **conceptual proof-of-concept**, not an empirically validated regulatory instrument. The archetype performance scores in `data/parameters.json` are **hypothetical and illustrative** — they are not derived from disclosed data belonging to any real manufacturer or aircraft system. See Section 4 of the paper for the full disclaimer, and Section 5 (Limitations) for what would be required before this framework could be used operationally.

## Reproducing the results

1. **AHP weights** (`ahp_weight_elicitation.py`): reads `data/survey_responses.csv` directly (no longer requires live Google Sheets access). For each respondent, computes both the original default-1 treatment of the two never-queried cells and the Harker (1987)-corrected treatment, and reports both individual and mean consistency ratios (CR). The Harker-corrected vector is adopted as primary because it substantially improves mean CR (0.41 → 0.10).
2. **ELECTRE TRI classification** (`electre_tri_classification.py`): runs directly, classifying all four illustrative archetypes under three weight vectors — the original baseline-illustrative vector, the superseded N=6 vector, and the primary N=9 Harker-corrected vector — for direct comparison. Output in `results/baseline_classification_output.txt`.
3. **Sensitivity analysis** (`sensitivity_analysis.py`): runs directly, reproducing the λ sweep, veto-threshold sweep, and a **bootstrap** Monte Carlo (5,000 resamples with replacement of the 9 individual respondent weight vectors). This replaces the earlier Dirichlet-distribution Monte Carlo, which used an assumed rather than measured dispersion parameter. Output in `results/sensitivity_analysis_output.txt`.

## Key finding reproduced by `sensitivity_analysis.py` (N=9)

Under the primary N=9 Harker-corrected weights, `SYS-BLACK-BOX` is classified as **Rejected**, and this classification is now robust across the full tested range of the λ cutting level (0.50–0.85) and the Explainability veto threshold (15–50) — no flips were found. The remaining instability is uncertainty in the panel-mean weight estimate itself: the bootstrap Monte Carlo (resampling the 9 respondents) classifies `SYS-BLACK-BOX` as Rejected in ~91% of resamples and Regulatory Sandbox in ~9%. `SYS-XAI-UNB` is robustly Rejected (~99% of resamples); `SYS-alpha` and `SYS-beta` are robustly classified into the Regulatory Sandbox category (100%).

This differs from the N=6 finding reported in earlier drafts, where `SYS-BLACK-BOX`'s classification flipped between Sandbox and Rejected depending on the λ and veto-threshold calibration, and a Dirichlet Monte Carlo (with an assumed, not measured, dispersion) put it at ~70% Sandbox / 30% Rejected. The direction of the finding has changed with more data; the qualitative conclusion — that this specific archetype's classification is sensitive to defensible variation in the elicitation and calibration process, and should not be read as a validated empirical result — still holds, and is if anything reinforced by the two additional, real sources of sensitivity now documented (panel composition via bootstrap, and the default-1-vs-Harker choice for incomplete matrix cells).

## CHANGELOG

- **N=9 update:** panel grew from 6 to 9 respondents (3 new). Harker's (1987) procedure now applied to the two never-queried criterion pairs (Safety×Sustainability, Explainability×Sustainability) using the actual individual response data, replacing the N=6-era default value of 1. Primary weight vector changed from (0.2986/0.2543/0.2721/0.1751) to (0.3514/0.3916/0.1853/0.0716). Monte Carlo procedure changed from a Dirichlet distribution with an assumed dispersion parameter to a bootstrap resampling of the real individual respondent vectors. `SYS-BLACK-BOX` baseline classification changed from Regulatory Sandbox to Rejected, and is now robust to λ/veto-threshold perturbation (the earlier flip points no longer occur); residual sensitivity is now characterized via the bootstrap instead.

## SMAA-TRI update

`smaa_tri.py` formalizes the robustness check as SMAA-TRI (Tervonen et al., 2009): weights (bootstrapped from the real N=9 panel) and the cutting level (\u03bb ~ U[0.60, 0.70]) are resampled jointly, and the script reports category acceptability indices alongside central weight vectors \u2014 including, for SYS-XAI-UNB and SYS-BLACK-BOX, the central weight vector for their minority (non-modal) outcome, characterizing what panel profile would flip each classification. This replaces the earlier ad hoc bootstrap-only Monte Carlo with a named, citable, established robustness-analysis method, and removes the "SMAA-TRI not applied" item from the paper's limitations.

## Completeness note

`subgroup_analysis.py` and `figures.py` were added after an audit found they had been run to produce results/figures reported in the paper but not originally committed to this repository. `subgroup_analysis.py` reproduces the legal/policy-vs-technical panel comparison discussed in Section 3.1; `figures.py` regenerates all four paper figures from the outputs of the other scripts.

## Requirements

```
numpy
pandas
```

## Citation

If you use this code, please cite the paper (full citation to be added upon publication/preprint availability).

## License

Add a license (e.g., MIT) before making this repository public, if you intend for others to reuse the code.

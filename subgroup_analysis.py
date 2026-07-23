# -*- coding: utf-8 -*-
"""
Panel subgroup analysis (Section 3.1 / reviewer comment on panel composition
bias). Splits the N=9 panel into legal/policy (n=5) and technical (n=2;
Aerospace + AI/CS) subgroups, compares their mean Harker-corrected weights,
and checks whether the ELECTRE TRI classification of the four archetypes
changes under each subgroup's weights relative to the full-panel vector.

Innovation Management respondents (n=2) are excluded from both subgroups
(neither clearly legal/policy nor technical) and are not separately
classified in the paper; they are included here for completeness.

Requires: data/survey_responses.csv, pesos_harker_individual.npy (produced
by ahp_weight_elicitation.py -- run that script first).
"""

import numpy as np
import pandas as pd
from electre_tri_classification import (
    ias, matriz_ias, classify_one, pref, indif, vetos_base, lambda_base,
)

LABELS = ["Safety", "Explainability", "Compliance", "Sustainability"]
CAT_LABELS = {"A": "CERTIFIED", "B": "REGULATORY SANDBOX", "C": "REJECTED"}


def main():
    df = pd.read_csv("data/survey_responses.csv")
    pesos_individual = np.load("pesos_harker_individual.npy")  # order matches CSV rows

    field_col = [c for c in df.columns if "Primary Field" in c][0]
    fields = df[field_col].tolist()

    legal_idx = [i for i, f in enumerate(fields) if "Law" in f]
    tech_idx = [i for i, f in enumerate(fields) if "Aerospace" in f or "Artificial Intelligence" in f]
    innov_idx = [i for i, f in enumerate(fields) if "Innovation" in f]

    subgroups = {
        f"Legal/Policy (n={len(legal_idx)})": legal_idx,
        f"Technical, Aerospace+AI/CS (n={len(tech_idx)})": tech_idx,
        f"Innovation Management (n={len(innov_idx)})": innov_idx,
        f"Full panel (n={len(pesos_individual)})": list(range(len(pesos_individual))),
    }

    weights_by_group = {}
    print("=" * 78)
    print("Mean Harker-corrected weights by subgroup")
    print("=" * 78)
    for label, idx in subgroups.items():
        w = pesos_individual[idx].mean(axis=0)
        weights_by_group[label] = w
        print(f"{label:35s}: " + ", ".join(f"{l}={v*100:.1f}%" for l, v in zip(LABELS, w)))

    legal_key = [k for k in subgroups if k.startswith("Legal")][0]
    tech_key = [k for k in subgroups if k.startswith("Technical")][0]
    w_legal, w_tech = weights_by_group[legal_key], weights_by_group[tech_key]

    print("\nAbsolute difference, Legal vs Technical (percentage points):")
    for l, a, b in zip(LABELS, w_legal, w_tech):
        print(f"  {l:20s}: {abs(a - b) * 100:5.1f} pts")

    print("\n" + "=" * 78)
    print("ELECTRE TRI classification under each subgroup's weights")
    print("(thresholds, veto, and lambda held at the baseline calibration)")
    print("=" * 78)
    for label, idx in subgroups.items():
        w = weights_by_group[label]
        print(f"\n{label}:")
        for i, name in enumerate(ias):
            cat, s_b1, s_b2 = classify_one(matriz_ias[i], w, pref, indif, vetos_base, lambda_base)
            print(f"  {name:15s} -> {CAT_LABELS[cat]:20s} (s_b1={s_b1:.3f}, s_b2={s_b2:.3f})")


if __name__ == "__main__":
    main()

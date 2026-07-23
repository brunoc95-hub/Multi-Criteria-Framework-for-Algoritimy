# -*- coding: utf-8 -*-
"""
SMAA-TRI (Tervonen, Figueira, Lahdelma, Almeida Dias & Salminen, 2009,
"A stochastic method for robustness analysis in sorting problems",
European Journal of Operational Research, 197(1), 236-242).

Formalizes the robustness check in sensitivity_analysis.py as a proper
SMAA-TRI: both the criteria weights AND the cutting level lambda are
treated as uncertain and resampled jointly. Reports:
  - category acceptability indices b_i^h (share of draws assigning
    alternative i to category h)
  - central weight vectors w_i^c (mean weight vector among draws
    producing a given outcome for alternative i), both for the modal
    outcome and, where informative, for the minority outcome (i.e.
    what panel profile would flip the classification)

Requires: pesos_harker_individual.npy, produced by ahp_weight_elicitation.py
"""

import numpy as np
from electre_tri_classification import (
    ias, matriz_ias, classify_one, pref, indif, vetos_base,
)

LABELS = ["Safety", "Explainability", "Compliance", "Sustainability"]
LAMBDA_RANGE = (0.60, 0.70)  # defensible qualified-majority band


def run_smaa_tri(pesos_individual, n_draws=5000, seed=42):
    # NOTE: uses the legacy np.random.seed/np.random.choice API (rather than
    # np.random.default_rng) to exactly reproduce the numbers reported in the
    # paper (Section 4.5), which were generated with this RNG stream.
    np.random.seed(seed)
    n_resp = pesos_individual.shape[0]

    category_counts = {name: {"A": 0, "B": 0, "C": 0} for name in ias}
    weight_sum_by_outcome = {name: {"A": np.zeros(4), "B": np.zeros(4), "C": np.zeros(4)} for name in ias}

    for _ in range(n_draws):
        idx = np.random.choice(n_resp, size=n_resp, replace=True)
        w_draw = pesos_individual[idx].mean(axis=0)
        lam_draw = np.random.uniform(*LAMBDA_RANGE)
        for i, name in enumerate(ias):
            cat, _, _ = classify_one(matriz_ias[i], w_draw, pref, indif, vetos_base, lam_draw)
            category_counts[name][cat] += 1
            weight_sum_by_outcome[name][cat] += w_draw

    return category_counts, weight_sum_by_outcome, n_draws


def report(category_counts, weight_sum_by_outcome, n_draws):
    print("=" * 78)
    print(f"SMAA-TRI category acceptability indices b_i^h (N={n_draws} draws,")
    print(f"weights bootstrapped from the real panel + lambda ~ U{LAMBDA_RANGE})")
    print("=" * 78)
    for name in ias:
        c = category_counts[name]
        print(f"{name:15s}: b^A={c['A']/n_draws*100:5.1f}%  b^B={c['B']/n_draws*100:5.1f}%  b^C={c['C']/n_draws*100:5.1f}%")

    print("\n" + "=" * 78)
    print("Central weight vectors w_i^c (mean weight vector for the MODAL outcome)")
    print("=" * 78)
    for name in ias:
        c = category_counts[name]
        modal_cat = max(c, key=c.get)
        n_modal = c[modal_cat]
        w_c = weight_sum_by_outcome[name][modal_cat] / n_modal
        print(f"{name:15s} (modal={modal_cat}, {n_modal/n_draws*100:.1f}%): "
              f"w_c = [{', '.join(f'{v:.3f}' for v in w_c)}]")

    print("\n" + "=" * 78)
    print("Central weight vectors for the MINORITY outcome, where present")
    print("(i.e., what panel profile would flip the classification)")
    print("=" * 78)
    for name in ias:
        c = category_counts[name]
        for cat, n_cat in c.items():
            modal_cat = max(c, key=c.get)
            if cat != modal_cat and n_cat > 0:
                w_c = weight_sum_by_outcome[name][cat] / n_cat
                print(f"{name:15s} -> Category {cat} ({n_cat/n_draws*100:.1f}%): "
                      f"w_c = [{', '.join(f'{v:.3f}' for v in w_c)}]")


if __name__ == "__main__":
    pesos_individual = np.load("pesos_harker_individual.npy")
    counts, weight_sums, n = run_smaa_tri(pesos_individual)
    report(counts, weight_sums, n)

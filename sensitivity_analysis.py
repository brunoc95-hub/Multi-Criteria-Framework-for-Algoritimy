# -*- coding: utf-8 -*-
"""
Robustness / sensitivity analysis for the ELECTRE TRI classification
(Section 4.5 of the paper). UPDATED to N=9 panel with Harker-corrected
weights, and to a bootstrap Monte Carlo procedure that resamples the
actual 9 individual respondent weight vectors, replacing the earlier
version's Dirichlet distribution with an assumed (not measured)
dispersion parameter.

Requires: pesos_harker_individual.npy, produced by ahp_weight_elicitation.py
"""

import numpy as np
from electre_tri_classification import (
    ias, matriz_ias, classify_one, pref, indif, vetos_base, lambda_base,
)

LABELS = ["Safety", "Explainability", "Compliance", "Sustainability"]


def lambda_sweep(pesos, lam_range=np.arange(0.50, 0.851, 0.01)):
    print("=" * 70)
    print("1. CUTTING-LEVEL (lambda) SWEEP")
    print("=" * 70)
    prev_cat, flips = {}, {}
    for lam in lam_range:
        for i, name in enumerate(ias):
            cat, _, _ = classify_one(matriz_ias[i], pesos, pref, indif, vetos_base, lam)
            if name in prev_cat and prev_cat[name] != cat and name not in flips:
                flips[name] = round(lam, 2)
            prev_cat[name] = cat
    print("Flip points found:", flips if flips else "none in tested range -> robust")
    return flips


def veto_sweep(pesos, v2_range=range(15, 51)):
    print("\n" + "=" * 70)
    print("2. EXPLAINABILITY VETO (v2) THRESHOLD SWEEP")
    print("=" * 70)
    prev_cat, flips = {}, {}
    for v2 in v2_range:
        vetos = np.array([15, v2, 25, 45])
        for i, name in enumerate(ias):
            cat, _, _ = classify_one(matriz_ias[i], pesos, pref, indif, vetos, lambda_base)
            if name in prev_cat and prev_cat[name] != cat and name not in flips:
                flips[name] = v2
            prev_cat[name] = cat
    print("Flip points found:", flips if flips else "none in tested range -> robust")
    return flips


def bootstrap_monte_carlo(pesos_individual, n_draws=5000, seed=42):
    """
    Real bootstrap: resample the 9 respondents' individual (Harker-corrected)
    weight vectors with replacement, take the mean each draw, and classify.
    This directly measures uncertainty in the panel-mean weight estimate
    from the actual data, rather than assuming a dispersion parameter.
    """
    print("\n" + "=" * 70)
    print("3. BOOTSTRAP MONTE CARLO (resampling the real N=9 panel)")
    print("=" * 70)
    rng = np.random.default_rng(seed)
    n_resp = pesos_individual.shape[0]
    results = {name: {"A": 0, "B": 0, "C": 0} for name in ias}
    boot_means = []

    for _ in range(n_draws):
        idx = rng.choice(n_resp, size=n_resp, replace=True)
        w_boot = pesos_individual[idx].mean(axis=0)
        boot_means.append(w_boot)
        for i, name in enumerate(ias):
            cat, _, _ = classify_one(matriz_ias[i], w_boot, pref, indif, vetos_base, lambda_base)
            results[name][cat] += 1

    print(f"N={n_draws} bootstrap resamples of the {n_resp}-respondent panel mean")
    for name in ias:
        r = results[name]
        print(f"{name:15s}: A={r['A']/n_draws*100:5.1f}%  B={r['B']/n_draws*100:5.1f}%  C={r['C']/n_draws*100:5.1f}%")

    boot_means = np.array(boot_means)
    sd_boot = boot_means.std(axis=0)
    w_mean = pesos_individual.mean(axis=0)
    print("\nBootstrap standard error of the panel-mean weight estimate:")
    for i, l in enumerate(LABELS):
        print(f"{l:20s}: SD={sd_boot[i]*100:5.2f} pts   relative SD={sd_boot[i]/w_mean[i]*100:5.1f}%")

    return results, boot_means


if __name__ == "__main__":
    pesos_individual = np.load("pesos_harker_individual.npy")
    pesos_mean = pesos_individual.mean(axis=0)
    print("Primary weight vector (N=9, Harker-corrected):", np.round(pesos_mean, 4))
    print()

    lambda_sweep(pesos_mean)
    veto_sweep(pesos_mean)
    bootstrap_monte_carlo(pesos_individual)

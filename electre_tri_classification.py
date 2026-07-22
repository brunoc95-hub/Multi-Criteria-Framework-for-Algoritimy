# -*- coding: utf-8 -*-
"""
ELECTRE TRI-B classification engine for the Multi-Criteria Framework for
Algorithmic Auditing and Governance in Autonomous Urban Air Mobility.

Refactored into an importable module (used by sensitivity_analysis.py).
Running this file directly reproduces the Section 4.1 baseline results
under three weight vectors for comparison: the original illustrative
baseline, the superseded N=6 elicited vector, and the current primary
N=9 Harker-corrected vector (see data/parameters.json).
"""

import numpy as np

# Alternatives: illustrative AI-system archetypes (hypothetical, not derived
# from real disclosed data -- see paper Section 4 disclaimer)
ias = ['SYS-alpha', 'SYS-beta', 'SYS-XAI-UNB', 'SYS-BLACK-BOX']

# Performance matrix (ILLUSTRATIVE scores) [Safety, Explainability, Compliance, Sustainability]
matriz_ias = np.array([
    [95, 75, 95, 70],   # SYS-alpha: illustrative high-compliance archetype
    [92, 60, 85, 95],   # SYS-beta: illustrative acoustic/sustainability-oriented archetype
    [70, 95, 40, 85],   # SYS-XAI-UNB: illustrative academic transparent-AI archetype
    [98, 15, 70, 60],   # SYS-BLACK-BOX: illustrative pure deep-learning (opaque) archetype
])

# Category boundary profiles (b_k)
fronteiras = np.array([
    [90, 70, 80, 65],   # b1: certification cut
    [70, 40, 50, 45],   # b2: sandbox cut
])

# ELECTRE TRI thresholds
vetos_base = np.array([15, 30, 25, 45])   # veto thresholds v_j
pref = np.array([10, 10, 10, 10])          # preference thresholds p_j
indif = np.array([5, 5, 5, 5])             # indifference thresholds q_j
lambda_base = 0.65                          # cutting level

# Weight vectors (see data/parameters.json for provenance of each)
pesos_baseline_illustrative = np.array([0.29, 0.25, 0.25, 0.17])
pesos_n6_default1 = np.array([0.2986, 0.2543, 0.2721, 0.1751])
pesos_n9_harker = np.array([0.3514, 0.3916, 0.1853, 0.0716])  # PRIMARY vector


def calcular_sigma(alternativa, perfil, w, p, q, v):
    concordancia_criterio = []
    for j in range(len(w)):
        diff = alternativa[j] - perfil[j]
        if diff >= p[j]:
            c = 1
        elif diff <= q[j]:
            c = 0
        else:
            c = (diff - q[j]) / (p[j] - q[j])
        concordancia_criterio.append(c)
    C = np.sum(np.array(concordancia_criterio) * w)

    discordancia = []
    for j in range(len(w)):
        diff_v = perfil[j] - alternativa[j]
        if diff_v <= p[j]:
            d = 0
        elif diff_v >= v[j]:
            d = 1
        else:
            d = (diff_v - p[j]) / (v[j] - p[j])
        discordancia.append(d)

    sigma = C
    for j in range(len(w)):
        if discordancia[j] > C:
            sigma = sigma * (1 - discordancia[j]) / (1 - C)
    return sigma


def classify_one(nota, pesos, p, q, v, lambda_corte):
    s_b1 = calcular_sigma(nota, fronteiras[0], pesos, p, q, v)
    s_b2 = calcular_sigma(nota, fronteiras[1], pesos, p, q, v)
    if s_b1 >= lambda_corte:
        cat = "A"
    elif s_b2 >= lambda_corte:
        cat = "B"
    else:
        cat = "C"
    return cat, s_b1, s_b2


def classify_all(pesos, p=pref, q=indif, v=vetos_base, lambda_corte=lambda_base):
    out = []
    for i, nome in enumerate(ias):
        cat, s_b1, s_b2 = classify_one(matriz_ias[i], pesos, p, q, v, lambda_corte)
        out.append({"ia": nome, "cat": cat, "s_b1": round(s_b1, 4), "s_b2": round(s_b2, 4)})
    return out


CAT_LABELS = {"A": "CERTIFIED", "B": "REGULATORY SANDBOX", "C": "REJECTED"}

if __name__ == "__main__":
    weight_sets = {
        "Baseline illustrative (0.29/0.25/0.25/0.17)": pesos_baseline_illustrative,
        "N=6 elicited, default1 (superseded)": pesos_n6_default1,
        "N=9 elicited, Harker-corrected (PRIMARY)": pesos_n9_harker,
    }
    for label, pesos in weight_sets.items():
        print("=" * 70)
        print(label)
        print("=" * 70)
        for r in classify_all(pesos):
            print(f"{r['ia']:15s} -> {CAT_LABELS[r['cat']]:20s} "
                  f"(s_b1={r['s_b1']}, s_b2={r['s_b2']})")
        print()

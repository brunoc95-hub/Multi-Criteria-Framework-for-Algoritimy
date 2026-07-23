# -*- coding: utf-8 -*-
"""
Multi-Criteria Framework for Algorithmic Auditing and Governance in
Autonomous Urban Air Mobility — AHP weight elicitation.

UPDATED (N=9): this version processes the full 9-respondent panel
(6 original + 3 additional respondents collected after initial submission)
and applies Harker's (1987) formal procedure for the two criterion pairs
that were never queried in the survey instrument (Safety x Sustainability,
Explainability x Sustainability), instead of silently defaulting those
cells to 1 as the original N=6 script did. See Section 3.1 and 5 of the
paper for full discussion of why this correction is necessary (it improves
mean per-respondent consistency ratio from ~0.41 to ~0.10).

Expects the raw Google Forms export CSV in the same directory as
'survey_responses.csv' (email addresses removed prior to publication,
per the paper's Research Ethics and Informed Consent statement).
"""

import pandas as pd
import numpy as np

CSV_PATH = "data/survey_responses.csv"
RI = 0.89  # Random Index for n=4 (Saaty, 1980)
LABELS = ["Safety", "Explainability", "Compliance", "Sustainability"]


def traduzir_expert(texto, termo_a, termo_b):
    """Maps a Google-Forms verbal response to a Saaty-scale pairwise value."""
    t = str(texto).lower().strip()
    if "neutral" in t or t == "" or "equally" in t:
        return 1
    peso = 5 if "strongly" in t else 3
    if termo_a.lower() in t:
        return peso
    elif termo_b.lower() in t:
        return 1 / peso
    return 1


def build_default1_matrix(a01, a02, a12, a23):
    """Original (N=6-era) treatment: missing cells default to 1."""
    M = np.ones((4, 4))
    M[0, 1] = a01; M[1, 0] = 1 / a01
    M[0, 2] = a02; M[2, 0] = 1 / a02
    M[1, 2] = a12; M[2, 1] = 1 / a12
    M[2, 3] = a23; M[3, 2] = 1 / a23
    return M


def build_harker_matrix(a01, a02, a12, a23):
    """
    Harker's (1987) construction for an incomplete pairwise-comparison
    matrix: unknown off-diagonal entries are set to 0 (not 1), and each
    diagonal entry is set to 1 + (number of missing comparisons in that
    row). The principal eigenvector of the resulting matrix is the
    Harker-consistent weight estimate.
    """
    M = np.zeros((4, 4))
    M[0, 1] = a01; M[1, 0] = 1 / a01
    M[0, 2] = a02; M[2, 0] = 1 / a02
    M[1, 2] = a12; M[2, 1] = 1 / a12
    M[2, 3] = a23; M[3, 2] = 1 / a23
    # (0,3) Safety x Sustainability and (1,3) Explainability x Sustainability
    # were never queried -> missing in every respondent's matrix.
    M[0, 0] = 1 + 1   # row 0: 1 missing entry, (0,3)
    M[1, 1] = 1 + 1   # row 1: 1 missing entry, (1,3)
    M[2, 2] = 1 + 0   # row 2: complete
    M[3, 3] = 1 + 2   # row 3: 2 missing entries, (3,0) and (3,1)
    return M


def weights_and_cr(M, n=4):
    eigvals, eigvecs = np.linalg.eig(M)
    idx = np.argmax(np.real(eigvals))
    w = np.real(eigvecs[:, idx])
    w = w / np.sum(w)
    lambda_max = np.real(eigvals[idx])
    CI = (lambda_max - n) / (n - 1)
    CR = CI / RI
    return w, CR


def main():
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} respondents.\n")

    pesos_default1, pesos_harker = [], []
    crs_default1, crs_harker = [], []

    col_q1 = [c for c in df.columns if c.startswith("Question 1")][0]
    col_q2 = [c for c in df.columns if c.startswith("Question 2")][0]
    col_q3 = [c for c in df.columns if c.startswith("Total Transparency")][0]
    col_q4 = [c for c in df.columns if c.startswith("Question 4")][0]

    for index, row in df.iterrows():
        a01 = traduzir_expert(row[col_q1], "Preventing", "Understanding")     # Safety vs Explainability
        a23 = traduzir_expert(row[col_q2], "Adherence", "Prioritizing")       # Compliance vs Sustainability
        a12 = traduzir_expert(row[col_q3], "Transparency", "Protection")      # Explainability vs Compliance
        a02 = traduzir_expert(row[col_q4], "Accountability", "Intellectual")  # Safety vs Compliance

        w1, cr1 = weights_and_cr(build_default1_matrix(a01, a02, a12, a23))
        w2, cr2 = weights_and_cr(build_harker_matrix(a01, a02, a12, a23))

        pesos_default1.append(w1); crs_default1.append(cr1)
        pesos_harker.append(w2);   crs_harker.append(cr2)

        print(f"Respondent {index+1}: default1 w={np.round(w1,4)} CR={cr1:.3f}  |  "
              f"Harker w={np.round(w2,4)} CR={cr2:.3f}")

    pesos_default1 = np.array(pesos_default1)
    pesos_harker = np.array(pesos_harker)

    w_final_default1 = pesos_default1.mean(axis=0)
    w_final_harker = pesos_harker.mean(axis=0)

    print("\n" + "=" * 60)
    print("FINAL WEIGHTS COMPARISON (N=%d)" % len(df))
    print("=" * 60)
    for i, l in enumerate(LABELS):
        print(f"{l:20s}: default1={w_final_default1[i]*100:6.2f}%   "
              f"Harker={w_final_harker[i]*100:6.2f}%")

    print(f"\nMean CR, default1: {np.mean(crs_default1):.4f}")
    print(f"Mean CR, Harker:   {np.mean(crs_harker):.4f}")
    print("\nHarker weights adopted as the primary elicited vector for the paper")
    print("(see Section 3.1 / 5): correcting the two never-queried cells materially")
    print("improves mean consistency and is therefore the more defensible estimate.")

    print("\nInter-respondent dispersion (Harker), per criterion:")
    sd = pesos_harker.std(axis=0, ddof=1)
    for i, l in enumerate(LABELS):
        print(f"{l:20s}: SD={sd[i]*100:5.2f} pts   relative SD={sd[i]/w_final_harker[i]*100:5.1f}%")
    print("(This is individual expert disagreement, NOT the uncertainty of the panel")
    print(" mean -- see sensitivity_analysis.py for the bootstrap standard error used")
    print(" in the Monte Carlo robustness check.)")

    np.save("pesos_harker_individual.npy", pesos_harker)
    np.save("pesos_harker_mean.npy", w_final_harker)


if __name__ == "__main__":
    main()

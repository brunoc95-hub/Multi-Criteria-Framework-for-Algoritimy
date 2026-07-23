# -*- coding: utf-8 -*-
"""
Regenerates all four figures used in the paper. Run after
ahp_weight_elicitation.py, electre_tri_classification.py, and smaa_tri.py
(the numbers below are taken from their output; this script does not
recompute them, it only visualizes them).

Outputs: fig1_architecture.png, fig2_subgroups.png,
         fig3_classification.png, fig4_smaatri.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np


def fig1_architecture():
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')

    def box(x, y, w, h, text, fc='#f2f2f2', fontsize=9.5):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.08",
                                     linewidth=1.2, edgecolor='black', facecolor=fc))
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize, wrap=True)

    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='-|>', mutation_scale=14,
                                      linewidth=1.3, color='black'))

    box(0.3, 4.2, 2.1, 1.3, "Expert Panel\n(N=9)\nPairwise\ncomparisons", fc='#e8eef7')
    box(2.9, 4.2, 2.1, 1.3, "Incomplete AHP\n+ Harker (1987)\ncorrection\n\u2192 criteria weights $w_j$", fc='#e8eef7')
    arrow(2.4, 4.85, 2.9, 4.85)
    box(0.3, 2.35, 2.1, 1.3, "Black-box AI\nsystem $f$\n(archetype)", fc='#f7ecdf')
    box(2.9, 2.35, 2.1, 1.3, "SHAP attributions\n\u2192 Explainability\nscore $E(f)$", fc='#f7ecdf')
    arrow(2.4, 3.0, 2.9, 3.0)
    box(5.5, 3.25, 2.0, 1.35, "Performance matrix\n(Safety, Explainability,\nCompliance,\nSustainability)", fc='#eef2e8')
    arrow(5.0, 4.85, 5.5, 4.1); arrow(5.0, 3.0, 5.5, 3.6)
    box(5.5, 1.15, 2.0, 1.6, "ELECTRE TRI\nPessimistic\nassignment\n($w_j, q_j, p_j, v_j,\\ \\lambda$)", fc='#f3e3e3')
    arrow(6.5, 3.25, 6.5, 2.75)
    box(8.1, 3.7, 1.65, 0.8, "Category A\nCertified", fc='#dcefe0')
    box(8.1, 2.55, 1.65, 0.8, "Category B\nRegulatory\nSandbox", fc='#fdf1cf')
    box(8.1, 1.4, 1.65, 0.8, "Category C\nRejected", fc='#f6dede')
    arrow(7.5, 2.35, 8.1, 3.85); arrow(7.5, 2.0, 8.1, 2.95); arrow(7.5, 1.75, 8.1, 1.8)

    ax.text(5, 5.75, "Figure 1. Overview of the hybrid IAHP\u2013SHAP\u2013ELECTRE TRI classification architecture.",
            ha='center', fontsize=10, weight='bold')
    plt.tight_layout()
    plt.savefig('fig1_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()


def fig2_subgroups():
    criteria = ['Safety', 'Explainability', 'Compliance', 'Sustainability']
    legal = [0.420, 0.364, 0.124, 0.091]
    tech = [0.209, 0.383, 0.350, 0.058]
    full = [0.351, 0.392, 0.185, 0.072]
    x = np.arange(len(criteria)); width = 0.26

    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.bar(x - width, legal, width, label='Legal/Policy subgroup (n=5)', color='#7396c4', edgecolor='black', linewidth=0.6)
    ax.bar(x, full, width, label='Full panel (n=9, primary)', color='#5a5a5a', edgecolor='black', linewidth=0.6)
    ax.bar(x + width, tech, width, label='Technical subgroup (n=2)', color='#c9a86a', edgecolor='black', linewidth=0.6)
    ax.set_xticks(x); ax.set_xticklabels(criteria, fontsize=10)
    ax.set_ylabel('Mean Harker-corrected weight', fontsize=10)
    ax.legend(fontsize=8.5, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
    ax.set_title('Figure 2. Elicited criteria weights by panel subgroup', fontsize=10.5, weight='bold')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.set_ylim(0, 0.48)
    plt.tight_layout()
    plt.savefig('fig2_subgroups.png', dpi=300, bbox_inches='tight')
    plt.close()


def fig3_classification():
    archetypes = ['SYS-\u03b1', 'SYS-\u03b2', 'SYS-XAI-UNB', 'SYS-BLACK-BOX']
    s_b1 = [0.185, 0.072, 0.000, 0.000]
    s_b2 = [1.000, 1.000, 0.463, 0.388]
    categories = ['B', 'B', 'C', 'C']
    cat_colors = {'A': '#3a8a4c', 'B': '#c9971f', 'C': '#b23b3b'}

    fig, ax = plt.subplots(figsize=(8, 4.6))
    x = np.arange(len(archetypes)); width = 0.35
    ax.bar(x - width/2, s_b1, width, label=r'$\sigma_{b1}$ (credibility vs. certification boundary)',
           color='#7396c4', edgecolor='black', linewidth=0.6)
    ax.bar(x + width/2, s_b2, width, label=r'$\sigma_{b2}$ (credibility vs. sandbox boundary)',
           color='#c9a86a', edgecolor='black', linewidth=0.6)
    ax.axhline(0.65, color='black', linestyle='--', linewidth=1.2)
    ax.text(3.55, 0.665, r'$\lambda$ = 0.65 (cutting level)', fontsize=8.5, va='bottom', ha='right')
    for i, cat in enumerate(categories):
        ax.text(i, 1.06, f'Category {cat}', ha='center', fontsize=9, weight='bold', color=cat_colors[cat])
    ax.set_ylim(0, 1.15); ax.set_xticks(x); ax.set_xticklabels(archetypes, fontsize=10)
    ax.set_ylabel('Outranking credibility index (\u03c3)', fontsize=10)
    ax.legend(fontsize=8.5, loc='upper left', bbox_to_anchor=(0.0, -0.12), ncol=1, frameon=False)
    ax.set_title('Figure 3. ELECTRE TRI classification of the four illustrative archetypes\n'
                 '(N=9 Harker-corrected primary weights, baseline calibration)', fontsize=10.5, weight='bold')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('fig3_classification.png', dpi=300, bbox_inches='tight')
    plt.close()


def fig4_smaatri():
    archetypes = ['SYS-\u03b1', 'SYS-\u03b2', 'SYS-XAI-UNB', 'SYS-BLACK-BOX']
    pct_sandbox = [100.0, 100.0, 1.1, 8.9]
    pct_rejected = [0.0, 0.0, 98.9, 91.1]

    fig, ax = plt.subplots(figsize=(8, 4.6))
    x = np.arange(len(archetypes)); width = 0.55
    ax.bar(x, pct_sandbox, width, label='Regulatory Sandbox (Category B)', color='#c9971f', edgecolor='black', linewidth=0.6)
    ax.bar(x, pct_rejected, width, bottom=pct_sandbox, label='Rejected (Category C)', color='#b23b3b', edgecolor='black', linewidth=0.6)
    for i, (s, r) in enumerate(zip(pct_sandbox, pct_rejected)):
        if s > 4:
            ax.text(i, s/2, f'{s:.1f}%', ha='center', va='center', fontsize=9, color='white', weight='bold')
        if r > 4:
            ax.text(i, s + r/2, f'{r:.1f}%', ha='center', va='center', fontsize=9, color='white', weight='bold')
        if 0 < s <= 4:
            ax.text(i, s + 3, f'{s:.1f}%', ha='center', va='bottom', fontsize=8)
    ax.set_ylim(0, 108); ax.set_xticks(x); ax.set_xticklabels(archetypes, fontsize=10)
    ax.set_ylabel('Share of 5,000 SMAA-TRI draws (%)', fontsize=10)
    ax.legend(fontsize=9, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)
    ax.set_title('Figure 4. SMAA-TRI category acceptability indices\n'
                 '(5,000 draws: N=9 panel weight bootstrap + \u03bb ~ U[0.60, 0.70])', fontsize=10.5, weight='bold')
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('fig4_smaatri.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    fig1_architecture()
    fig2_subgroups()
    fig3_classification()
    fig4_smaatri()
    print("All 4 figures regenerated.")

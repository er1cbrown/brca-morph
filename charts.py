"""Four required figures at 300 DPI. Diagnosis order is Benign then Malignant."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE = Path(r"C:\Users\viper\Desktop\biostatspython\BiostatsPython\brca-morph")
df = pd.read_csv(BASE / "wdbc.csv").drop(columns=["id"])
st = json.loads((BASE / "work" / "stats.json").read_text(encoding="utf-8"))

sns.set_theme(style="whitegrid", context="notebook")
PALETTE = {"B": "#4C72B0", "M": "#C26A33"}
ORDER = ["B", "M"]
TICKS = ["Benign (n=357)", "Malignant (n=212)"]
DPI = 300


def fmt_p(p):
    return f"{p:.2e}" if p < 1e-3 else f"{p:.3f}"


# Chart 1. Boxplot with jitter. Explicit order so M is not labeled Benign.
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(
    data=df, x="diagnosis", y="radius_mean", hue="diagnosis",
    order=ORDER, hue_order=ORDER, palette=PALETTE, fliersize=0,
    legend=False, ax=ax,
)
sns.stripplot(
    data=df, x="diagnosis", y="radius_mean", hue="diagnosis",
    order=ORDER, hue_order=ORDER, palette=PALETTE, jitter=0.2,
    alpha=0.35, legend=False, ax=ax,
)
ax.set_title("Mean cell radius by diagnosis")
ax.set_xlabel("Diagnosis")
ax.set_ylabel("Mean cell radius")
ax.set_xticks([0, 1], TICKS)
ax.text(
    0.5, 0.96,
    f"Mann-Whitney U = {st['H1']['U']:.0f},  p = {fmt_p(st['H1']['p'])}",
    transform=ax.transAxes, ha="center", va="top", fontsize=11,
    bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none"},
)
fig.tight_layout()
fig.savefig(BASE / "H1_Tumor_Radius_Boxplot.png", dpi=DPI)
plt.close(fig)

# Chart 2. Stratified scatter with 95% confidence bands.
h2 = st["H2"]
g = sns.lmplot(
    data=df, x="radius_mean", y="texture_mean", hue="diagnosis",
    hue_order=ORDER, palette=PALETTE, height=6, aspect=1.15,
    scatter_kws={"alpha": 0.45, "s": 22}, ci=95, legend=False,
)
g.set_axis_labels("Mean cell radius", "Mean cell texture")
g.fig.suptitle("Mean radius and mean texture by diagnosis", y=1.03)
note = (
    f"All: r = {h2['All']['r']:.3f}, 95% CI [{h2['All']['ci_lo']:.3f}, {h2['All']['ci_hi']:.3f}], p = {fmt_p(h2['All']['p'])}\n"
    f"Malignant: r = {h2['M']['r']:.3f}, p = {fmt_p(h2['M']['p'])}\n"
    f"Benign: r = {h2['B']['r']:.3f}, p = {fmt_p(h2['B']['p'])}"
)
g.ax.text(
    0.02, 0.98, note, transform=g.ax.transAxes, va="top", fontsize=9,
    bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "0.8"},
)
from matplotlib.patches import Patch
g.ax.legend(
    handles=[Patch(facecolor=PALETTE["B"], label="Benign"), Patch(facecolor=PALETTE["M"], label="Malignant")],
    frameon=False, loc="lower right",
)
g.fig.tight_layout()
g.savefig(BASE / "H2_Radius_Texture_Scatter.png", dpi=DPI)
plt.close("all")

# Chart 3. Correlation heatmap of the ten mean nuclear features.
mean_cols = [c for c in df.columns if c.endswith("_mean")]
labels = [c.replace("_mean", "").replace("_", " ") for c in mean_cols]
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    df[mean_cols].corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1,
    fmt=".2f", xticklabels=labels, yticklabels=labels, square=True,
    cbar_kws={"shrink": 0.8}, ax=ax,
)
ax.set_title("Correlations among mean nuclear features")
plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
plt.setp(ax.get_yticklabels(), rotation=0)
fig.tight_layout()
fig.savefig(BASE / "Biomarker_Correlation_Heatmap.png", dpi=DPI)
plt.close(fig)

# Chart 4. ECDF of concave points. This is the H3 figure.
fig, ax = plt.subplots(figsize=(8, 6))
sns.ecdfplot(
    data=df, x="concave_points_mean", hue="diagnosis",
    hue_order=ORDER, palette=PALETTE, ax=ax,
)
ax.set_title("ECDF of mean concave points by diagnosis")
ax.set_xlabel("Mean concave points")
ax.set_ylabel("Cumulative probability")
legend = ax.get_legend()
if legend is not None:
    for text, label in zip(legend.get_texts(), ["Benign", "Malignant"]):
        text.set_text(label)
    legend.set_title("Diagnosis")
ax.text(
    0.98, 0.08,
    f"Mann-Whitney U = {st['H3']['U']:.0f},  p = {fmt_p(st['H3']['p'])}",
    transform=ax.transAxes, ha="right", fontsize=11,
    bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none"},
)
fig.tight_layout()
fig.savefig(BASE / "ConcavePoints_ECDF.png", dpi=DPI)
plt.close(fig)
print("charts saved")

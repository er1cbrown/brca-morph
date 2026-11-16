import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

BASE = r"C:\Users\viper\Desktop\biostatspython\BiostatsPython\brca-morph"
df = pd.read_csv(f"{BASE}\\wdbc.csv")
df = df.drop(columns=["id"])
# encode
df["diagnosis_code"] = df["diagnosis"].map({"M":1,"B":0})
print("shape", df.shape)
print(df["diagnosis"].value_counts())
print("missing", df.isnull().sum().sum())
print("dup", df.duplicated().sum())

# H1
mal = df[df.diagnosis=="M"]["radius_mean"]
ben = df[df.diagnosis=="B"]["radius_mean"]
print("H1 n M/B", len(mal), len(ben))
print("H1 desc M", mal.describe().round(4).to_dict())
print("H1 desc B", ben.describe().round(4).to_dict())
sm = stats.shapiro(mal); sb = stats.shapiro(ben)
print("shapiro M", sm.statistic, sm.pvalue)
print("shapiro B", sb.statistic, sb.pvalue)
u, p1 = stats.mannwhitneyu(mal, ben, alternative="greater")
print("MW U", u, "p", p1)
# ttest for completeness
welch = stats.ttest_ind(mal, ben, alternative="greater", equal_var=False)
t, tp = float(welch.statistic), float(welch.pvalue)
welch_df = float(welch.df)
print("welch t", t, "df", welch_df, "p", tp)
if not (p1 < 1e-10):
    raise SystemExit(f"H1 Mann-Whitney p was not the expected tiny value: {p1}")
md = mal.mean(); bd = ben.mean()
sdm = mal.std(); sdb = ben.std()
cd = (md-bd)/np.sqrt((sdm**2+sdb**2)/2)
print("means", md, bd, "stds", sdm, sdb, "cohens d", cd)
# median IQR
for g in ["M","B"]:
    x = df[df.diagnosis==g]["radius_mean"]
    print(g, "median", x.median(), "IQR", x.quantile(.75)-x.quantile(.25))

# H2
xv="radius_mean"; yv="texture_mean"
def pearson_ci(x,y):
    n=len(x); r,p=stats.pearsonr(x,y)
    z=np.arctanh(r); se=1/np.sqrt(n-3)
    zc=stats.norm.ppf(0.975)
    return r,p,np.tanh(z-zc*se),np.tanh(z+zc*se),n
for grp in ["All","M","B"]:
    sub = df if grp=="All" else df[df.diagnosis==grp]
    r,p,lo,hi,n = pearson_ci(sub[xv],sub[yv])
    rho,pr = stats.spearmanr(sub[xv],sub[yv])
    print(f"H2 {grp}: n={n} r={r:.6f} p={p:.3e} CI=({lo:.4f},{hi:.4f}) spearman rho={rho:.4f} p={pr:.3e}")
# compare M vs B correlations
rM,_,_,_,nM = pearson_ci(df[df.diagnosis=="M"][xv], df[df.diagnosis=="M"][yv])
rB,_,_,_,nB = pearson_ci(df[df.diagnosis=="B"][xv], df[df.diagnosis=="B"][yv])
z1,z2 = np.arctanh(rM), np.arctanh(rB)
se = np.sqrt(1/(nM-3)+1/(nB-3))
zstat=(z1-z2)/se
pp=2*(1-stats.norm.cdf(abs(zstat)))
print("compare corr z", zstat, "p", pp)

# H3
cp_m = df[df.diagnosis=="M"]["concave_points_mean"]
cp_b = df[df.diagnosis=="B"]["concave_points_mean"]
print("H3 desc M", cp_m.describe().round(5).to_dict())
print("H3 desc B", cp_b.describe().round(5).to_dict())
print("skew M", stats.skew(cp_m), "B", stats.skew(cp_b))
sm3=stats.shapiro(cp_m); sb3=stats.shapiro(cp_b)
print("shapiro cp M", sm3.statistic, sm3.pvalue, "B", sb3.statistic, sb3.pvalue)
u3,p3 = stats.mannwhitneyu(cp_m, cp_b, alternative="greater")
print("MW U3", u3, "p", p3)
md3=cp_m.mean(); bd3=cp_b.mean()
sd3m=cp_m.std(); sd3b=cp_b.std()
cd3=(md3-bd3)/np.sqrt((sd3m**2+sd3b**2)/2)
print("means3", md3, bd3, "stds", sd3m, sd3b, "d3", cd3)
welch3 = stats.ttest_ind(cp_m, cp_b, alternative="greater", equal_var=False)
rb3 = (2 * u3) / (len(cp_m) * len(cp_b)) - 1
print("H3 welch", float(welch3.statistic), "df", float(welch3.df), "p", float(welch3.pvalue), "rb", rb3)
tex_m = df.loc[df.diagnosis=="M", "texture_mean"]
tex_b = df.loc[df.diagnosis=="B", "texture_mean"]
for g in ["M","B"]:
    x=df[df.diagnosis==g]["concave_points_mean"]
    print(g,"median",x.median(),"IQR",x.quantile(.75)-x.quantile(.25))

# Correlation matrix for heatmap (mean features)
mean_cols = [c for c in df.columns if c.endswith("_mean")]
print("mean cols", mean_cols)
corr = df[mean_cols].corr()
print(corr.round(3).to_string())
# save corr
corr.to_csv(f"{BASE}\\work\\corr_mean.csv")

# Save stats summary to file
import json
stats_out = {
 "n_total": len(df), "n_M": int((df.diagnosis=="M").sum()), "n_B": int((df.diagnosis=="B").sum()),
 "H1": {"mean_M":float(mal.mean()),"mean_B":float(ben.mean()),"std_M":float(mal.std()),"std_B":float(ben.std()),
        "median_M":float(mal.median()),"median_B":float(ben.median()),
        "IQR_M":float(mal.quantile(.75)-mal.quantile(.25)),"IQR_B":float(ben.quantile(.75)-ben.quantile(.25)),
        "shapiro_M_W":float(sm.statistic),"shapiro_M_p":float(sm.pvalue),
        "shapiro_B_W":float(sb.statistic),"shapiro_B_p":float(sb.pvalue),
        "U":float(u),"p":float(p1),"cohens_d":float(cd),
        "t":float(t),"t_df":welch_df,"t_p":float(tp)},
 "texture": {"mean_M":float(tex_m.mean()),"mean_B":float(tex_b.mean()),
             "std_M":float(tex_m.std()),"std_B":float(tex_b.std()),
             "median_M":float(tex_m.median()),"median_B":float(tex_b.median()),
             "IQR_M":float(tex_m.quantile(.75)-tex_m.quantile(.25)),
             "IQR_B":float(tex_b.quantile(.75)-tex_b.quantile(.25))},
 "H2": {},
 "H3": {"mean_M":float(cp_m.mean()),"mean_B":float(cp_b.mean()),"std_M":float(cp_m.std()),"std_B":float(cp_b.std()),
        "median_M":float(cp_m.median()),"median_B":float(cp_b.median()),
        "IQR_M":float(cp_m.quantile(.75)-cp_m.quantile(.25)),"IQR_B":float(cp_b.quantile(.75)-cp_b.quantile(.25)),
        "skew_M":float(stats.skew(cp_m)),"skew_B":float(stats.skew(cp_b)),
        "shapiro_M_W":float(sm3.statistic),"shapiro_M_p":float(sm3.pvalue),
        "shapiro_B_W":float(sb3.statistic),"shapiro_B_p":float(sb3.pvalue),
        "U":float(u3),"p":float(p3),"cohens_d":float(cd3),
        "t":float(welch3.statistic),"t_df":float(welch3.df),"t_p":float(welch3.pvalue),
        "rank_biserial":float(rb3)},
 "compare_corr": {"z":float(zstat),"p":float(pp)},
}
for grp in ["All","M","B"]:
    sub = df if grp=="All" else df[df.diagnosis==grp]
    r,ppp,lo,hi,n = pearson_ci(sub[xv],sub[yv])
    rho,pr = stats.spearmanr(sub[xv],sub[yv])
    stats_out["H2"][grp] = {"n":int(n),"r":float(r),"p":float(ppp),"ci_lo":float(lo),"ci_hi":float(hi),
                            "spearman_rho":float(rho),"spearman_p":float(pr)}
with open(f"{BASE}\\work\\stats.json","w") as f:
    json.dump(stats_out, f, indent=2)
print("saved stats")
print(json.dumps(stats_out, indent=2))

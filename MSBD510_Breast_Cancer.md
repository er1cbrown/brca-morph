---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.5
  kernelspec:
    display_name: Python 3
    name: python3
---

<!-- #region id="view-in-github" colab_type="text" -->
<a href="https://colab.research.google.com/github/er1cbrown/brca-morph/blob/main/MSBD510_Breast_Cancer.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
<!-- #endregion -->

<!-- #region id="f524d51a" -->
# Course Project: Statistical Analysis of Cellular Morphology in Breast Cancer Diagnostics

---

## 1. Project Overview & Administrative Metadata

| Metadata | Details |
| :--- | :--- |
| **Project Duration** | 2 Weeks (Part-Time / Lab Assignment) |
| **Team Structure** | 2–3 Students per Group |
| **Core Technical Stack** | Python (`pandas`, `numpy`, `scipy.stats`, `matplotlib`, `seaborn`) |
| **Dataset Name & Dimensions** | Breast Cancer Wisconsin (Diagnostic) — 569 patient records × 32 features |
| **Direct CSV Access URL** | [Data CSV URL](https://raw.githubusercontent.com/gscdit/Breast-CancerDetection/refs/heads/master/data.csv) |

### Brief Notes / Status:
* [ X] Team formed
* [X ] GitHub URL confirmed
<!-- #endregion -->

```python id="V_MKtKJXzBXk" colab={"base_uri": "https://localhost:8080/", "height": 436} outputId="8d2ae937-3809-46dc-9d3a-24ca37b4bffc"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats

df = pd.read_csv("wdbc.csv")

# Display the first five rows
df.tail()
```

<!-- #region id="d2be77a5" -->
## 2. Target Hypotheses & Required Statistical Tests

### $H_1$: Tumor Size and Malignancy (Two-Sample Comparative Test)
* **Research Question:** Is the mean cell radius (`radius_mean`) significantly larger in malignant tumors than in benign masses?
* **Hypotheses:**
  * $H_{01}: \mu(\text{Radius, Malignant}) = \mu(\text{Radius, Benign})$
  * $H_{a1}: \mu(\text{Radius, Malignant}) > \mu(\text{Radius, Benign})$
* **Status / Results:** *[Fill in test results and Cohen's d here]*

### $H_2$: Morphological Scaling Correlation (Bivariate Analysis)
* **Research Question:** Is there a significant linear relationship between mean cell radius (`radius_mean`) and mean cell texture (`texture_mean`), and does it differ by diagnosis?
* **Hypotheses:**
  * $H_{02}: r(\text{radius_mean, texture_mean}) = 0$
  * $H_{a2}: r(\text{radius_mean, texture_mean}) \neq 0$
* **Status / Results:** *[Fill in correlation coefficients and 95% CIs here]*

### $H_3$: Structural Irregularity & Contour Concavity (Non-Parametric Evaluation)
* **Research Question:** Do malignant cells display significantly higher boundary irregularity (`concave points_mean`) compared to benign cells?
* **Hypotheses:**
  * $H_{03}: \mu(\text{Concave Points, Malignant}) = \mu(\text{Concave Points, Benign})$
  * $H_{a3}: \mu(\text{Concave Points, Malignant}) > \mu(\text{Concave Points, Benign})$
* **Status / Results:** *[Fill in Mann-Whitney U test results here]*
<!-- #endregion -->

```python id="2HOag1l7zCC8" outputId="c920b9cd-219e-48e3-e818-2cbcfce610bc" colab={"base_uri": "https://localhost:8080/", "height": 382}
# H1: Tumor Size and Malignancy (Two-Sample Comparative Test)
#Import libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats

#Load dataset

df = pd.read_csv("wdbc.csv")

# Display the first five rows
df.head()

#Inspect dataset

# Number of rows and columns
print("Dataset dimensions:", df.shape)

# Column names
print("\nColumn names:")
print(df.columns.tolist())

# Data types
print("\nData types:")
print(df.dtypes)

# General dataset information
df.info()

#Clean dataset

# Remove patient ID because it is not needed for statistical testing
df = df.drop(columns=["id"])

# Check for missing values
print("Missing values:")
print(df.isnull().sum().sum())

# Check diagnosis categories
print("\nDiagnosis counts:")
print(df["diagnosis"].value_counts())

# Check for duplicate rows
print("\nDuplicate rows:", df.duplicated().sum())

#Separate diagnosis groups

# Malignant tumors
malignant = df[df["diagnosis"] == "M"]["radius_mean"]

# Benign tumors
benign = df[df["diagnosis"] == "B"]["radius_mean"]

# Display sample sizes
print("Malignant sample size:", len(malignant))
print("Benign sample size:", len(benign))

#Descriptive statistics

summary = df.groupby("diagnosis")["radius_mean"].agg(
    ["count", "mean", "std", "median"]
)

# Calculate IQR
iqr = df.groupby("diagnosis")["radius_mean"].apply(
    lambda x: x.quantile(0.75) - x.quantile(0.25)
)

summary["IQR"] = iqr

print(summary)

#Shapiro-Wilk normality test

# Test malignant group
shapiro_m = stats.shapiro(malignant)

# Test benign group
shapiro_b = stats.shapiro(benign)

# Display results
print("Malignant Shapiro-Wilk Test")
print("W-statistic:", shapiro_m.statistic)
print("P-value:", shapiro_m.pvalue)

print("\nBenign Shapiro-Wilk Test")
print("W-statistic:", shapiro_b.statistic)
print("P-value:", shapiro_b.pvalue)
#Mann-Whitney U test

u_stat, p_value = stats.mannwhitneyu(
    malignant,
    benign,
    alternative="greater"
)

print("Mann-Whitney U statistic:", u_stat)
print("P-value:", p_value)

alpha = 0.05

if p_value < alpha:
    print("Reject the null hypothesis.")
else:
    print("Fail to reject the null hypothesis.")

#Calculate Cohen's d

# Calculate group means
mean_m = malignant.mean()
mean_b = benign.mean()

# Calculate group standard deviations
std_m = malignant.std()
std_b = benign.std()

# Calculate Cohen's d
cohens_d = (mean_m - mean_b) / np.sqrt(
    (std_m**2 + std_b**2) / 2
)

print("Malignant mean:", mean_m)
print("Benign mean:", mean_b)
print("Cohen's d:", cohens_d)
```

```python id="epIouk40BZdl"
# H2: Morphological Scaling Correlation (Bivariate Analysis)

# Variables for H2 stored as a tuple (fixed pair)
h2_vars = ("radius_mean", "texture_mean")
x_var, y_var = h2_vars

alpha = 0.05

# Groups to analyze stored as a list
groups = ["All", "M", "B"]

# Readable labels stored in a dictionary
group_labels = {"All": "All Tumors", "M": "Malignant", "B": "Benign"}

print("H2 variables:", h2_vars)
print(df[list(h2_vars)].describe().round(3))
```

<!-- #region id="e60d1f3e" -->
## 3. Required Data Visualizations

Track the completion and output file locations for the 4 required figures (300 DPI):

- [ ] **Chart 1: Distribution Comparison Plot (Boxplot with Jitter / Swarmplot)**
  - *Target:* Compare `radius_mean` across Benign and Malignant groups with annotated p-values.
  - *File Path:*
- [ ] **Chart 2: Stratified Scatter Plot with Linear Regression Lines**
  - *Target:* Plot `radius_mean` vs. `texture_mean` stratified by diagnosis with 95% confidence bands.
  - *File Path:*
- [ ] **Chart 3: Biomarker Feature Correlation Heatmap**
  - *Target:* Display feature correlation matrix across primary cell nucleus markers.
  - *File Path:*
- [ ] **Chart 4: Empirical Cumulative Distribution Function (ECDF) / KDE Plot**
  - *Target:* Compare cumulative probability curves for `concave points_mean` between cohorts.
  - *File Path:*
<!-- #endregion -->

```python id="50KLGzvLi1b3"
# H1: Tumor Size and Malignancy (Two-Sample Comparative Test)
#Boxplot with jitter

plt.figure(figsize=(9, 6))

# Create boxplot
sns.boxplot(
    data=df,
    x="diagnosis",
    y="radius_mean",
    fliersize=0
)

# Overlay individual observations
sns.stripplot(
    data=df,
    x="diagnosis",
    y="radius_mean",
    jitter=0.2,
    alpha=0.35
)

# Add labels and title
plt.title("Mean Cell Radius by Tumor Diagnosis")
plt.xlabel("Tumor Diagnosis")
plt.ylabel("Mean Cell Radius")

# Rename categories
plt.xticks([0, 1], ["Benign", "Malignant"])

#p-value
plt.text(
    0.5,
    0.95,
    "Mann-Whitney U p = 1.35e-68",
    transform=plt.gca().transAxes,
    ha="center"
)

plt.tight_layout()

# Save chart at 300 DPI
plt.savefig("H1_Tumor_Radius_Boxplot.png", dpi=300)

# Display chart
plt.show()
```

```python id="RQvKHu0QzC6S"
# H2: Helper functions

# Pearson r with a 95% CI using the Fisher z transformation
def pearson_with_ci(x, y, conf=0.95):
    n = len(x)
    r, p = stats.pearsonr(x, y)
    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    z_crit = stats.norm.ppf(1 - (1 - conf) / 2)
    lower = np.tanh(z - z_crit * se)
    upper = np.tanh(z + z_crit * se)
    return r, p, (lower, upper), n

# Describe correlation strength using Cohen's guidelines
def describe_strength(r):
    size = abs(r)
    if size < 0.10:
        return "negligible"
    elif size < 0.30:
        return "weak"
    elif size < 0.50:
        return "moderate"
    else:
        return "strong"

# Return the rows for a group
def get_group(data, group):
    if group == "All":
        return data
    else:
        return data[data["diagnosis"] == group]

# Fisher z test for comparing two independent correlations
def compare_correlations(r1, n1, r2, n2):
    z1, z2 = np.arctanh(r1), np.arctanh(r2)
    se_diff = np.sqrt(1 / (n1 - 3) + 1 / (n2 - 3))
    z_stat = (z1 - z2) / se_diff
    p = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    return z_stat, p
```

<!-- #region id="c2011268" -->
## 4. PDF Scientific Report Layout & Content Checklists

Use this checklist to draft and compile your final 3-5 page manuscript:

- [ ] **Title & Authors:** Clean title, affiliations, and dates.
- [ ] **Abstract:** 150-200 word summary containing background, objective, tests used, key p-values, and clinical conclusions.
- [ ] **Introduction:** FNA background and clinical justification for morphological markers.
- [ ] **Methodology:** Data details, preprocessing steps, and hypotheses formulas.
- [ ] **Results:** Stratified summary table, embedded figures with captions, and explicit reporting of test statistics.
- [ ] **Discussion:** Clinical implications, limitations, and future outlook.
- [ ] **References:** 2-3 formal academic citations.
<!-- #endregion -->

```python id="pFzUxNISzDlM"

```

<!-- #region id="0968da3f" -->
## 5. Mandatory Student Collaboration Table

| Student Name | Assigned Tasks & Focus Areas | Specific Artifacts Created | Contribution % |
| :--- | :--- | :--- | :--- |
| **Student 1** | | | % |
| **Student 2** | | | % |
| **Student 3** | | | % |
<!-- #endregion -->

```python id="damYkiSvzEfD"

```

<!-- #region id="Z3hrkWiWygcH" -->
# Course Project Specification: Statistical Analysis of Cellular Morphology in Breast Cancer Diagnostics

---

## 1. Project Overview & Administrative Metadata

| Metadata | Details |
| :--- | :--- |
| **Project Duration** | 2 Weeks (Part-Time / Lab Assignment) |
| **Team Structure** | 2–3 Students per Group |
| **Core Technical Stack** | Python (`pandas`, `numpy`, `scipy.stats`, `matplotlib`, `seaborn`) |
| **Dataset Name & Dimensions** | Breast Cancer Wisconsin (Diagnostic) — 569 patient records × 32 features |
| **Direct CSV Access URL** | [Data CSV URL](https://raw.githubusercontent.com/gscdit/Breast-CancerDetection/refs/heads/master/data.csv) |

In this project, student teams act as **junior biomedical data analysts** investigating quantitative cell nucleus features calculated from digitized fine-needle aspirate (FNA) images of breast masses. By analyzing nuclear radius, texture, perimeter, area, smoothness, and boundary concavity, students will clean real-world clinical data, test formal statistical hypotheses, produce publication-quality charts, and summarize findings in a manuscript-style PDF report and slide presentation.

---

## 2. Target Hypotheses & Required Statistical Tests

### $H_1$: Tumor Size and Malignancy (Two-Sample Comparative Test)
* **Research Question:** Is the mean cell radius (`radius_mean`) significantly larger in malignant tumors than in benign masses?
* **Hypotheses:**
  * $H_{01}: \mu(\text{Radius, Malignant}) = \mu(\text{Radius, Benign})$
  * $H_{a1}: \mu(\text{Radius, Malignant}) > \mu(\text{Radius, Benign})$
* **Required Analysis:** Assess distribution normality per cohort. Run a parametric or non-parametric test and compute Cohen's $d$ effect size.

### $H_2$: Morphological Scaling Correlation (Bivariate Analysis)
* **Research Question:** Is there a significant linear relationship between mean cell radius (`radius_mean`) and mean cell texture (`texture_mean`), and does it differ by diagnosis?
* **Hypotheses:**
  * $H_{02}: r(\text{radius_mean, texture_mean}) = 0$
  * $H_{a2}: r(\text{radius_mean, texture_mean}) \neq 0$
* **Required Analysis:** Compute Pearson $r$ or Spearman rank coefficients separately for benign and malignant cohorts alongside 95% confidence intervals.

### $H_3$: Structural Irregularity & Contour Concavity (Non-Parametric Evaluation)
* **Research Question:** Do malignant cells display significantly higher boundary irregularity (`concave points_mean`) compared to benign cells?
* **Hypotheses:**
  * $H_{03}: \mu(\text{Concave Points, Malignant}) = \mu(\text{Concave Points, Benign})$
  * $H_{a3}: \mu(\text{Concave Points, Malignant}) > \mu(\text{Concave Points, Benign})$
* **Required Analysis:** Evaluate positive distribution skewness and run a Mann–Whitney U test.

### Required Statistical Methodology & SciPy API Functions
1. **Normality Testing:** Use `scipy.stats.shapiro(x)` or `scipy.stats.normaltest(x)` on each feature vector. If $p < 0.05$, reject normality and select non-parametric alternatives.
2. **Independent Two-Sample Tests:** Use `scipy.stats.ttest_ind(a, b, alternative='greater')` for normally distributed features, or `scipy.stats.mannwhitneyu(a, b, alternative='greater')` for non-normal features.
3. **Effect Size Calculation (Cohen's $d$):** Calculate via NumPy:
   $$\text{Cohen's } d = \frac{\text{mean}(a) - \text{mean}(b)}{\sqrt{\frac{\text{std}(a)^2 + \text{std}(b)^2}{2}}}$$
4. **Bivariate Correlation:** Use `scipy.stats.pearsonr(x, y)` for linear relationships or `scipy.stats.spearmanr(x, y)` for non-linear monotonic relationships.
5. **Summary Metrics:** Compute descriptive metrics using pandas:
   ```python
   df.groupby('diagnosis').agg(['mean', 'std', 'median', lambda x: x.quantile(0.75) - x.quantile(0.25)])
   ```

---

## 3. Required Data Visualizations & API Documentation

* **Chart 1: Distribution Comparison Plot (Boxplot with Jitter / Swarmplot)**
  * *Target:* Compare `radius_mean` across Benign and Malignant groups with annotated p-values.
  * *Functions:* `sns.boxplot(..., fliersize=0)` overlaid with `sns.stripplot(jitter=0.2)` or `sns.swarmplot()`.
* **Chart 2: Stratified Scatter Plot with Linear Regression Lines**
  * *Target:* Plot `radius_mean` vs. `texture_mean` stratified by diagnosis with 95% confidence bands.
  * *Functions:* `sns.lmplot(..., hue='diagnosis')` or `sns.scatterplot()` paired with `sns.regplot()` and custom `plt.text()` for correlation coefficients.
* **Chart 3: Biomarker Feature Correlation Heatmap**
  * *Target:* Display feature correlation matrix across primary cell nucleus markers.
  * *Functions:* `df.corr()` followed by `sns.heatmap(annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')`.
* **Chart 4: Empirical Cumulative Distribution Function (ECDF) / KDE Plot**
  * *Target:* Compare cumulative probability curves for `concave points_mean` between cohorts.
  * *Functions:* `sns.ecdfplot(..., hue='diagnosis')` or `sns.kdeplot(cumulative=True)`.

---

## 4. PDF Scientific Report Layout & Content Requirements

Your final 3-5 page scientific research paper should contain the following structured sections:
1. **Title & Authors:** Concise title, course name, team member names, affiliations, and date.
2. **Abstract (150–200 words):** Executive summary of the biological background, core objectives, methodologies, primary findings (p-values, effect sizes), and main diagnostic conclusions.
3. **Introduction:** Background on breast cancer screening and FNA biopsy techniques. Scientific justification for using quantitative nuclear morphology.
4. **Methodology:**
   * *Data Description:* Detail the UCI WDBD origin, sample size (569), features (30), and split (357 Benign, 212 Malignant).
   * *Data Cleaning:* Step-by-step preprocessing (dropping `id`, `Unnamed: 32`, encoding `M=1, B=0`, outlier/missing value audit).
   * *Hypotheses & Tests:* Formal statements of $H_1, H_2, H_3$ with mathematical formulas and normality-testing justifications.
5. **Results & Visualizations:**
   * Stratified descriptive summary table (Mean ± SD, Median [IQR]).
   * High-resolution embedded Figures (1 to 4) with clear captions.
   * Detailed statistical results reporting test statistics ($t$, $U$, $r$), exact p-values, degrees of freedom, and Cohen's $d$ effect sizes.
6. **Discussion & Limitations:** Interpretation of clinical implications, potential data limitations (single-center sampling, multicollinearity), and future directions.
7. **References:** Citations of key sources (e.g., Street et al. 1993, SciPy/Pandas docs).
8. **Student Collaboration Table:** Explicit breakdown of individual contributions.

---

## 5. Mandatory Student Collaboration Table

| Student Name | Assigned Tasks & Focus Areas | Specific Artifacts Created | Contribution % |
| :--- | :--- | :--- | :--- |
| **Student 1 (Lead Analyst)** | Data loading, Preprocessing, cleaning, Shapiro-Wilk testing, Hypothesis $H_1$ | Chart 1, Preprocessing scripts, Results section drafting | 33.3% |
| **Student 2 (Visualization & Stats)** | Exploratory scatter plots, Pearson/Spearman correlations for $H_2$, Heatmap | Chart 2, Chart 3, Methods section drafting | 33.3% |
| **Student 3 (Report & Presentation)** | Non-parametric evaluation for $H_3$, ECDF chart generation, PDF/Slide compilation | Chart 4, Abstract, Discussion, Slide Deck production | 33.3% |

---

## 6. Two-Week Milestone Roadmap

### Week 1: Data Preprocessing & Exploratory Analysis
1. **Environment Setup:** Load CSV from Github raw URL. Drop metadata (`id`, `Unnamed: 32`) and encode `diagnosis` (`M=1, B=0`).
2. **Exploratory Data Analysis:** Run missing value audits and compute descriptive statistics.
3. **Visual Output:** Generate and save 300 DPI high-resolution image files for Charts 1, 2, 3, and 4.

### Week 2: Statistical Testing, Manuscript & Presentation
1. **Inferential Statistics:** Perform Shapiro-Wilk tests, run comparative tests, and compute effect sizes.
2. **PDF Manuscript:** Draft and compile the final 3-page scientific paper.
3. **Oral Presentation:** Create a 5-slide presentation deck summarizing findings.

---

## 7. Evaluation Rubric Matrix

| Evaluation Category | Weight | Specific Grading Criteria |
| :--- | :--- | :--- |
| **Data Preprocessing & Hygiene** | 15% | Correct CSV loading, label encoding, metadata column removal, missing value audit, clean Pandas code structure. |
| **Statistical Rigor & Methodology** | 25% | Appropriate distribution checks, correct test selection, accurate statistical reporting (p-values, effect sizes). |
| **Data Visualizations** | 25% | Production of all 4 required charts with professional styling (labeled axes, units, titles, clear palettes). |
| **Paper-Style PDF Manuscript** | 20% | Full adherence to scientific paper layout, embedded figures, summary tables, and clear academic writing. |
| **Presentation & Collaboration Table** | 15% | Clear 5-slide deck, effective team delivery, and completed mandatory Collaboration Table. |
<!-- #endregion -->

<!-- #region id="d8b91616" -->
## 6. Two-Week Milestone Roadmap

### Week 1: Data Preprocessing & Exploratory Analysis
1. **Environment Setup:** Load CSV from Github raw URL. Drop metadata (`id`, `Unnamed: 32`) and encode `diagnosis` (`M=1, B=0`).
2. **Exploratory Data Analysis:** Run missing value audits and compute descriptive statistics.
3. **Visual Output:** Generate and save 300 DPI high-resolution image files for Charts 1, 2, 3, and 4.

### Week 2: Statistical Testing, Manuscript & Presentation
1. **Inferential Statistics:** Perform Shapiro-Wilk tests, run comparative tests, and compute effect sizes.
2. **PDF Manuscript:** Draft and compile the final 3-page scientific paper.
3. **Oral Presentation:** Create a 5-slide presentation deck summarizing findings.
<!-- #endregion -->

<!-- #region id="2418e162" -->
## 7. Evaluation Rubric Matrix

| Evaluation Category | Weight | Specific Grading Criteria |
| :--- | :--- | :--- |
| **Data Preprocessing & Hygiene** | 15% | Correct CSV loading, label encoding, metadata column removal, missing value audit, clean Pandas code structure. |
| **Statistical Rigor & Methodology** | 25% | Appropriate distribution checks, correct test selection, accurate statistical reporting (p-values, effect sizes). |
| **Data Visualizations** | 25% | Production of all 4 required charts with professional styling (labeled axes, units, titles, clear palettes). |
| **Paper-Style PDF Manuscript** | 20% | Full adherence to scientific paper layout, embedded figures, summary tables, and clear academic writing. |
| **Presentation & Collaboration Table** | 15% | Clear 5-slide deck, effective team delivery, and completed mandatory Collaboration Table. |
<!-- #endregion -->

```python id="gSv8ZBhlzFKY"
```

"""Manuscript PDF for the MSBD510 cellular-morphology project. 3 to 5 pages."""
import json
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE = Path(r"C:\Users\viper\Desktop\biostatspython\BiostatsPython\brca-morph")
st = json.loads((BASE / "work" / "stats.json").read_text(encoding="utf-8"))

pdfmetrics.registerFont(TTFont("Calibri", r"C:\Windows\Fonts\calibri.ttf"))
pdfmetrics.registerFont(TTFont("Calibri-Bold", r"C:\Windows\Fonts\calibrib.ttf"))
pdfmetrics.registerFont(TTFont("Calibri-Italic", r"C:\Windows\Fonts\calibrii.ttf"))
pdfmetrics.registerFont(TTFont("Calibri-BoldItalic", r"C:\Windows\Fonts\calibriz.ttf"))
pdfmetrics.registerFontFamily(
    "Calibri",
    normal="Calibri",
    bold="Calibri-Bold",
    italic="Calibri-Italic",
    boldItalic="Calibri-BoldItalic",
)

INK = colors.HexColor("#1B2420")
FOREST = colors.HexColor("#2C4A2B")
MUTED = colors.HexColor("#5C6158")
RULE = colors.HexColor("#C9C4B4")
HEAD_BG = colors.HexColor("#E7EFE4")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    "CoverTitle", fontName="Calibri-Bold", fontSize=16, leading=20,
    textColor=INK, alignment=TA_CENTER, spaceAfter=4,
))
styles.add(ParagraphStyle(
    "CoverSub", fontName="Calibri-Italic", fontSize=11, leading=14,
    textColor=FOREST, alignment=TA_CENTER, spaceAfter=2,
))
styles.add(ParagraphStyle(
    "CoverMeta", fontName="Calibri", fontSize=10, leading=13,
    textColor=MUTED, alignment=TA_CENTER, spaceAfter=2,
))
styles.add(ParagraphStyle(
    "H", fontName="Calibri-Bold", fontSize=12.5, leading=16,
    textColor=FOREST, spaceBefore=11, spaceAfter=4,
))
styles.add(ParagraphStyle(
    "Body", fontName="Calibri", fontSize=10.5, leading=13.6,
    textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6,
))
styles.add(ParagraphStyle(
    "Caption", fontName="Calibri-Italic", fontSize=9, leading=11.5,
    textColor=MUTED, spaceBefore=2, spaceAfter=8,
))
styles.add(ParagraphStyle(
    "Cell", fontName="Calibri", fontSize=8, leading=10, textColor=INK,
))
styles.add(ParagraphStyle(
    "CellHead", fontName="Calibri-Bold", fontSize=8, leading=10, textColor=INK,
))
styles.add(ParagraphStyle(
    "BulletBody", fontName="Calibri", fontSize=10.5, leading=13.4, textColor=INK,
))
styles.add(ParagraphStyle(
    "Ref", fontName="Calibri", fontSize=10, leading=13, textColor=INK,
    leftIndent=12, firstLineIndent=-12, spaceAfter=3,
))


def P(text, style="Body"):
    return Paragraph(text, styles[style])


def fmt_p(p):
    if p < 1e-3:
        return f"{p:.2e}"
    if p < 0.01:
        return f"{p:.4f}"
    return f"{p:.3f}"


def mean_sd(mean, sd, digits):
    return f"{mean:.{digits}f} &plusmn; {sd:.{digits}f}"


def med_iqr(med, iqr, digits):
    return f"{med:.{digits}f} [{iqr:.{digits}f}]"


h1, h2, h3 = st["H1"], st["H2"], st["H3"]
tx, cmp_ = st["texture"], st["compare_corr"]

ABSTRACT = (
    "Digitized fine-needle aspirate images quantify the nuclei in a breast mass. "
    "Using the Wisconsin Diagnostic Breast Cancer data (569 cases; 357 benign, 212 malignant), "
    "we tested three hypotheses: malignant nuclei have a larger mean radius; mean radius and mean "
    "texture are linearly related, possibly differently by diagnosis; and malignant nuclei have more "
    "concave points. Shapiro-Wilk tests rejected normality for malignant radius and for concave points "
    "in both groups, so those comparisons used one-sided Mann-Whitney U tests and Cohen's d. "
    "Pearson correlations used Fisher z 95% confidence intervals. Malignant mean radius was 17.46 versus "
    "12.15 (U = 70955, p = 1.35e-68, d = 2.05). Radius and texture correlated in the pooled sample "
    "(r = 0.324, 95% CI 0.248 to 0.395, p = 2.36e-15) but in neither diagnosis alone, and the two "
    "within-group correlations did not differ (z = 1.65, p = 0.099). Concave points were higher in "
    "malignant nuclei (mean 0.0880 versus 0.0257; U = 72992.5, p = 5.03e-77, d = 2.33). Mean radius "
    "and concave points separate these diagnoses with very large effects."
)
abstract_words = len(ABSTRACT.split())
if not 150 <= abstract_words <= 200:
    raise SystemExit(f"Abstract word count {abstract_words} is outside 150-200")


def figure(path, caption, max_height=3.35 * inch):
    image = PILImage.open(path)
    width_px, height_px = image.size
    height = max_height
    width = height * width_px / height_px
    max_width = 7.1 * inch
    if width > max_width:
        width = max_width
        height = width * height_px / width_px
    return KeepTogether([
        Image(str(path), width=width, height=height, hAlign="CENTER"),
        P(caption, "Caption"),
    ])


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(FOREST)
    canvas.rect(0, letter[1] - 0.38 * inch, letter[0], 0.38 * inch, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Calibri", 9)
    canvas.drawString(0.7 * inch, letter[1] - 0.25 * inch, "MSBD510  ·  Cellular morphology in breast cancer diagnosis")
    canvas.setFillColor(MUTED)
    canvas.setFont("Calibri", 9)
    canvas.drawString(0.7 * inch, 0.38 * inch, "Wisconsin Diagnostic Breast Cancer  ·  n = 569")
    canvas.drawRightString(letter[0] - 0.7 * inch, 0.38 * inch, str(doc.page))
    canvas.restoreState()


def cell(text, head=False):
    return P(text, "CellHead" if head else "Cell")


desc_header = [
    cell("Feature", True),
    cell("Benign mean &plusmn; SD", True),
    cell("Benign median [IQR]", True),
    cell("Malignant mean &plusmn; SD", True),
    cell("Malignant median [IQR]", True),
]
desc_rows = [desc_header]
for label, block, digits, other in [
    ("radius_mean", h1, 2, None),
    ("texture_mean", tx, 2, None),
    ("concave_points_mean", h3, 4, None),
]:
    desc_rows.append([
        cell(label),
        cell(mean_sd(block["mean_B"], block["std_B"], digits)),
        cell(med_iqr(block["median_B"], block["IQR_B"], digits)),
        cell(mean_sd(block["mean_M"], block["std_M"], digits)),
        cell(med_iqr(block["median_M"], block["IQR_M"], digits)),
    ])

desc = Table(desc_rows, colWidths=[1.55*inch, 1.4*inch, 1.45*inch, 1.55*inch, 1.45*inch])
desc.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.3, RULE),
    ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))

collab_header = [cell(h, True) for h in ["Student", "Focus", "Artifacts", "%"]]
collab_data = [
    ["Student 1 (Lead analyst)", "Load, clean, Shapiro-Wilk, H1 radius test", "Chart 1 and the results table", "33.3%"],
    ["Student 2 (Visualization)", "H2 correlation, scatter plot, heatmap", "Charts 2 and 3, methods", "33.3%"],
    ["Student 3 (Report)", "H3 concave points, ECDF, paper, slides", "Chart 4, abstract, discussion, deck", "33.3%"],
]
collab_rows = [collab_header] + [[cell(v) for v in row] for row in collab_data]
collab = Table(collab_rows, colWidths=[1.7*inch, 2.35*inch, 2.35*inch, 0.6*inch])
collab.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.3, RULE),
    ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ("ALIGN", (3, 1), (3, -1), "CENTER"),
]))

story = [
    P("Statistical Analysis of Cellular Morphology in Breast Cancer Diagnostics", "CoverTitle"),
    P("MSBD510 course project", "CoverSub"),
    P("Student 1 (Lead analyst), Student 2 (Visualization and statistics), Student 3 (Report and presentation)", "CoverMeta"),
    P("16 November 2026", "CoverMeta"),
    Spacer(1, 6),
    P("Abstract", "H"),
    P(ABSTRACT),
    P("1. Introduction", "H"),
    P(
        "Breast cancer diagnosis often starts with a tissue sample rather than an open biopsy. "
        "Fine-needle aspiration recovers cells from a breast mass, and a digitized image of those "
        "cells can be summarized by the size, gray-level variation, and outline of each nucleus. "
        "Street, Wolberg, and Mangasarian computed thirty such features for 569 masses and showed "
        "that the benign and malignant classes are separable in that feature space. This project "
        "does not refit their classifier. It tests three features that have a direct reading on a "
        "cytology slide: mean radius, mean texture, and mean number of concave points on the contour."
    ),
    P("2. Methods", "H"),
    P(
        "The Wisconsin Diagnostic Breast Cancer table has 569 rows and 32 columns: an identifier, "
        "the diagnosis, and 30 numeric nuclear features. There are 357 benign (B) and 212 malignant (M) "
        "cases, no missing values, and no duplicate rows. The identifier was dropped. An empty trailing "
        "column is dropped if a copy of the file contains one. Diagnosis was coded M = 1 and B = 0 for "
        "the audit, and the letter labels were kept for the figures. No observations were removed. "
        "The file used here is the project copy of wdbc.csv, which matches the University of Wisconsin release."
    ),
    P(
        "Each hypothesis was written as a one-sided comparison except the correlation, which is two-sided. "
        "The significance level is 0.05. Shapiro-Wilk was applied to each cohort. If either cohort rejected "
        "normality, the primary two-sample test was the Mann-Whitney U test with alternative 'greater' "
        "(malignant values larger). Cohen's d used the two sample standard deviations with the usual "
        "n-1 denominator. A Welch t test is reported only as a sensitivity check. Pearson r is the "
        "test of the correlation hypothesis, with a 95% confidence interval from the Fisher z transformation. "
        "The malignant and benign correlations were compared with a two-sided Fisher z test. Spearman rank "
        "correlations are reported beside the Pearson results."
    ),
    P(
        "<b>H1.</b> H01: mean radius is equal in malignant and benign nuclei. Ha1: the malignant mean is larger."
    ),
    P(
        "<b>H2.</b> H02: the Pearson correlation of radius_mean and texture_mean is zero. "
        "Ha2: the correlation is not zero. The correlation is estimated in the pooled sample and inside each diagnosis."
    ),
    P(
        "<b>H3.</b> H03: mean concave points are equal in the two diagnoses. "
        "Ha3: the malignant mean is larger. Skewness is reported because the assignment asks for it before the rank test. "
        "The rank-biserial correlation is 2U / (nM × nB) − 1."
    ),
    KeepTogether([
        P("3. Results", "H"),
        desc,
        P("Table 1. Mean &plusmn; SD and median [IQR] by diagnosis. Benign n = 357. Malignant n = 212.", "Caption"),
    ]),
    P(
        f"<b>H1, radius.</b> The malignant distribution is not normal (Shapiro-Wilk W = {h1['shapiro_M_W']:.3f}, "
        f"p = {fmt_p(h1['shapiro_M_p'])}). The benign distribution is compatible with normality "
        f"(W = {h1['shapiro_B_W']:.3f}, p = {fmt_p(h1['shapiro_B_p'])}). Because one cohort fails normality, "
        f"the primary test is Mann-Whitney U. U = {h1['U']:.0f}, one-sided p = {fmt_p(h1['p'])}. "
        f"Cohen's d = {h1['cohens_d']:.2f}. The Welch check agrees: t = {h1['t']:.2f}, "
        f"df = {h1['t_df']:.1f}, one-sided p = {fmt_p(h1['t_p'])}. Reject H01."
    ),
    figure(
        BASE / "H1_Tumor_Radius_Boxplot.png",
        f"Figure 1. Mean cell radius by diagnosis, with each case shown. "
        f"Mann-Whitney U = {h1['U']:.0f}, p = {fmt_p(h1['p'])}.",
    ),
    P(
        f"<b>H2, radius and texture.</b> In all 569 cases, r = {h2['All']['r']:.3f}, "
        f"95% CI [{h2['All']['ci_lo']:.3f}, {h2['All']['ci_hi']:.3f}], df = {h2['All']['n'] - 2}, "
        f"p = {fmt_p(h2['All']['p'])}. Spearman rho = {h2['All']['spearman_rho']:.3f}. "
        f"Inside malignant cases, r = {h2['M']['r']:.3f}, 95% CI [{h2['M']['ci_lo']:.3f}, {h2['M']['ci_hi']:.3f}], "
        f"df = {h2['M']['n'] - 2}, p = {fmt_p(h2['M']['p'])}. "
        f"Inside benign cases, r = {h2['B']['r']:.3f}, 95% CI [{h2['B']['ci_lo']:.3f}, {h2['B']['ci_hi']:.3f}], "
        f"df = {h2['B']['n'] - 2}, p = {fmt_p(h2['B']['p'])}. "
        f"The two group correlations do not differ: Fisher z = {cmp_['z']:.2f}, p = {fmt_p(cmp_['p'])}. "
        "Reject H02 in the pooled sample. Do not reject it inside either diagnosis."
    ),
    figure(
        BASE / "H2_Radius_Texture_Scatter.png",
        "Figure 2. Mean radius against mean texture, with a separate least-squares line and 95% band for each diagnosis. "
        "The lines inside each diagnosis are nearly flat. The pooled correlation comes from the two clouds sitting in different places.",
    ),
    figure(
        BASE / "Biomarker_Correlation_Heatmap.png",
        "Figure 3. Pearson correlations among the ten mean nuclear features. "
        "Radius, perimeter, and area are nearly the same measurement (r about 0.99).",
        max_height=3.15 * inch,
    ),
    P(
        f"<b>H3, concave points.</b> Both samples are right-skewed (malignant skewness {h3['skew_M']:.2f}, "
        f"benign {h3['skew_B']:.2f}). Shapiro-Wilk rejects normality in both "
        f"(malignant W = {h3['shapiro_M_W']:.3f}, p = {fmt_p(h3['shapiro_M_p'])}; "
        f"benign W = {h3['shapiro_B_W']:.3f}, p = {fmt_p(h3['shapiro_B_p'])}). "
        f"Mann-Whitney U = {h3['U']:.1f}, one-sided p = {fmt_p(h3['p'])}. "
        f"Cohen's d = {h3['cohens_d']:.2f}. Rank-biserial correlation = {h3['rank_biserial']:.2f}. "
        f"The Welch check agrees (t = {h3['t']:.2f}, df = {h3['t_df']:.1f}, p = {fmt_p(h3['t_p'])}) "
        "but is not the primary test. Reject H03."
    ),
    figure(
        BASE / "ConcavePoints_ECDF.png",
        f"Figure 4. Empirical cumulative distribution of mean concave points. "
        f"The malignant curve lies to the right. Mann-Whitney U = {h3['U']:.1f}, p = {fmt_p(h3['p'])}.",
    ),
    P("4. Discussion", "H"),
    P(
        "H1 and H3 are supported, and the effects are large enough to see on the plots without the p-values. "
        "A malignant nucleus in this table is, on average, both larger and more indented. "
        "H2 needs a narrower claim. Radius and texture are associated when the diagnoses are pooled, "
        "and they are not associated inside either diagnosis. The test of whether those two correlations "
        "differ does not reach 0.05 (p = 0.099). The honest description is that malignant cases sit higher "
        "on both axes, which creates a correlation in the mixture, rather than that texture scales with "
        "radius inside a tumor class."
    ),
    P(
        "Figure 3 is a warning about double-counting. Radius, perimeter, and area move together, and concave "
        "points move with them (r = 0.82 with radius). A later model that treats those columns as separate "
        "biological facts will overstate how many independent signals it has. Street, Wolberg, and Mangasarian "
        "already found that a plane in three features was enough for a high correct-classification rate. "
        "This paper does not estimate sensitivity, specificity, or performance on a later set of patients."
    ),
    P("5. Limitations", "H"),
    ListFlowable(
        [
            ListItem(P("One institution and one imaging pipeline, from a release dated November 1995.", "BulletBody")),
            ListItem(P("The diagnosis is taken as given. We did not review the slides.", "BulletBody")),
            ListItem(P("The within-group correlation comparison is not significant, so a larger sample could still change that part of H2.", "BulletBody")),
            ListItem(P("No held-out cases and no classifier. These results are not a diagnostic claim.", "BulletBody")),
        ],
        bulletType="bullet",
        leftIndent=14,
        spaceBefore=0,
        spaceAfter=6,
    ),
    P("References", "H"),
    P("Street WN, Wolberg WH, Mangasarian OL. Nuclear feature extraction for breast tumor diagnosis. Proc SPIE. 1993;1905:861-870.", "Ref"),
    P("Mangasarian OL, Street WN, Wolberg WH. Breast cancer diagnosis and prognosis via linear programming. Operations Research. 1995;43(4):570-577.", "Ref"),
    P("Virtanen P, Gommers R, Oliphant TE, et al. SciPy 1.0: fundamental algorithms for scientific computing in Python. Nature Methods. 2020;17:261-272.", "Ref"),
    KeepTogether([
        P("6. Collaboration", "H"),
        P("Each person is responsible for one third of the submitted work. Type legal names over the role labels before upload."),
        collab,
    ]),
    Spacer(1, 6),
]

out = BASE / "BRCA_Morph_Report.pdf"
doc = SimpleDocTemplate(
    str(out),
    pagesize=letter,
    leftMargin=0.7 * inch,
    rightMargin=0.7 * inch,
    topMargin=0.58 * inch,
    bottomMargin=0.58 * inch,
    title="Statistical Analysis of Cellular Morphology in Breast Cancer Diagnostics",
    author="MSBD510 project group",
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print("abstract words", abstract_words)
print("saved", out)

/**
 * Five-slide MSBD510 deck.
 * Palette and type from the biology dissertation template:
 * cream / forest / terracotta, Georgia + Calibri, wide layout.
 */
const pptxgen = require("C:/Users/viper/AppData/Local/Temp/pptxgen/node_modules/pptxgenjs");

const COLOR = {
  darkBg: "1B2420",
  cream: "F1EDE3",
  beige: "E8DFC8",
  card: "F7F3EA",
  ink: "1B2420",
  body: "3B3F3A",
  muted: "7A7F76",
  mutedLight: "A7A79A",
  forest: "3B5D3A",
  forestDeep: "2C4A2B",
  terracotta: "C26A33",
  hairline: "C9C4B4",
  titleOnDark: "EFE9D9",
  subtitleOnDark: "C9C4B4",
  white: "FFFFFF",
};

const FONT = { head: "Georgia", body: "Calibri", mono: "Consolas" };
const BASE = "C:/Users/viper/Desktop/biostatspython/BiostatsPython/brca-morph";

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
pres.layout = "WIDE";
pres.title = "Cellular morphology in breast cancer diagnosis";
pres.author = "MSBD510 project group";
pres.subject = "WDBC hypotheses H1, H2, and H3";

const W = 13.333;
const H = 7.5;

function shadow() {
  return { type: "outer", color: "1B2420", blur: 10, offset: 3, angle: 135, opacity: 0.08 };
}

function eyebrow(slide, label, page, onDark) {
  slide.addText(label, {
    x: 0.55, y: 0.28, w: 8.5, h: 0.28,
    fontFace: FONT.body, fontSize: 12, color: onDark ? COLOR.mutedLight : COLOR.muted,
    charSpacing: 1.6, margin: 0,
  });
  slide.addText(page, {
    x: 10.3, y: 0.28, w: 2.45, h: 0.28,
    fontFace: FONT.body, fontSize: 12, color: onDark ? COLOR.mutedLight : COLOR.muted,
    align: "right", margin: 0,
  });
}

function slide1() {
  const s = pres.addSlide();
  s.background = { color: COLOR.darkBg };
  eyebrow(s, "MSBD510  ·  COURSE PROJECT", "01  /  05", true);

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.55, y: 1.15, w: 4.55, h: 0.38,
    fill: { color: COLOR.darkBg },
    line: { color: COLOR.mutedLight, width: 1 },
    rectRadius: 0.06,
  });
  s.addText("WISCONSIN DIAGNOSTIC BREAST CANCER", {
    x: 0.55, y: 1.15, w: 4.55, h: 0.38,
    fontFace: FONT.body, fontSize: 11, color: COLOR.subtitleOnDark,
    align: "center", valign: "middle", margin: 0, charSpacing: 0.6,
  });

  s.addText("Cell nucleus shape\nand a malignant diagnosis", {
    x: 0.55, y: 1.75, w: 12.1, h: 2.15,
    fontFace: FONT.head, fontSize: 42, color: COLOR.titleOnDark, margin: 0, valign: "top",
  });
  s.addText("Three tests on 569 fine-needle aspirate cases. Radius, texture, and contour irregularity.", {
    x: 0.55, y: 4.15, w: 10.5, h: 0.45,
    fontFace: FONT.body, fontSize: 18, color: COLOR.subtitleOnDark, margin: 0,
  });

  const stats = [
    ["569", "cases"],
    ["357", "benign"],
    ["212", "malignant"],
  ];
  stats.forEach((pair, i) => {
    const x = 0.55 + i * 2.55;
    s.addText(pair[0], {
      x, y: 5.15, w: 2.3, h: 0.62,
      fontFace: FONT.head, fontSize: 32, color: COLOR.titleOnDark, margin: 0,
    });
    s.addText(pair[1], {
      x, y: 5.78, w: 2.3, h: 0.3,
      fontFace: FONT.body, fontSize: 14, color: COLOR.mutedLight, margin: 0,
    });
  });

  s.addText("Student 1   ·   Student 2   ·   Student 3      16 November 2026", {
    x: 0.55, y: 6.85, w: 12, h: 0.3,
    fontFace: FONT.body, fontSize: 14, color: COLOR.mutedLight, margin: 0,
  });

  s.addNotes(
    "Look at the camera, then start. Good morning. Our group analyzed cell-nucleus measurements from fine-needle aspirates of breast masses. The question is whether size, texture, and an irregular outline differ between malignant and benign tumors. The table has 569 cases, 357 benign and 212 malignant. I will go through the three tests. My own section is the concave-points result on slide 4. Then I will stop for questions."
  );
}

function card(slide, x, y, w, h, fill) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: fill },
    line: { color: fill },
    rectRadius: 0.08,
    shadow: shadow(),
  });
}

function slide2() {
  const s = pres.addSlide();
  s.background = { color: COLOR.cream };
  eyebrow(s, "DATA AND HYPOTHESES", "02  /  05", false);
  s.addText("What we tested, before looking at a p-value", {
    x: 0.55, y: 0.68, w: 12, h: 0.55,
    fontFace: FONT.head, fontSize: 28, color: COLOR.ink, margin: 0,
  });

  const items = [
    ["H1  ·  Student 1", "Mean radius", "Malignant nuclei are larger. One-sided. The malignant group is not normal, so the test is Mann-Whitney U, with Cohen's d."],
    ["H2  ·  Student 2", "Radius and texture", "Is there a linear correlation, and does it differ by diagnosis? Pearson r, a 95% Fisher interval, and a test of the two correlations."],
    ["H3  ·  Student 3", "Concave points", "Malignant contours are more indented. Both groups are skewed, so the primary test is again one-sided Mann-Whitney U."],
  ];
  items.forEach((item, i) => {
    const x = 0.55 + i * 4.2;
    card(s, x, 1.55, 3.95, 3.85, COLOR.card);
    s.addText(item[0], {
      x: x + 0.25, y: 1.75, w: 3.45, h: 0.32,
      fontFace: FONT.body, fontSize: 13, color: COLOR.terracotta, margin: 0,
    });
    s.addText(item[1], {
      x: x + 0.25, y: 2.15, w: 3.45, h: 0.7,
      fontFace: FONT.head, fontSize: 26, color: COLOR.ink, margin: 0,
    });
    s.addText(item[2], {
      x: x + 0.25, y: 2.95, w: 3.45, h: 2.15,
      fontFace: FONT.body, fontSize: 15, color: COLOR.body, margin: 0,
    });
  });

  s.addText("Cleaning: drop the id. No missing values. No duplicate rows. Code M = 1 and B = 0. Alpha = 0.05. Do not delete outliers.", {
    x: 0.55, y: 5.7, w: 12.2, h: 0.7,
    fontFace: FONT.body, fontSize: 16, color: COLOR.body, margin: 0,
  });
  s.addText("Run from the brca-morph folder in LazyVim: open the .ipynb, Space mp, then Space rA. The CSV is wdbc.csv.", {
    x: 0.55, y: 6.5, w: 12.2, h: 0.45,
    fontFace: FONT.body, fontSize: 15, color: COLOR.forest, margin: 0,
  });

  s.addNotes(
    "We wrote the hypotheses first. H1: malignant nuclei have a larger mean radius. H2: radius and texture are linearly correlated, and we asked whether that correlation differs by diagnosis. H3: malignant nuclei have more concave points, which counts indentations on the outline. That third test is mine. We dropped the patient id. Nothing was missing, and there were no duplicate rows. If a group was not normal, we did not use a t test as the main result. Alpha is 0.05."
  );
}

function statBlock(slide, x, y, w, value, label, valueColor) {
  slide.addText(value, {
    x, y, w, h: 0.42,
    fontFace: FONT.head, fontSize: 22, color: valueColor || COLOR.ink, margin: 0,
  });
  slide.addText(label, {
    x, y: y + 0.4, w, h: 0.28,
    fontFace: FONT.body, fontSize: 12, color: COLOR.muted, margin: 0,
  });
}

function slide3() {
  const s = pres.addSlide();
  s.background = { color: COLOR.beige };
  eyebrow(s, "RESULTS  ·  H1 AND H2", "03  /  05", false);
  s.addText("Size separates the groups. Texture does not scale inside them.", {
    x: 0.5, y: 0.62, w: 12.3, h: 0.5,
    fontFace: FONT.head, fontSize: 24, color: COLOR.ink, margin: 0,
  });

  card(s, 0.5, 1.3, 6.15, 2.55, COLOR.card);
  s.addText("H1 supported", {
    x: 0.72, y: 1.42, w: 5.7, h: 0.32,
    fontFace: FONT.body, fontSize: 13, color: COLOR.forest, margin: 0,
  });
  s.addText("17.46  vs  12.15", {
    x: 0.72, y: 1.76, w: 5.7, h: 0.46,
    fontFace: FONT.head, fontSize: 26, color: COLOR.ink, margin: 0,
  });
  s.addText("Malignant mean radius versus benign", {
    x: 0.72, y: 2.24, w: 5.7, h: 0.26,
    fontFace: FONT.body, fontSize: 13, color: COLOR.muted, margin: 0,
  });
  s.addText("U = 70,955     p = 1.35e-68     d = 2.05", {
    x: 0.72, y: 2.62, w: 5.7, h: 0.36,
    fontFace: FONT.body, fontSize: 15, color: COLOR.body, margin: 0,
  });
  s.addText("Welch check: t = 22.21, df = 289.7. Same decision.", {
    x: 0.72, y: 3.05, w: 5.7, h: 0.4,
    fontFace: FONT.body, fontSize: 14, color: COLOR.body, margin: 0,
  });

  card(s, 0.5, 4.02, 6.15, 2.95, COLOR.card);
  s.addText("H2 only in the pooled sample", {
    x: 0.72, y: 4.14, w: 5.7, h: 0.3,
    fontFace: FONT.body, fontSize: 13, color: COLOR.terracotta, margin: 0,
  });
  s.addText("r = 0.324", {
    x: 0.72, y: 4.48, w: 5.7, h: 0.42,
    fontFace: FONT.head, fontSize: 26, color: COLOR.ink, margin: 0,
  });
  s.addText("95% CI 0.248 to 0.395     p = 2.36e-15     df = 567", {
    x: 0.72, y: 4.96, w: 5.7, h: 0.32,
    fontFace: FONT.body, fontSize: 14, color: COLOR.body, margin: 0,
  });
  s.addText("Malignant r = 0.107, p = 0.122\nBenign r = -0.037, p = 0.484\nDifference between those r values: z = 1.65, p = 0.099", {
    x: 0.72, y: 5.38, w: 5.7, h: 1.25,
    fontFace: FONT.body, fontSize: 15, color: COLOR.body, margin: 0,
  });

  s.addImage({
    path: BASE + "/H1_Tumor_Radius_Boxplot.png",
    x: 7.05, y: 1.45, w: 5.7, h: 4.275,
  });
  s.addText("Figure. Mean radius. Benign is on the left.", {
    x: 7.05, y: 5.85, w: 5.7, h: 0.3,
    fontFace: FONT.body, fontSize: 12, color: COLOR.muted, margin: 0,
  });
  s.addText("Inside each diagnosis, radius and texture are not correlated.", {
    x: 7.05, y: 6.2, w: 5.7, h: 0.55,
    fontFace: FONT.body, fontSize: 14, color: COLOR.body, margin: 0,
  });

  s.addNotes(
    "H1 is supported. Malignant mean radius is 17.46. Benign is 12.15. The malignant distribution was not normal, so the main test is Mann-Whitney. U is 70,955. The p-value is 1.35 times 10 to the minus 68. Cohen's d is 2.05, which is a very large effect. A Welch t test gives the same decision. H2 is only partly supported. In the full sample, r is 0.324, and the confidence interval does not include zero. Inside malignant cases the p-value is 0.12. Inside benign cases it is 0.48. The two correlations are not significantly different from each other. Fisher z p-value is 0.099. Say that clearly. The pooled correlation exists because the groups sit in different parts of the plot, not because texture grows with radius inside one diagnosis."
  );
}

function slide4() {
  const s = pres.addSlide();
  s.background = { color: COLOR.cream };
  eyebrow(s, "HYPOTHESIS 3  ·  STUDENT 3", "04  /  05", false);
  s.addText("Malignant nuclei have a more irregular contour", {
    x: 0.5, y: 0.62, w: 12.3, h: 0.5,
    fontFace: FONT.head, fontSize: 26, color: COLOR.ink, margin: 0,
  });

  card(s, 0.5, 1.35, 6.15, 5.45, COLOR.card);
  s.addText("Mean concave points", {
    x: 0.75, y: 1.52, w: 5.7, h: 0.3,
    fontFace: FONT.body, fontSize: 14, color: COLOR.terracotta, margin: 0,
  });
  s.addText("0.0880   vs   0.0257", {
    x: 0.75, y: 1.9, w: 5.7, h: 0.5,
    fontFace: FONT.head, fontSize: 28, color: COLOR.ink, margin: 0,
  });
  s.addText("Malignant versus benign", {
    x: 0.75, y: 2.45, w: 5.7, h: 0.28,
    fontFace: FONT.body, fontSize: 14, color: COLOR.muted, margin: 0,
  });

  const rows = [
    ["Mann-Whitney U", "72,992.5"],
    ["One-sided p", "5.03e-77"],
    ["Cohen's d", "2.33"],
    ["Rank-biserial r", "0.93"],
    ["Skewness, M and B", "0.73 and 0.92"],
    ["Shapiro-Wilk", "both p < 0.001"],
  ];
  rows.forEach((row, i) => {
    const y = 3.0 + i * 0.52;
    s.addText(row[0], {
      x: 0.75, y, w: 3.1, h: 0.4,
      fontFace: FONT.body, fontSize: 15, color: COLOR.body, margin: 0, valign: "middle",
    });
    s.addText(row[1], {
      x: 3.7, y, w: 2.6, h: 0.4,
      fontFace: FONT.body, fontSize: 16, color: COLOR.ink, margin: 0, align: "right", valign: "middle",
    });
  });

  s.addImage({
    path: BASE + "/ConcavePoints_ECDF.png",
    x: 7.05, y: 1.45, w: 5.7, h: 4.275,
  });
  s.addText("Figure. The malignant curve is shifted right. A t test is not the primary test, because both groups fail normality.", {
    x: 7.05, y: 5.9, w: 5.7, h: 0.85,
    fontFace: FONT.body, fontSize: 14, color: COLOR.body, margin: 0,
  });

  s.addNotes(
    "This slide is my section. Concave points measure indentations on the nucleus outline. Both groups are right-skewed, about 0.73 in malignant nuclei and 0.92 in benign nuclei. Shapiro-Wilk rejects normality in both, so a t test would be the wrong primary test. The Mann-Whitney U test, one-sided, gives U of 72,992.5 and a p-value of 5.03 times 10 to the minus 77. The malignant mean is 0.088. The benign mean is 0.026. Cohen's d is 2.33. The rank-biserial correlation is 0.93, which means a randomly chosen malignant nucleus almost always has more concave points than a randomly chosen benign nucleus. The ECDF shows that shift. We reject the null hypothesis."
  );
}

function slide5() {
  const s = pres.addSlide();
  s.background = { color: COLOR.cream };
  eyebrow(s, "CLOSE", "05  /  05", false);
  s.addText("What we can say, and what we should not claim", {
    x: 0.5, y: 0.62, w: 12.2, h: 0.5,
    fontFace: FONT.head, fontSize: 26, color: COLOR.ink, margin: 0,
  });

  const blocks = [
    [COLOR.forest, "Supported", "Malignant nuclei are larger and more indented. Both effects are very large and visible on the plots."],
    [COLOR.terracotta, "Narrower claim", "Radius and texture correlate only in the mixed sample. They do not correlate inside either diagnosis."],
    [COLOR.forestDeep, "Do not claim", "We did not build a classifier, and this is one center's images from 1995. Radius, perimeter, and area are almost one measurement."],
  ];
  blocks.forEach((b, i) => {
    const y = 1.35 + i * 1.25;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y, w: 0.12, h: 1.05,
      fill: { color: b[0] }, line: { color: b[0] }, rectRadius: 0.04,
    });
    s.addText(b[1], {
      x: 0.85, y, w: 7.3, h: 0.32,
      fontFace: FONT.body, fontSize: 14, color: b[0], margin: 0,
    });
    s.addText(b[2], {
      x: 0.85, y: y + 0.34, w: 7.3, h: 0.7,
      fontFace: FONT.body, fontSize: 16, color: COLOR.body, margin: 0,
    });
  });

  card(s, 8.55, 1.35, 4.25, 3.7, COLOR.darkBg);
  s.addText("EQUAL SHARES", {
    x: 8.8, y: 1.55, w: 3.8, h: 0.28,
    fontFace: FONT.body, fontSize: 12, color: COLOR.mutedLight, margin: 0, charSpacing: 1.2,
  });
  const people = [
    ["33.3%", "Student 1", "Cleaning and H1"],
    ["33.3%", "Student 2", "H2 and charts 2 and 3"],
    ["33.3%", "Student 3", "H3, paper, slides"],
  ];
  people.forEach((p, i) => {
    const y = 2.05 + i * 0.9;
    s.addText(p[0], {
      x: 8.8, y, w: 3.8, h: 0.34,
      fontFace: FONT.head, fontSize: 20, color: COLOR.titleOnDark, margin: 0,
    });
    s.addText(p[1] + "  ·  " + p[2], {
      x: 8.8, y: y + 0.34, w: 3.8, h: 0.3,
      fontFace: FONT.body, fontSize: 13, color: COLOR.subtitleOnDark, margin: 0,
    });
  });

  s.addText("Type the three legal names over Student 1, 2, and 3 before you upload. Presenter View shows these notes on your screen while the class sees the slide.", {
    x: 0.5, y: 6.45, w: 12.3, h: 0.6,
    fontFace: FONT.body, fontSize: 14, color: COLOR.forestDeep, margin: 0,
  });

  s.addNotes(
    "Close like this. Radius and concave points separate the two diagnoses, and the effects are large. Do not say we invented a new screening test. We did not build a classifier, and the images come from one center in 1995. Also do not treat radius, perimeter, and area as three separate findings. They are almost the same measurement. The work is split in thirds. Student 1 did the cleaning and the radius test. Student 2 did the correlation, the scatter plot, and the heatmap. I did the concave-points test, the cumulative curve, the paper, and these slides. Each share is 33.3 percent. Thank you. I can take questions."
  );
}

slide1();
slide2();
slide3();
slide4();
slide5();

pres.writeFile({ fileName: BASE + "/BRCA_Morph_Slides.pptx" }).then(() => {
  console.log("saved pptx");
});

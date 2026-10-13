# TEJ cheat sheet and reference guide style guide

## Purpose

Use this guide for printable cheat sheets, formula sheets, quick references, and compact reference guides. These documents are for fast lookup during instruction, practice, assignments, and tests. They are not condensed textbooks.

The current reference implementation is [`../reference/TEJ-Electronics-Quick-Reference.qmd`](../reference/TEJ-Electronics-Quick-Reference.qmd). Its shared PDF styling is in [`tej-quick-reference-branding.tex`](tej-quick-reference-branding.tex), [`tej-preamble.tex`](tej-preamble.tex), and [`tej-print-bw.tex`](tej-print-bw.tex). This two-page LaTeX-generated PDF is the single student cheat sheet. The chaptered electronics handbook is a course book, not a second cheat sheet.

## Design goals

| Goal | Standard |
|:--|:--|
| Fast scanning | A student should find a symbol, rule, equation, or example within a few seconds. |
| Plain language | Use short sentences and familiar words. Explain a technical term where it first appears. |
| Print reliability | The document must remain clear when printed in black and white on an ordinary school printer. |
| Readability | Use 12 pt text where possible. Do not use text smaller than 10 pt, including table text and footers. |
| Visual calm | Use whitespace, page breaks, and small focused tables instead of packing every topic into one table. |
| Consistency | Use the same symbols, subscripts, units, schematic labels, and equation forms throughout. |
| Verifiable layout | Render and inspect every page. Equation spacing must also pass a measurable overlap check. |

## Page structure

Give each page one clear job. Keep related reference material together and begin a major topic on a new page when that improves scanning.

For the concise two-page student cheat sheet, use this order unless the course sequence requires otherwise:

1. quantities, letters, units, significant figures, the GUESS method, common metric prefixes, engineering-notation examples, and standard 5% resistor values;
2. Ohm's law, power, energy, derived-unit checks, parallel rules, and series rules.

Put parallel before series when following the TEJ Electronics Quick Reference sequence. Put only the prefixes used most often in the course on page 1. Keep the complete SI prefix table in the course notes or handbook so the cheat sheet remains concise.

## Typography

| Element | Standard |
|:--|:--|
| Body text | Liberation Sans, 12 pt where possible |
| Mathematics | Liberation Sans math letters, Greek letters, numerals, subscripts, and superscripts |
| Page title | Large, bold, centred, with a short subtitle |
| Section title | Large, bold, left aligned, with clear space above and below |
| Table text | 12 pt preferred, 10 pt minimum |
| Header | Course name on the left and `andrewandrade.ca` on the right |
| Footer | 10 pt minimum, light grey, and separated from page content |
| Colour | Black text on white; light grey table headers may be used |

Never place blue text on black or rely on colour to communicate meaning. Avoid decorative fonts. Do not use em dashes or en dashes in instructional text. Use commas, parentheses, colons, or ASCII hyphens instead.

For XeLaTeX documents that use `unicode-math`, apply the sans-serif math range after the document begins:

```tex
\AtBeginDocument{%
  \setmathfont[
    range={up/{Latin,latin,Greek,greek,num},it/{Latin,latin,Greek,greek},bfup/{Latin,latin,Greek,greek,num},bfit/{Latin,latin,Greek,greek}},
    Scale=MatchLowercase
  ]{Liberation Sans}%
}
```

Do not load `sansmath` beside `unicode-math`. Those packages conflict in this workflow.

## Tables

Use tables for structured reference information. Avoid bullet lists inside the student-facing reference unless a list is the clearest possible representation.

Use separate columns for separate ideas. For example, a core quantities table should use:

| Quantity | Letter | Unit | Unit symbol | Simple meaning |
|:--|:--:|:--|:--:|:--|
| Current | $I$ | ampere | A | How much electric charge is moving. |

Do not combine the unit name, unit symbol, variable, and explanation in one crowded cell. Break large collections into smaller subtables such as core quantities, significant figures, GUESS, Ohm's law, power, parallel rules, series rules, and SI prefixes.

Use a light grey header row, a strong top rule, and a strong bottom rule. Avoid full cell borders unless the table is an input area or a boxed note. Keep numerical and symbol columns narrow and explanation columns flexible.

## Equations and notation

Write equations as mathematics, not as typed approximations.

| Requirement | Example |
|:--|:--|
| Use a multiplication sign | $P=V\times I$ |
| Use a stacked fraction | $R=\dfrac{V}{I}$ |
| Use subscripts for totals | $V_T$, $I_T$, $R_T$, $P_T$ |
| Use numbered subscripts for parts or branches | $V_1$, $I_1$, $R_1$, $P_1$ |
| Use a source subscript when needed | $V_S$ |
| Keep related subscripts together | $R_1=\dfrac{V_1}{I_1}$ |

Explain subscripts on the circuit page where students use them. On the parallel page, identify total values and numbered branches. On the series page, identify total values and numbered components. Do not use a separate generic subscript section when the same idea can be taught beside the matching schematic and rules.

Put each major equation or concept on its own table row. Do not place several unrelated formulas in one paragraph. Align equations consistently so students can compare their structure.

Write final values as a number from 0 to 999 followed by the appropriate metric prefix and unit. For example, write $0.047\ \mathrm{A}$ as $47\ \mathrm{mA}$ and $4700\ \Omega$ as $4.7\ \mathrm{k}\Omega$.

Do not define a term by repeating the same term. For energy, use a concrete explanation such as, "How much work a source can provide or a load has used."

## Derived units

After the main Ohm's law, power, and energy equations, show how named units are built from other units. Use a short table and include these relationships:

| Named unit | Relationship |
|:--|:--|
| ohm | $1\ \Omega=1\ \mathrm{V}/1\ \mathrm{A}$ |
| watt | $1\ \mathrm{W}=1\ \mathrm{V}\times1\ \mathrm{A}=1\ \mathrm{J/s}$ |
| joule | $1\ \mathrm{J}=1\ \mathrm{W}\times1\ \mathrm{s}$ |
| watt-hour | $1\ \mathrm{Wh}=1\ \mathrm{W}\times1\ \mathrm{h}=3600\ \mathrm{J}$ |

State the time-unit rule explicitly: seconds give joules, while hours give watt-hours. Never state that one joule is one watt-hour.

Show where the factor of 3600 comes from: $1\ \mathrm{h}=60\ \mathrm{min}\times60\ \mathrm{s/min}=3600\ \mathrm{s}$, so $1\ \mathrm{Wh}=1\ \mathrm{W}\times3600\ \mathrm{s}=3600\ \mathrm{J}$.

Treat the values and units given in the question as the equation inputs. Use a heading such as `Question gives` instead of the vague phrase `Use when you know`. Give students direct unit clues, such as $\mathrm{V}/\mathrm{A}=\Omega$, $\mathrm{V}/\Omega=\mathrm{A}$, $\mathrm{A}\times\Omega=\mathrm{V}$, and $\mathrm{V}\times\mathrm{A}=\mathrm{W}$.

## Formula triangles

Place the Ohm's law, power, and energy triangles near the top of the main calculations page. Use one consistent triangle style:

| Triangle | Top | Bottom left | Bottom right |
|:--|:--:|:--:|:--:|
| Ohm's law | $V$ | $I$ | $R$ |
| Power | $P$ | $V$ | $I$ |
| Energy | $E$ | $P$ | $t$ |

Keep the triangles large enough to read at normal print size. Label each triangle below it. The triangles support equation recall but do not replace the full equation tables.

## Equation spacing

Automatic table row height is not enough for stacked fractions. Fractions extend above and below the normal text box and can collide with the equation in the next row even when the page appears acceptable at a quick glance.

Use these starting values for equation-heavy tables:

```tex
\renewcommand{\arraystretch}{1.55}
```

Add explicit clearance after rows that contain tall fractions:

```tex
Resistance & $\dfrac{1}{R_T}=\dfrac{1}{R_1}+\dfrac{1}{R_2}+\cdots$ & Add the reciprocals.\\[14pt]
Two resistors & $R_T=\dfrac{R_1\times R_2}{R_1+R_2}$ & Use this shortcut for two resistors.\\[6pt]
```

Treat these values as starting points, not proof that the result is correct. Font changes, page geometry, equation size, and adjacent content can change the required spacing.

### No-overlap acceptance rule

For adjacent equation rows, measure the rendered PDF text bounds:

```text
gap = top of the next equation - bottom of the previous equation
```

The gap must be at least 8 pt for stacked equations. A gap below 0 pt is a true overlap and fails review. A gap from 0 pt to less than 8 pt is too tight and must be increased.

The parallel-resistance table exposed the need for this rule. Its first render had the reciprocal denominator ending at 660.64 pt and the next numerator beginning at 657.66 pt. The calculated gap was -2.98 pt, so the characters overlapped. A later 4.02 pt gap was still visually too tight. It no longer passes this guide.

Do not approve an equation-dense page only by looking at a scaled screenshot. Inspect it at high resolution and measure the bounding boxes when rows contain fractions, superscripts, subscripts, radicals, matrices, or multi-line equations.

## Circuit rules pages

Give parallel and series circuits separate pages when space permits. Each page should contain:

| Element | Requirement |
|:--|:--|
| Subscript table | Place it before the schematic. Explain total, numbered branch or component, and source in that specific circuit. |
| Schematic | Use one large, clean, canonical schematic after the subscript explanation. |
| Rule table | Show voltage, current, resistance, and power relationships. Put each plain-language rule beside its equation. |
| Quick check | Add one short way to test whether the result is reasonable. |
| Summation notation | After the series rule, show $R_T=\sum_{i=1}^{n}R_i=R_1+R_2+\cdots+R_n$. |

Keep the one-path or multiple-path rule visible but subordinate to the equation it explains. For example, place "More than one path. The same voltage is across every branch." beside $V_T=V_1=V_2=\cdots$. Do not use an oversized banner when the sentence belongs with the rule table. Keep the equations aligned and use matching reference labels in the schematic and rule table.

Teach summation notation with a concrete case before expecting students to use the general form. Place the given component values directly below the schematic. In the worked example, align the equals signs and show one operation per line: the summation, the expanded terms, the substituted values with units, and the final total. For three resistors, use this sequence:

\[
\begin{aligned}
R_T &= \sum_{i=1}^{3}R_i \\
    &= R_1+R_2+R_3 \\
    &= \text{the three given resistance values} \\
    &= \text{the final resistance with its unit.}
\end{aligned}
\]

## Schematics

Use CircuitikZ or another approved schematic generator with actual electrical symbols. Do not use rough slide shapes or an automatically arranged Tinkercad schematic as the final reference image.

Schematics must:

1. be large enough to read at normal print size;
2. use straight, neat conductors and clear right-angle routing;
3. show junction dots where conductors connect;
4. avoid ambiguous wire crossings;
5. use consistent labels such as $V_S$, $R_1$, $R_2$, $I_1$, and $I_2$;
6. place explanatory captions below the drawing;
7. remain legible in black and white;
8. be reused from one canonical source instead of redrawn in several files.

For a nonstandard or real-world load, use the correct symbol when one exists. Otherwise, use a clean labelled box and put the plain-language component name below it.

## Examples and explanations

Include short examples beside or immediately after the rule they demonstrate. Do not make students search another page to understand a formula.

Use simple language such as:

| Avoid | Prefer |
|:--|:--|
| Select the applicable relationship according to the provided parameters. | Choose the equation that uses the values known in the problem. |
| Retain computational precision during intermediate operations. | Keep the full calculator value until the final answer. |

Keep significant-figure rules on separate lines or table rows. Show one concept per row. When calculator notation is included, use the same notation students see on the approved calculator.

## Print and page-fit rules

Use letter-sized pages unless another paper size is required. Keep at least 0.55 in margins and reserve enough space for the header and licence footer. Put the website in the header. Render the CC BY-SA licence footer in light grey so it remains available without competing with the instructional content. Do not allow a table, quick check, or schematic caption to touch the footer.

Do not solve page-fit problems by shrinking text below 10 pt. Use these remedies in order:

1. remove repeated wording;
2. split one large table into smaller tables;
3. move a major topic to a new page;
4. reduce decorative spacing that does not support scanning;
5. adjust margins only if the page remains comfortable to print and annotate.

## Required quality assurance

Every new or revised cheat sheet must pass all of the following checks before release:

| Check | Pass condition |
|:--|:--|
| Build | The source renders without LaTeX, Quarto, font, or missing-image errors. |
| Page count | The intended number of pages is confirmed with `pdfinfo`. |
| Visual inspection | Every page is rendered to PNG and reviewed at normal page view. |
| High-resolution inspection | Equation-heavy pages are reviewed at 300 dpi or equivalent. |
| Equation bounds | Adjacent stacked equations have at least 8 pt of measurable clearance. |
| Typography | Body and table text are 12 pt where possible and never below 10 pt. |
| Contrast | All content remains readable in black and white. |
| Schematics | Symbols, labels, junctions, paths, and captions are clear. |
| Page boundaries | Nothing is clipped, crowded against the footer, or outside the printable area. |
| Content consistency | Symbols, units, subscripts, terminology, and examples agree across every page. |
| Text hygiene | No em dashes or en dashes appear in instructional text. |

Render the complete final PDF again after the last spacing or font change. A successful compile is not proof of a correct layout.

## Release checklist

- [ ] The document has one clear purpose and a predictable page order.
- [ ] Parallel appears before series when using the TEJ Electronics sequence.
- [ ] Core quantities use separate quantity, letter, unit, unit-symbol, and meaning columns.
- [ ] Equations use sans-serif mathematics, stacked fractions, multiplication signs, and correct subscripts.
- [ ] Circuit-specific subscripts are explained before each matching schematic.
- [ ] Equation tables have enough vertical clearance for all fractions and subscripts.
- [ ] Measured equation gaps are at least 8 pt.
- [ ] Circuit diagrams are large, neat, canonical, and readable in black and white.
- [ ] Major plain-language rules appear beside the equations they explain.
- [ ] Significant-figure guidance uses separate lines or rows.
- [ ] Common metric prefixes are on page 1; the complete SI prefix table remains in the course notes or handbook.
- [ ] Final values include a number from 0 to 999, the metric prefix, and the unit.
- [ ] The Ohm's law, power, and energy triangles appear near the top of the calculations page.
- [ ] Derived-unit relationships correctly distinguish joules, watt-seconds, and watt-hours.
- [ ] Equation guidance identifies values and units from the question as inputs and shows how units help select or check the equation.
- [ ] The watt-hour conversion shows that 3600 comes from the number of seconds in one hour.
- [ ] Series rules include the general summation form and a concrete three-resistor example.
- [ ] Summation examples place givens below the schematic and align each calculation step at the equals sign.
- [ ] The website appears in the header and the licence footer is light grey.
- [ ] No body or table text is below 10 pt.
- [ ] Every page has been rendered and visually inspected.
- [ ] The final distribution PDF matches the inspected render.

## Release rule

A cheat sheet or reference guide is complete only when it is easy to scan, mathematically correct, readable in print, and free of measured overlap. If compactness conflicts with legibility, add space or add a page.

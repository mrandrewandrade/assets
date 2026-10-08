# TEJ cheat sheet and reference guide style guide

## Purpose

Use this guide for printable cheat sheets, formula sheets, quick references, and compact reference guides. These documents are for fast lookup during instruction, practice, assignments, and tests. They are not condensed textbooks.

The current reference implementation is [`../reference/TEJ-Electronics-Quick-Reference.qmd`](../reference/TEJ-Electronics-Quick-Reference.qmd). Its shared PDF styling is in [`tej-quick-reference-branding.tex`](tej-quick-reference-branding.tex), [`tej-preamble.tex`](tej-preamble.tex), and [`tej-print-bw.tex`](tej-print-bw.tex).

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

For an introductory electronics reference, use this order unless the course sequence requires otherwise:

1. quantities, letters, units, significant figures, and the GUESS method;
2. Ohm's law, power, energy, and the meaning of subscripts;
3. parallel circuits;
4. series circuits;
5. the complete SI prefix table.

Put parallel before series when following the TEJ Electronics Quick Reference sequence. Put the large SI prefix table at the end so it remains available without crowding the core formulas.

## Typography

| Element | Standard |
|:--|:--|
| Body text | Liberation Sans, 12 pt where possible |
| Mathematics | Liberation Sans math letters, Greek letters, numerals, subscripts, and superscripts |
| Page title | Large, bold, centred, with a short subtitle |
| Section title | Large, bold, left aligned, with clear space above and below |
| Table text | 12 pt preferred, 10 pt minimum |
| Footer | 10 pt minimum and separated from page content |
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

Explain the difference between a general equation and a circuit-specific equation. A plain variable such as $R=V/I$ states a general relationship. A subscripted equation such as $R_1=V_1/I_1$ identifies the values for one component or branch.

Put each major equation or concept on its own table row. Do not place several unrelated formulas in one paragraph. Align equations consistently so students can compare their structure.

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

The gap must be at least 4 pt for stacked equations. A gap below 0 pt is a true overlap and fails review. A gap from 0 pt to less than 4 pt is too tight and must be increased.

The parallel-resistance table exposed the need for this rule. Its first render had the reciprocal denominator ending at 660.64 pt and the next numerator beginning at 657.66 pt. The calculated gap was -2.98 pt, so the characters overlapped. After correction, the denominator ended at 657.33 pt and the next numerator began at 661.35 pt. The 4.02 pt gap passed.

Do not approve an equation-dense page only by looking at a scaled screenshot. Inspect it at high resolution and measure the bounding boxes when rows contain fractions, superscripts, subscripts, radicals, matrices, or multi-line equations.

## Circuit rules pages

Give parallel and series circuits separate pages when space permits. Each page should contain:

| Element | Requirement |
|:--|:--|
| Plain-language rule | Use a large statement such as `MORE THAN ONE PATH. SAME VOLTAGE ACROSS EVERY BRANCH.` |
| Schematic | Use one large, clean, canonical schematic. |
| Subscript table | Explain no subscript, total, numbered branch or component, and source. |
| Rule table | Show voltage, current, resistance, and power relationships. |
| Quick check | Add one short way to test whether the result is reasonable. |

Make the one-path or multiple-path rule visibly larger than ordinary body text. Keep the equations aligned and use matching reference labels in the schematic and rule table.

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

Use letter-sized pages unless another paper size is required. Keep at least 0.55 in margins and reserve enough space for the header and licence footer. Do not allow a table, quick check, or schematic caption to touch the footer.

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
| Equation bounds | Adjacent stacked equations have at least 4 pt of measurable clearance. |
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
- [ ] General variables and specific subscripted variables are explained.
- [ ] Equation tables have enough vertical clearance for all fractions and subscripts.
- [ ] Measured equation gaps are at least 4 pt.
- [ ] Circuit diagrams are large, neat, canonical, and readable in black and white.
- [ ] Major rules are visually prominent.
- [ ] Significant-figure guidance uses separate lines or rows.
- [ ] The SI prefix table is placed at the end.
- [ ] No body or table text is below 10 pt.
- [ ] Every page has been rendered and visually inspected.
- [ ] The final distribution PDF matches the inspected render.

## Release rule

A cheat sheet or reference guide is complete only when it is easy to scan, mathematically correct, readable in print, and free of measured overlap. If compactness conflicts with legibility, add space or add a page.

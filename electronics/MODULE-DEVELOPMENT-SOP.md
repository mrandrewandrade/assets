# TEJ electronics lesson-package style guide and SOP

## Purpose

Use this guide to create a coordinated TEJ electronics lesson package. The **Basic Electricity to Basic Computer Systems** package is the reference implementation, but future packages must follow the tighter lesson boundaries, five-question limit, textbook support, and visual rules below.

The standard package has three classroom artifacts:

1. a Google Slides teaching deck;
2. a student Google Doc with five assigned questions and five photo-upload spaces;
3. a restricted teacher Google Doc with complete worked answers to those same five questions.

A package teaches one coherent concept. If five questions cannot sample the required learning fairly, split the concept into two or more packages rather than adding a longer worksheet or an overloaded deck.

## Reference implementation

- [Basic Electricity to Basic Computer Systems slides](https://docs.google.com/presentation/d/1FD7od7Hi5-tcddWI44oEDzjqIKGQnsp7sOmaokiyH5o/edit)
- [Basic Circuit Calculations student handout](https://docs.google.com/document/d/11ooJTlUf7ckOjkTP9eyJr8FyojWuOHV9-IFjZ5IoCeA/edit)
- [Basic Circuit Calculations teacher answer key](https://docs.google.com/document/d/1Ux3gAje5iED6vO_gBcF7SbaBJ5TJkV5RqJmkc6XFtDw/edit)
- [TEJ Electronics Formula, Units, and Calculator Reference](https://docs.google.com/document/d/1DyGsEwpLrrwSRnyMXN5kze2qRYFoAY2t-P09wnfUS6c/edit)

Treat these as references for structure and division of roles. They are not permission to carry forward an error, an outdated photo workflow, or a question that does not match the new lesson.

## Technical source hierarchy

Use sources in this order:

1. **Grob's Basic Electronics, 12th edition** for technical explanations, chapter structure, examples, circuit rules, and terminology.
2. **Problems Manual for Grob's Basic Electronics** for solved-example patterns and graded practice problems.
3. **Experiments Manual for Grob's Basic Electronics** for practical verification, equipment use, and lab extensions.
4. **Open Circuits** for component cutaways and internal construction.
5. **ElectroBOOM** for a short, engaging conceptual introduction.
6. **The Organic Chemistry Tutor or Khan Academy** for a slower explanation or worked calculation review.
7. The TEJ electronics reference handbook for formulas, notation, calculator entry, and course conventions.

Internal textbook links for authorized classroom use:

- [Grob's Basic Electronics, 12th edition](https://drive.google.com/file/d/14nqYZQwgYer3mU_AjLOb_EXryzUtotqf/view)
- [Problems Manual for Grob's Basic Electronics](https://drive.google.com/file/d/14tvslnLyvOMci-5YBw_jHbHw_jxmsTfQ/view)
- [Experiments Manual for Grob's Basic Electronics](https://drive.google.com/file/d/15KJmGLXvTh0oivaqnV0SvWB7N64V1soT/view)

Do not publish textbook scans on the public website. Public materials may provide a bibliographic reference; classroom slides and handouts may link to the authorized Drive copy when students have permission to open it.

## Required chapter support

Every package must identify the chapter and section used. The same support line must appear in the deck and student question document.

Use this format:

> **Textbook support:** Grob, Chapter 3, Sections 3-1 to 3-9, pp. 76-93. **Practice support:** Problems Manual, Chapter 3, pp. 34-45.

The textbook title or support label must be clickable. Do not link only to a general references page when students need the assigned chapter. Keep the chapter and page range visible even when the link opens the whole book.

Place the support line:

- on the lesson-route or reference slide near the beginning;
- on the formula/rules slide;
- before Question 1 in the student document;
- at the beginning of the teacher answer document;
- beside any question that deliberately uses a different chapter.

When a figure, example, or problem pattern comes from a specific page, add a short local citation such as **[Grob, Ch. 5, p. 148]**. Paraphrase problem wording and change values or context while preserving the mathematical structure. Never imply that an invented question came from the book.

## Package boundary: the five-question rule

Five questions are the standard because the student document has five photo-upload spaces and each question should provide meaningful evidence. Five is not a reason to compress several lessons into one question.

A concept fits one package when all five questions use the same central model and no more than two new mathematical or representational moves are introduced.

Split the concept when any of the following is true:

- students need more than one substantially different circuit topology;
- the lesson introduces more than one new governing rule;
- troubleshooting requires a different reasoning process from normal operation;
- a new instrument or measurement method needs explicit instruction;
- the final question would contain several unrelated tasks merely to cover everything;
- a typical complete handwritten solution will not fit clearly on one page;
- the five questions cannot include introduction, transfer, and challenge without skipping an essential skill;
- the deck would require more than about 25–30 teaching slides before the question section.

When splitting, create Package A and Package B with separate decks, student documents, and answer documents. Reuse earlier formulas as prerequisite support, but do not repeat the entire earlier lesson.

## Pedagogical sequence

The classroom sequence is concrete, engaging, explanatory, symbolic, and then applied:

> Real system → ElectroBOOM → theory video → components → cutaways → symbols → clean schematic → rules and equations → guided example → five-question assignment → later review with the answer document

### 1. Show the real-world system

Start with the complete system so students know the purpose. For the first electricity lesson, show a battery, switch, conductors, and lamp operating together before isolating the individual parts.

The opening should answer:

- What is the system supposed to do?
- Where is electrical energy entering?
- What is the load?
- What will students be able to predict, measure, build, or troubleshoot?

### 2. Use ElectroBOOM for engagement

Play the relevant ElectroBOOM101 segment after the real example. Use only the episodes or excerpts that support the current lesson. The video creates interest and a memorable conceptual picture; it does not replace technical instruction.

For the introductory sequence, use ElectroBOOM101 episodes 1, 2, and 3 as appropriate. Do not insert the resistor episode when it is outside the current scope.

### 3. Use a theory video for support

Use The Organic Chemistry Tutor or Khan Academy for the slower explanation, derivation, or worked calculation. Give students the exact viewing purpose, such as:

> Watch for why voltage is measured between two points and why an ammeter must be placed in the current path.

Avoid a generic list of videos. Each video must be attached to one learning goal and placed where it supports that goal.

### 4. Move from physical components to symbols

For each component:

1. show the real classroom component;
2. show the same component beside an Open Circuits cutaway or a truthful functional internal view;
3. show the same real component beside its schematic symbol;
4. name its terminals, polarity, value, rating, and functional role;
5. show it inside the complete circuit schematic.

The real/cutaway and real/symbol comparisons must reuse the same photograph, orientation, name, and labels. Do not crop away terminals, polarity marks, switch contacts, or meter controls that students need to identify.

### 5. Convert the real setup into a schematic

Show the physical setup first and then redraw the same connections as a clean circuit schematic. Point out what was removed from the drawing and what information was preserved.

Use the canonical schematic generator. Do not draw circuits freehand in Google Slides. Standard symbols, visible junctions, realistic rectangular paths, unambiguous crossings, and consistent labels are required.

### 6. Teach the rule and general equation

Place a rule beside the schematic to which it applies. Series rules belong beside a series schematic; parallel rules belong beside a parallel schematic.

Use general equations while teaching:

- use `V = IR`, not a question-specific substituted equation;
- use total/branch notation only when the topology requires it;
- use true subscripts, not typed underscore notation such as `R_1`;
- typeset equations clearly and consistently;
- define every symbol and unit before students use it.

Question-specific equations appear only during a fully worked solution in the teacher answer document or the single guided example.

### 7. Model one guided example

Use a textbook solved-example structure or a close paraphrase with new values. Reveal the GUESS stages separately:

1. Given
2. Unknown
3. General Equations
4. Substitute and Solve
5. Statement

The guided example teaches the method. It must not be one of the five assigned questions and must not reveal the answer to an assigned question.

### 8. Assign the five questions

The slide deck introduces the assignment and links the student document. The student document contains the complete questions, canonical schematics, support links, and five photo-upload spaces. The restricted answer document contains the solutions.

Do not place complete assigned-question answers in the student-facing deck.

## Choosing the five questions

Choose questions by evidence required, not by arbitrary difficulty labels.

### Question 1 — direct transfer

Use the same central relationship and topology as the guided example, with a different context or values. Students should be able to begin independently.

### Question 2 — rearrangement or representation change

Change the unknown, require one algebraic rearrangement, or require students to move from a real component description to a schematic quantity.

### Question 3 — units and practical values

Use realistic component or device values and require engineering notation, metric prefixes, significant figures, or a device-label interpretation.

### Question 4 — multi-step application

Require an intermediate result, a total, a branch quantity, or a check using a second relationship. This is the first question that should clearly depend on full-precision intermediate values.

### Question 5 — synthesis or troubleshooting

Use the most difficult fair application of the lesson. Combine the current concept with one previously mastered skill, or ask students to explain a fault, rating, or design decision. Do not introduce an untaught topology or formula here.

### Selection process

1. List the lesson's observable learning goals.
2. Identify the Grob textbook section and Problems Manual section for each goal.
3. Select a solved example to model, but do not assign it unchanged.
4. Select or adapt five problem structures that collectively cover the learning goals.
5. Order them by the number of reasoning steps and amount of independence required.
6. Solve all five before publishing them.
7. Remove any duplicate question that provides the same evidence as another.
8. Split the package if an essential learning goal still has no fair question.

Do not create random word problems merely to reach five. Use authentic computer, automotive, sensor, power-supply, and classroom-component contexts only when the values and model are technically credible.

## Curriculum and Grob review

The TEJ basic-electronics pathway is broader than one five-question package. Grob's chapter structure confirms that the topics should be split as follows.

| TEJ concept | Grob support | Recommended packages | Reason |
|:--|:--|:--:|:--|
| Engineering notation and metric prefixes | Introduction, Sections I-1 to I-9, pp. 2-17 | 2 | Prefix conversion and calculator/precision work are different skills. |
| Charge, voltage, current, and a complete path | Chapter 1, pp. 22-49 | 1 | One physical model can support five mostly conceptual questions and one `I = Q/t` calculation. |
| Ohm's law | Chapter 3, Sections 3-1 to 3-6, pp. 76-85 | 1 | Five questions can cover all three unknowns, units, and interpretation. |
| Power, energy, opens, and shorts | Chapter 3, Sections 3-7 to 3-12, pp. 86-99 | 1 | Power equations, energy over time, and fault limits form a coherent extension of Ohm's law. |
| Resistors, colour code, ratings, and faults | Chapter 2, pp. 54-70 | 1 | Five questions can cover reading, selection, tolerance, rating, and failure. |
| Series circuits | Chapter 4, pp. 108-131 | 2 | Separate normal analysis from random unknowns, ground-referenced voltage, and troubleshooting. |
| Parallel circuits | Chapter 5, pp. 142-165 | 2 | Separate branch rules/basic analysis from random unknowns and fault behaviour. |
| Series-parallel circuits | Chapter 6, pp. 174-194 | 2 | Reduction/redrawing should be mastered before random unknowns and troubleshooting. |
| Voltage and current dividers | Chapter 7, pp. 208-221 | 2 | Unloaded dividers belong before loaded dividers and design. |
| Multimeters and measurement | Chapter 8, pp. 232-255 | 2 | Connection and safe use should precede loading effects and diagnostic use. |
| Kirchhoff's laws and node/loop methods | Chapter 9, pp. 264-281 | 2 | KCL/KVL fundamentals should precede branch-current and node-voltage analysis. |
| Conductors, switches, fuses, and temperature | Chapter 11, pp. 320-345 | 2 | Protection/components and wire-resistance/thermal calculations need different evidence. |
| Batteries and source behaviour | Chapter 12, pp. 350-378 | 2 | Cell connections/capacity should precede internal resistance and load behaviour. |
| Capacitors and time constants | Chapters 16 and 22, pp. 484-515 and 668-691 | 2 or 3 | Construction/value/connection, charging behaviour, and RC calculations should not be compressed. |
| Diodes and power-supply applications | Chapter 27, pp. 842 onward | 2 | Diode behaviour should precede rectification, filtering, and regulation. |
| Logic gates and truth tables | Experiments Manual, Supplemental A-1 to A-4, pp. 461-476 | 2 | Gate truth tables belong before multi-input logic and state. Grob is supplementary here, not the only theory source. |

### Decision for the current basic-electricity material

The current material should not be treated as one five-question lesson. It contains at least four packages:

1. **Electrical quantities and complete circuits** — Grob Chapter 1.
2. **Ohm's law and electrical power** — Grob Chapter 3.
3. **Parallel loads and totals in computer systems** — Grob Chapter 5 plus Chapter 3 power relationships.
4. **Multimeter connection and measurement** — Grob Chapter 8.

Open/short circuits and fuses may be taught with Package 1 as conceptual safety content, but if students must calculate fault current or diagnose faults, make that a separate package. The computer-system slides are a transfer/application deck and should not force extra calculation questions into the electrical-fundamentals assignment.

## Experiment recommendation and preparation

Every lesson package must review the matching Grob Experiments Manual section. The package record must either recommend an experiment, recommend a smaller adapted investigation, or state that no experiment is needed. Do not add a lab merely because the manual contains one.

For every recommended experiment, record:

1. the Grob experiment number and title;
2. the lesson goal it verifies;
3. whether it is a demonstration, simulation, physical investigation, or extension;
4. the exact equipment required;
5. the software required or optional;
6. the reusable components and consumables required;
7. any teacher preparation, prebuilt circuit, current limit, or fault station;
8. the measurements, table, graph, photograph, or explanation students submit;
9. the important safety boundary;
10. any adaptation from the published experiment and why it was made.

Use current-limited, protected extra-low-voltage sources for student circuit work. Do not reproduce a mains-powered procedure merely because it appears in a textbook. Replace obsolete or unavailable equipment with an equivalent modern measurement or simulation method, and document the change.

### Core reusable lab kit

The basic circuit investigations can share one kit:

- current-limited low-voltage DC bench supply or protected battery source;
- digital multimeter with fused current ranges and suitable leads;
- solderless breadboard;
- insulated jumpers and alligator leads;
- resistor assortment with known ratings;
- switches or pushbuttons;
- protected lamps, LEDs with current-limiting resistors, or other low-voltage loads;
- calculator and the TEJ electronics reference;
- safety glasses where component failure, wire trimming, or exposed conductors create a risk.

Tinkercad Circuits is the default introductory simulation when it supports the circuit. Multisim may be used for a closer match to the Grob manuals. KiCad is for later schematic and PCB work, not for replacing the introductory physical build. A spreadsheet is required only when the investigation produces enough measurements to justify a graph or fitted relationship.

### Recommended Grob experiment sequence

| TEJ package | Grob experiment suggestion | Equipment and components | Software | Consumables and preparation |
|:--|:--|:--|:--|:--|
| Engineering notation and calculator skills | Introduction Experiment: Electronics Math | Calculator and reference sheet | None | Printed or digital calculation prompts; no circuit parts |
| Electrical quantities, components, and safe setup | Experiment 1-1: Lab Safety, Equipment, and Components | Protected source, DMM, breadboard, resistor and component samples | Optional Tinkercad orientation | Prepare labelled components and one known-safe demonstration circuit |
| Resistance and resistor identification | Experiments 2-1 and 2-2 | DMM, resistor assortment, breadboard, protected source | Optional Tinkercad | Resistors with readable and partly obscured colour bands; replacement parts for damaged leads |
| Ohm's law and power | Experiments 3-1 and 3-2 | Current-limited supply, DMM, breadboard, several rated resistors | Tinkercad first; Multisim optional | Prepare value sets that stay below resistor power ratings |
| Series circuits | Experiments 4-1 to 4-4 | Supply, DMM, breadboard, three or more resistors, switch | Tinkercad or Multisim | Teacher-prepared removable open fault; no deliberate hard short |
| Parallel circuits | Experiments 5-1 to 5-4 | Fused/current-limited supply, DMM, breadboard, branch resistors | Tinkercad or Multisim | Teacher-prepared open-branch fault; verify total-current range before use |
| Series-parallel circuits | Experiments 6-1 to 6-4 | Supply, DMM, breadboard, resistor network | Multisim recommended before physical build | Prepare one canonical network and labelled reduction stages |
| Voltage and current dividers | Experiments 7-1 to 7-4 | Supply, DMM, fixed resistors, potentiometer, representative load | Tinkercad or Multisim | Check potentiometer pinout and resistor power before class |
| Multimeter fundamentals | Adapt measurement procedures from Experiments 1-1, 2-1, 3-1, 4-1, and 5-1 | DMM, fused leads, protected circuits, known-value resistors and battery | Optional meter simulation | Prepare stations for voltage, current, resistance, continuity, and a deliberate wrong-method discussion; do not energize an ohmmeter station |
| Conductors and insulation | Experiment 11-1 | DMM, wire samples, conductor and insulator samples | None | Cut and label equal-length samples; deburr sharp wire ends |
| Batteries and source behaviour | Experiments 12-1 and 12-2 | Cells or protected battery packs, holders, DMM, rated loads | Optional Multisim | Inspect cells; calculate safe load values; never short a cell |
| Capacitors and RC response | Experiments 16-1 and 22-1 | Capacitors, resistors, breadboard, DMM; oscilloscope or data logger for response curves | Multisim or Tinkercad where supported | Observe polarity and voltage ratings; discharge capacitors before handling |
| Diodes and power supplies | Experiments 27-1, 27-3, 27-4, and 27-5 | Diodes, resistors, capacitors, oscilloscope, isolated low-voltage AC source or function generator | Multisim recommended | Do not connect student breadboards directly to mains; prepare low-voltage rectifier parts and fault stations |
| Logic gates and truth tables | Supplemental Experiments A-1 to A-4 | 5 V regulated source, logic ICs, switches, pull resistors, LEDs and current-limiting resistors | Logisim Evolution, Tinkercad, or equivalent | Verify IC family, pinout, supply voltage, and unused-input handling before class |

The website lab index should show the recommended experiment, the minimum equipment, software, consumables, safety boundary, and status. Classroom-facing documents and the public site may link directly to the Google Drive Experiments Manual; the site must not host or redistribute the copyrighted PDF. The Drive file's own permissions control access.

## Artifact 1: Google Slides teaching deck

### Role

The deck tells the instructional story. It should teach, model, and prepare students for the assignment. It is not the student worksheet or the complete answer key.

### Required sections

1. Title and useful outcome
2. Real-world system
3. ElectroBOOM viewing prompt
4. Theory-video viewing prompt
5. Learning goals
6. Textbook and Problems Manual support links
7. Physical components and cutaways
8. Physical components and symbols
9. Complete clean schematic
10. Rules and general equations
11. One guided GUESS example
12. Assignment instructions and student-document link
13. Transfer, safety, or next-system connection
14. Sources and attribution

### Visual style

- Use sans-serif type throughout.
- Use one restrained palette; avoid large blue panels that compete with content.
- Use one main idea per slide.
- Use short statement titles rather than topic-only titles.
- Keep text, equation labels, and schematic labels readable from the back of the room.
- Use whitespace instead of squeezing or shrinking.
- Never allow text wrapping, clipping, or overflowing shapes.
- Use clear typeset equations with real subscripts and consistent variables.
- Keep a schematic close to the rule, example, or question that uses it.
- Do not stretch, distort, or heavily crop photographs or figures.
- Use colour as reinforcement, never as the only meaning carrier.
- Use red only for a genuine warning, misconception, or key solution note.
- Keep source notes concise and readable; keep the common licence footer consistent.

### Schematic standard

- Generate schematics with the established circuit generator.
- Use standard IEC/ANSI symbols consistently within the course.
- Use rectangular wiring paths and square corners where they make topology clearer.
- Use visible junction dots and unambiguous crossings.
- Label source, load, total, and branch quantities consistently.
- Place ammeters in series, voltmeters across two points, and resistance measurements only on de-energized circuits.
- Export one canonical high-quality schematic and reuse it in slides, student questions, and answers.
- Verify every schematic against the written problem before release.

## Artifact 2: student question and photo-submission Google Doc

### Role

The student document contains the five assigned questions and collects five photographs of handwritten work. It is not an answer key and does not contain teacher planning notes.

### Required structure

1. Assignment title and one-sentence purpose
2. Student identifier field
3. Short instructions
4. Textbook chapter link and visible chapter/page range
5. Problems Manual link and visible section/page range when used
6. Electronics reference-handbook link
7. GUESS expectations
8. Question 1 with its schematic and Photo 1 space
9. Question 2 with its schematic and Photo 2 space
10. Question 3 with its schematic and Photo 3 space
11. Question 4 with its schematic and Photo 4 space
12. Question 5 with its schematic and Photo 5 space
13. Submission check

Students complete one question per sheet and upload one clear, upright, cropped photograph of the complete page into the matching space. If a normal solution regularly needs a second page, reduce the question scope or split the package instead of designing a routine ten- or twelve-photo submission.

For every question, students must draw or copy the schematic by hand and show Given, Unknown, general Equations, Substitute and Solve, and a final Statement. They must show conversions, rearrangement, units, full-precision intermediate values, appropriate metric prefixes, and final precision.

Do not add estimated time, publication status, copyright administration, equipment inventories, or other teacher-planning material to the student document.

## Artifact 3: restricted teacher answer Google Doc

### Role

The teacher document contains complete solutions to the exact five assigned questions. Keep it restricted while the questions are assessed.

### Required structure for each answer

1. Exact question title and wording
2. Canonical schematic
3. Given table: quantity, symbol, value, unit
4. Unknown table: quantity, symbol, required unit
5. General equations
6. Algebraic rearrangement
7. Metric-prefix conversions
8. Substitution with units
9. Calculator entries, one per line
10. Full unrounded result before final rounding
11. Final results table
12. Plain-language answer statement
13. Short red key note only when a misconception, safety issue, or calculator trap deserves emphasis

Use `ANS` or calculator memory when later calculations depend on an earlier result. Do not re-enter rounded intermediate values. Match the Casio calculator model recommended for the course and keep each key sequence on its own line.

The answer document must use the same wording, topology, labels, values, units, order, and precision expectations as the student document.

## GUESS standard

### Given

List known quantities with schematic symbols, values, and units. Keep different variables on different rows or lines.

### Unknown

State exactly what must be found and the required unit. Do not hide prerequisite unknowns that must be calculated.

### Equations

Write the general relationships first. Do not insert question-specific subscripts until the exact solution step.

### Substitute and Solve

Rearrange symbolically, convert prefixes, substitute values with units, and show each calculator entry separately. Preserve full precision.

### Statement

Report every requested value with a symbol, unit, sensible engineering prefix, and correct precision. Finish with a sentence explaining the result in the real system.

## Alignment checklist

Before release, confirm that all three artifacts use the same:

- lesson title and learning goals;
- textbook chapter, sections, pages, and links;
- question order and exact wording;
- circuit topology and canonical schematic;
- values, units, variables, and subscripts;
- GUESS method and calculator conventions;
- significant-figure and rounding rules;
- expected final answers;
- electronics reference-handbook link;
- source and attribution treatment.

## Quality-assurance checklist

### Instruction

- [ ] The real system appears before isolated components.
- [ ] ElectroBOOM has a clear engagement purpose.
- [ ] The Organic Chemistry Tutor or Khan Academy has a clear theory purpose.
- [ ] Physical components lead to cutaways, symbols, and then a complete schematic.
- [ ] Rules and general equations are beside the relevant schematic.
- [ ] One guided example models GUESS without revealing an assigned answer.
- [ ] The lesson fits one coherent five-question package, or it has been split.
- [ ] The matching Grob experiment was reviewed and a lab, adaptation, or explicit no-lab decision is recorded.

### Questions and answers

- [ ] There are exactly five assigned questions and five photo spaces.
- [ ] Each question measures a distinct part of the learning goal.
- [ ] Question 5 is the hardest fair application, not a surprise topic.
- [ ] Every student question has a matching complete teacher answer.
- [ ] All three artifacts link the assigned Grob chapter and course reference.
- [ ] General equations appear before substitutions.
- [ ] Units, conversions, rearrangement, and precision are visible.
- [ ] Dependent calculations use unrounded values.
- [ ] Each answer ends with a results table and contextual statement.

### Visuals and schematics

- [ ] All text is sans-serif, legible, and free of overflow.
- [ ] Equations are typeset clearly with real subscripts.
- [ ] Component photographs are clear and correctly oriented.
- [ ] Cutaways are accurate and have a teaching purpose.
- [ ] Schematics come from the canonical generator.
- [ ] Junctions, crossings, labels, meter positions, and topology are correct.
- [ ] No meaning-bearing visual is stretched or unintentionally cropped.
- [ ] Third-party visuals and problem sources are attributed concisely.

### Google Classroom workflow

- [ ] The student document can be assigned as “make a copy for each student.”
- [ ] Each question has one stable photo-upload space.
- [ ] Students are told to crop, rotate, and check readability.
- [ ] The final check requires all five photos and the student identifier.
- [ ] Student links work with student permissions.
- [ ] Teacher-answer permissions remain restricted.

### Final verification

- [ ] Review every slide in presentation mode.
- [ ] Complete every question using only the provided information and linked support.
- [ ] Recalculate every answer independently.
- [ ] Test all five photo-upload spaces using a student copy.
- [ ] Check slides and Docs on a student-sized screen.
- [ ] Verify all chapter, video, reference, and assignment links.
- [ ] Verify the experiment number, equipment, software, consumables, preparation, evidence, and safety boundary.
- [ ] Confirm that no assigned answer appears in the student-facing deck.

## Release rule

The package is complete when the deck teaches one coherent concept, the student document collects five clear pieces of handwritten evidence, the teacher document solves those exact five questions, and all three artifacts link the relevant textbook chapter and course reference. If the required evidence does not fit this structure cleanly, split the concept into another package.

# TEJ electronics lesson-package SOP

## Purpose

Use this SOP to create a coordinated TEJ lesson package based on the existing **Basic Electricity to Basic Computer Systems** materials.

The standard package has three classroom artifacts:

1. a Google Slides teaching deck;
2. a student Google Doc containing the questions and handwritten-work submission spaces;
3. a restricted teacher Google Doc containing complete worked answers.

Component photographs, comparison diagrams, and clean circuit schematics support all three artifacts. A physical lab, simulation guide, or separate student worksheet is not part of this baseline package unless the lesson specifically requires one.

## Reference implementation

- [Basic Electricity to Basic Computer Systems slides](https://docs.google.com/presentation/d/1FD7od7Hi5-tcddWI44oEDzjqIKGQnsp7sOmaokiyH5o/edit)
- [Basic Circuit Calculations answers](https://docs.google.com/document/d/1Ux3gAje5iED6vO_gBcF7SbaBJ5TJkV5RqJmkc6XFtDw/edit)
- [Basic Circuit Calculations handwritten-work submission](https://docs.google.com/document/d/11ooJTlUf7ckOjkTP9eyJr8FyojWuOHV9-IFjZ5IoCeA/edit)

Treat these files as the reference for instructional structure and division of roles. Do not turn the package into a lab sequence unless requested.

## Pedagogical model

The package moves from concrete experience to symbolic reasoning and then back to authentic application:

> Familiar system → physical component → functional meaning → schematic symbol → clean circuit → worked method → student practice → computer-hardware application

The lesson also uses a gate:

> Students demonstrate the required electrical reasoning before they unlock the next hardware task.

This makes the calculation meaningful, gives the teacher a manageable checkpoint, and allows students who finish first to become pathfinders who help peers and improve the instructions.

## Artifact 1: teaching slide deck

### Role

The slide deck is the instructional story. It introduces concepts, connects real objects to electrical representations, models the calculation process, provides short practice, and shows how the learning unlocks the next task.

It is not a copy of the answer key and should not become a wall of text.

### Recommended lesson sequence

Use the parts that fit the topic while preserving the progression.

1. **Title and purpose** — name the lesson and show what it unlocks.
2. **Today's route** — show the major stages in plain language.
3. **Quantities, symbols, and units** — establish the technical vocabulary students need.
4. **Useful comparison** — compare related sources, systems, components, or representations.
5. **Misconception repair** — address ideas such as voltage being between two points, current requiring a complete path, or ground being a reference rather than a place where current disappears.
6. **Real component** — show the actual classroom object before expecting students to interpret its symbol.
7. **Internal view or mechanism** — use a cutaway or close-up when it explains what the component does.
8. **Schematic symbol and rule** — connect the physical object to the symbol, label, value, and connection rule.
9. **Complete class setup** — show the real arrangement and identify what students should find.
10. **Clean schematic** — redraw the same system without physical clutter.
11. **Circuit relationship** — show the current paths, voltage relationships, or power relationships directly on the schematic.
12. **GUESS overview** — Given, Unknown, Equations, Substitute and Solve, Statement.
13. **Worked example** — reveal one stage at a time rather than presenting the full solution at once.
14. **Guided practice** — use a similar problem with one meaningful variation.
15. **Independent question slides** — show the givens, schematic, and quantities to find without showing the worked answer.
16. **Faults, protection, and limits** — include opens, shorts, fuses, conductor capacity, ratings, or other relevant boundaries.
17. **Measurement or observation procedure** — show the correct setup when students must inspect or measure something.
18. **Transfer to the next system** — apply the lesson to computers or another authentic technology.
19. **Gate and completion criteria** — make the evidence required to continue visible.
20. **Sharing and attribution** — identify original and third-party material clearly.

### Slide design rules

- Put one main teaching idea on each slide.
- Use a short title that states the idea, not merely the topic.
- Prefer a labelled image, schematic, comparison, equation, or prompt to a dense paragraph.
- Show the real classroom component beside its schematic symbol when possible.
- Keep symbols and subscripts consistent across slides, questions, and answers.
- Put the schematic beside the givens for calculation questions.
- Link the current electronics quick-reference sheet from the GUESS overview or another clearly labelled reference slide.
- Reveal or discuss a prediction before showing the result.
- Keep body text, table text, schematic labels, and gate labels readable from the back of the classroom.
- Do not stretch photographs, screenshots, or schematics.
- Use colour to organize information, but never as the only carrier of meaning.
- Use the same attribution treatment throughout the deck. Put a concise source beside third-party media and keep the common licence footer consistent.

## Artifact 2: student question and submission Google Doc

### Role

The student document is a simple Google Classroom submission shell. Students solve each problem by hand, photograph the front and back of the work, and insert those photographs into clearly labelled spaces.

The document collects evidence without forcing students to reproduce mathematical notation or schematics with awkward Google Docs tools.

### Required structure

1. Lesson or assignment title
2. One-sentence purpose
3. Student number or other required identifier
4. Concise instructions
5. A direct link to the current electronics quick-reference sheet
6. GUESS requirements
7. Handwritten-work requirement
8. One clearly titled section for each question
9. The complete question text
10. A front-photo space
11. A back-photo space
12. A final submission check
13. Clean reference schematics for every question

The front and back photo spaces should use stable tables or image placeholders so students can click, replace the prompt, and keep the page organized. Require both sides even when the back is blank so submissions are consistent and missing work is easier to identify.

### Student work requirements

For every assigned question, students should:

1. copy or draw the circuit schematic by hand;
2. identify the given values with symbols and units;
3. state all unknowns;
4. write the general equations before substituting;
5. show conversions and rearrangement;
6. substitute values with units;
7. retain unrounded calculator values until the final step;
8. state the final answer using appropriate units and precision;
9. explain what the result means when requested;
10. submit clear, upright, cropped front and back photographs.

Do not add pages of teacher planning, estimated time, publishing status, copyright administration, or equipment lists to the student submission document.

## Artifact 3: restricted teacher answer Google Doc

### Role

The teacher answer document provides a complete, consistent model of the expected reasoning. It supports instruction, conferencing, and marking. It is not merely a list of final answers.

Keep the answer document restricted when the questions are being assessed.

### Required structure for each question

1. Repeat the exact question title and context.
2. Show the related schematic.
3. Link the current electronics quick-reference sheet beside the GUESS reference.
4. Provide a **Given** table with quantity, symbol, value, and unit.
5. Provide an **Unknowns** table with quantity, symbol, and required unit.
6. Write the general equations before inserting numbers.
7. Show rearrangement where needed.
8. Show metric-prefix conversions explicitly.
9. Put each calculator entry or calculation step on its own line.
10. Keep full calculator precision for dependent calculations.
11. Explain when to use `ANS` or calculator memory.
12. State the rounding or significant-figure rule.
13. Provide a results table with every requested quantity.
14. Finish with a plain-language answer statement.
15. Add a short teacher note only where it helps address a likely misconception or acceptable variation.

The answer key must follow the same question order, variable names, circuit labels, and wording as the student document.

## Question-set progression

A useful six-question progression is:

1. **Worked bridge problem** — connect a simple load calculation to a computer-system context.
2. **Single-load variation** — change a value or component while keeping the mathematical structure familiar.
3. **Parallel application** — combine branch quantities and total quantities.
4. **Different authentic context** — transfer the same equations to a USB, automotive, fan, heater, lighting, or computer example.
5. **Metric-prefix and equation-rearrangement problem** — require conversions before substitution.
6. **Comprehensive synthesis** — solve voltage, current, resistance, power, totals, and equivalent resistance in one labelled circuit.

The sequence should increase independence and mathematical demand without changing every feature at once. Early questions reinforce the method; later questions combine representations, conversions, and circuit rules.

## GUESS standard

Use GUESS consistently in slides, questions, and answers.

### Given

List the known quantities with matching schematic symbols, values, and units.

### Unknown

State exactly what must be found. Keep different variables on separate lines or in separate table rows.

### Equations

Write general relationships first. Use $V$, $I$, $R$, and $P$ before inserting the particular circuit subscripts.

### Substitute and solve

Use the symbols and subscripts from the schematic. Show conversions and rearrangement. Put separate calculator entries on separate lines. Preserve unrounded intermediate results with `ANS` or memory.

### Statement

Give the final values with symbols, units, sensible metric prefixes, and correct precision. Finish with a sentence explaining the result in the context of the system.

## Components, photographs, and schematics

### Concrete-to-symbolic sequence

Whenever students will handle or identify a component, use this progression:

1. class setup or authentic system photograph;
2. isolated component photograph or close-up;
3. component name and functional role;
4. schematic symbol and connection rule;
5. clean schematic using that component;
6. calculation or decision based on the schematic.

This helps students understand that the photograph and schematic are two representations of the same system rather than unrelated pictures.

### Schematic rules

- Use the established schematic generator instead of drawing circuits manually in Slides or Docs.
- Use standard electrical symbols and consistent reference labels.
- Label sources, loads, branch quantities, totals, values, and units clearly.
- Use visible junctions and unambiguous crossings.
- Keep series and parallel relationships visually obvious.
- Put meters in their correct electrical positions.
- Leave enough whitespace for projection and printing.
- Export a high-quality format suitable for both Slides and Google Docs.
- Reuse one canonical schematic everywhere rather than maintaining slightly different copies.

### Media selection

Use original classroom photographs when the physical object or setup matters. Use a cited cutaway or technical figure only when it reveals something the exterior cannot show. Every image must have a teaching purpose: identify, compare, explain a mechanism, connect representations, or support a decision.

## Why the package supports good pedagogy

| Feature | Why it helps students |
|:--|:--|
| Clear route | Students can see where the lesson is going and what will unlock next. |
| Familiar computer and automotive contexts | Abstract quantities become connected to systems students recognize. |
| Real component followed by schematic symbol | Students learn to translate between physical hardware and engineering drawings. |
| Misconception slides | Incorrect mental models are addressed before they become calculation habits. |
| GUESS worked example | Expert problem-solving steps become visible and repeatable. |
| General equation before substitution | Students learn relationships instead of memorizing calculator recipes. |
| Separate calculator-entry guidance | Calculator syntax does not become a hidden barrier to demonstrating understanding. |
| Full precision until the final step | Students avoid accumulated rounding error and learn professional calculation habits. |
| Guided then independent practice | Support is reduced gradually instead of disappearing all at once. |
| Progressive six-question set | Difficulty grows through controlled changes, transfer, and synthesis. |
| Handwritten solutions | The teacher can see diagrams, setup, reasoning, corrections, and not only a typed final answer. |
| Google Doc photo submission | Students retain handwritten mathematical work while gaining an organized digital submission. |
| Complete teacher model | Feedback can address method, notation, units, precision, and interpretation consistently. |
| Hardware gate | The calculation has an immediate purpose and important checkpoints remain manageable. |
| Pathfinder role | Faster students deepen learning by explaining and improving instructions rather than simply racing ahead. |

## Alignment checklist

Before release, confirm that all three artifacts use the same:

- lesson title and purpose;
- question order and wording;
- circuit topology and schematic;
- component values and units;
- variable names and subscripts;
- GUESS steps;
- calculator conventions;
- precision and significant-figure rules;
- expected final answers;
- the current electronics quick-reference link;
- source links and attribution.

The slides may include one fully worked example and guided practice. They should not reveal all answers to the assigned student questions before those questions are completed.

## Quality-assurance checklist

### Instructional quality

- [ ] The lesson moves from concrete objects to symbolic representation.
- [ ] Prerequisite quantities, units, and relationships are reviewed.
- [ ] At least one common misconception is addressed explicitly.
- [ ] A worked example models the complete GUESS process.
- [ ] Practice moves from guided to independent.
- [ ] The final task connects to an authentic system or the next course activity.
- [ ] The gate requires meaningful evidence rather than simple completion.

### Questions and answers

- [ ] Every student question has a matching worked answer.
- [ ] The slide deck, student document, and answer key link the same electronics quick-reference sheet.
- [ ] Question numbers, wording, diagrams, values, and unknowns match.
- [ ] Givens and unknowns are visually separated.
- [ ] General equations appear before substitutions.
- [ ] Conversions, units, rearrangement, and precision are shown.
- [ ] Dependent calculations use unrounded values.
- [ ] Each solution ends with a results table and answer statement.
- [ ] The teacher document remains restricted.

### Visuals and schematics

- [ ] Component photographs are clear, relevant, and correctly oriented.
- [ ] Schematics come from the canonical generator.
- [ ] Symbols, labels, junctions, and meter positions are correct.
- [ ] Text and schematic labels are readable in class and on student devices.
- [ ] Meaning-bearing visuals are not cropped or stretched.
- [ ] Third-party visuals have concise, accurate attribution.

### Google Classroom use

- [ ] The student document can be assigned as “make a copy for each student.”
- [ ] Student number and instructions are easy to find.
- [ ] Each question has stable front and back photo spaces.
- [ ] Students are told to crop, rotate, and check readability.
- [ ] The final submission check states exactly what must be present.
- [ ] All links open with the intended student or teacher permissions.

### Final verification

- [ ] Review every slide in presentation mode.
- [ ] Complete every student question using only the provided information.
- [ ] Recalculate every teacher answer independently.
- [ ] Test the student-photo workflow using a copy of the Google Doc.
- [ ] Check the deck and both documents on desktop and a student-sized screen.
- [ ] Confirm that the public deck, student document, and restricted answer document have the correct access settings.

## Release rule

The lesson package is complete when the deck teaches the ideas, the student document collects the intended evidence, and the teacher document models and verifies every solution. Additional labs, simulations, handbooks, or website pages are separate enhancements and should be added only when they serve the lesson.

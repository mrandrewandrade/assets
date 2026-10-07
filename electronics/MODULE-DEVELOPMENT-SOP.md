# TEJ electronics module development SOP

## Purpose

Use this SOP to create a complete TEJ electronics learning module rather than a disconnected slide deck or worksheet. H01 Safety and Lab Practice is the current reference implementation.

The module should help students move from a familiar physical system to an engineering model, make a prediction, calculate, verify, build safely, troubleshoot, and explain what the evidence means.

## Required instructional sequence

Use this sequence unless the topic makes one stage genuinely unnecessary:

1. State one clear learning goal and observable success criteria.
2. Activate prerequisite knowledge with a short retrieval question or diagnostic prompt.
3. Begin with a real object, application, or failure students can recognize.
4. Show the inside view or component construction when it explains behaviour.
5. Reduce the system to functional blocks such as source, protection, control, conductors, input, processor, driver, and load.
6. Show a proper schematic using standard symbols, reference labels, values, rails, and readable junctions.
7. Identify each component's role and the check required before power is applied.
8. Ask for a qualitative prediction before presenting equations or simulator results.
9. Model the calculation with GUESS: Given, Unknown, Equation, Substitute, and Statement.
10. Show the exact calculator entry on separate lines, retain full precision internally, and round only the final answer.
11. Have students calculate before they simulate or build.
12. Use simulation to verify a prediction, compare values, and identify a limitation of the model.
13. Use a pre-power inspection and teacher approval gate before a physical build.
14. Measure the physical circuit and compare calculated, simulated, and measured evidence.
15. Introduce one safe, teacher-approved fault and require diagnosis from evidence.
16. Finish with transfer, reflection, cleanup, and a short exit check.

The common evidence cycle is:

> Predict → calculate → draw → simulate or verify → build or test → compare → diagnose → explain → reflect

## Complete module package

Each complete hardware module should include the following coordinated materials.

### Module metadata

Create `module.yml` with the module identifier, topic, audience, requirement level, components, equipment, contexts, difficulty, curriculum connections, technical references, safety category, source and download paths, website and slide links, version, review status, and asset list.

Metadata makes the module searchable and keeps the website, build system, and curriculum map consistent.

### Lesson slides

The slides guide teacher-led instruction and discussion. They should include:

- the lesson route and learning goal;
- a real object or authentic context;
- an internal view, functional block diagram, and proper schematic where relevant;
- component roles and safety limits;
- a prediction prompt before the worked solution;
- a worked GUESS example and exact calculator entries;
- brief checks for understanding with answers revealed after students commit;
- simulation, build, measurement, and troubleshooting instructions;
- reflection, downloads, and an exit check.

Keep one main idea on each slide. Prefer a labelled visual, equation, table, or question over a dense paragraph. Use the same circuit, values, symbols, terminology, and sequence as the worksheet and answer key.

### Student worksheet or question set

The student document records thinking and evidence. It should contain:

- student name, date, and class fields;
- the document role and evidence cycle;
- the reference schematic before related calculations;
- enough working space for calculations, diagrams, and explanations;
- required questions that establish essential understanding;
- optional challenge questions that deepen transfer and design reasoning;
- explicit unknowns, precision, units, calculator expectations, and simulation expectations;
- places to record calculated, simulated, and measured values;
- a common assessment rubric or evidence checklist.

A strong ten-question pattern is:

1. Predict and calculate the central quantity.
2. Recreate or verify the system in a simulator.
3. Identify functional roles and make a justified design or protection choice.
4. Plan safe measurement and correct meter placement.
5. Diagnose a common open, short, incorrect value, polarity, or signal fault.
6. Redesign an unsafe or ineffective system.
7. Explain an internal component mechanism or cutaway.
8. Transfer the idea to another authentic context.
9. Diagnose a procedural mistake and propose prevention.
10. Synthesize the work into a safety case, design justification, or reflection.

Questions 1 to 5 normally provide the required evidence. Questions 6 to 10 provide extension or higher-level evidence without withholding the core learning from other students.

### Teacher answer key

The key must follow the student question order exactly. It should model the quality of reasoning expected, not merely list final numbers.

For calculations, include:

1. givens and unknowns on separate lines or in clear tables;
2. the general equation before numerical substitution;
3. rearrangement where required;
4. substituted values with units;
5. exact calculator entries on separate lines;
6. unrounded intermediate values where later parts depend on them;
7. a final value with appropriate units and significant figures;
8. a plain-language answer statement;
9. rating, safety, or model-limit checks;
10. teacher notes for likely misconceptions, acceptable variation, and required evidence.

The answer key is a restricted teacher resource when publishing student-facing pages.

### Simulation guide

Include a separate simulation guide when students must construct, measure, or troubleshoot in software. It should preserve the sequence “calculate first, simulate second, build third” and include:

- construction steps based on the proper schematic;
- component values and polarity checks;
- correct meter placement;
- a calculated-versus-simulated comparison table;
- percent difference where meaningful;
- required screenshots or share links;
- one discrepancy explanation;
- at least one stated limitation of the simulator.

Simulation verifies a model and rehearses procedure. It does not replace the hand calculation or certify physical safety.

### Physical lab handout

Include a separate lab when physical construction or measurement is part of the learning. It should contain:

- learning goal and prerequisite evidence;
- approved equipment and consumables;
- voltage, current, temperature, mechanical, and stored-energy limits;
- explicit stop conditions;
- calculation and simulation gates before construction;
- pre-power inspection, partner trace, and teacher approval;
- numbered build and measurement steps;
- tables comparing calculated, simulated, and measured evidence;
- a safe, teacher-approved troubleshooting task;
- cleanup, evidence submission, and reflection.

Do not use destructive faults. Never ask students to probe mains circuits or defeat protection.

### Schematics, cutaways, and reference visuals

Create visuals with the established CircuitikZ/TikZ generation workflow and export reusable PDF and accessible SVG versions. Do not redraw a rough replacement inside each document.

Use three different representations for three different purposes:

1. **Real object or cutaway:** what the device looks like and what is inside it.
2. **Functional block diagram:** what each part does and how energy or information moves.
3. **Schematic:** how the electrical nodes and components are connected.

Schematics should use standard symbols, visible values and reference labels, consistent rails, unambiguous junctions, readable text, and enough whitespace for print and projection. Captions and alternative text must say what students should notice.

### Reference support

Connect the module to the two-page quick reference and the fuller electronics handbook. Add or revise a handbook section when students need durable explanations, formulas, component limits, reference circuits, or troubleshooting guidance beyond the lesson.

Technical statements and adapted ideas require chapter- or page-level references where possible. Keep copyrighted source files in restricted Drive and publish only original explanations, diagrams, activities, and permitted links.

### Website module page

The public page should act as the module hub. Include the learning route, public downloads, slide link, schematic and reference links, safety boundary, curriculum connections, and references. Teacher keys and licensed textbook materials should be clearly marked restricted.

## Why these elements support good pedagogy

| Element | Pedagogical purpose |
|:--|:--|
| Authentic object or problem | Gives the abstract idea a reason to exist and supports transfer. |
| Real object, block diagram, and schematic | Builds connections between physical appearance, system function, and electrical representation. |
| Prediction before explanation | Exposes prior thinking and makes the result something students can test. |
| Worked GUESS example | Makes expert problem-solving steps visible and reduces avoidable cognitive load. |
| Exact calculator entries | Removes calculator syntax as a hidden barrier while preserving mathematical reasoning. |
| Required and optional questions | Establishes a common core while allowing extension without rushing ahead. |
| Calculation before simulation | Prevents trial-and-error clicking from replacing a physical model. |
| Simulation before physical build | Provides rapid feedback and a safe rehearsal of connections and meter placement. |
| Physical measurement | Connects ideal models to tolerances, noise, limits, and real equipment. |
| Calculated-simulated-measured comparison | Teaches that engineering claims require converging evidence, not one answer source. |
| Safe inserted fault | Develops systematic troubleshooting instead of part swapping. |
| Reflection and transfer | Requires students to explain what changed, what the model omitted, and where the idea applies next. |
| Matched answer key | Supports consistent feedback and shows complete reasoning, units, precision, and interpretation. |
| Reusable references | Reduces memory burden during practice and supports increasing independence. |

## Alignment rules

Before release, confirm that every artifact uses the same:

- module identifier and title;
- learning goal and technical vocabulary;
- circuit topology, component values, reference labels, and units;
- schematic source;
- question numbering and required-versus-optional distinction;
- formulas, calculator sequence, and final precision;
- safety limits, approval gates, and stop conditions;
- public and restricted access labels;
- citations and destination links.

Change the canonical source first, regenerate derivatives, and then update links. Do not manually patch exported PDFs or copied schematics.

## Quality-assurance checklist

### Content

- [ ] Learning goal describes an observable student capability.
- [ ] Prerequisites are taught or checked.
- [ ] Technical claims and adapted ideas have suitable references.
- [ ] The real context, model, calculation, and application agree.
- [ ] Every question produces evidence that can be assessed.
- [ ] Required work is achievable without completing optional challenges.

### Mathematics and electronics

- [ ] Symbols are defined before use.
- [ ] Givens and unknowns are visually separated.
- [ ] General equations precede substitutions.
- [ ] Units are carried through the work.
- [ ] Intermediate values retain enough precision.
- [ ] Final precision and metric prefixes are sensible.
- [ ] Component ratings and operating limits are checked.
- [ ] Schematics are electrically correct and readable.

### Safety and inclusion

- [ ] The safety category and stop conditions are explicit.
- [ ] The activity uses teacher-approved protected low voltage.
- [ ] Meter procedures include jack, function, range, placement, and power state.
- [ ] Teacher approval occurs before energizing or introducing a fault.
- [ ] Visuals have useful captions and alternative text.
- [ ] Colour is not the only carrier of meaning.
- [ ] Printed text, equations, gate labels, and schematic labels remain readable.
- [ ] Instructions use direct, plain language while preserving correct technical terms.

### Package and publication

- [ ] Slides, worksheet, answer key, simulation guide, lab, references, and module page agree.
- [ ] `module.yml` is complete and lists every deliverable.
- [ ] Public student resources and restricted teacher resources are separated.
- [ ] Source files build without errors.
- [ ] PDFs are rendered and visually inspected page by page.
- [ ] SVGs are inspected at presentation and print sizes.
- [ ] Website and download links are tested.
- [ ] Mobile and desktop website views are checked.
- [ ] Version, review status, and updated date are current.

## Build and review

From the `assets` repository root, render maintained electronics outputs with:

```bash
bash render.sh electronics
```

On Windows PowerShell when Git Bash or WSL is unavailable, use:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/render-electronics.ps1
```

Review the generated PDF and SVG outputs visually. Then render the companion slide deck and public website, test every link, and verify that teacher-only resources remain restricted. A module is not complete merely because its source compiles.

## Reference implementation

Use `electronics/modules/H01-safety-lab-practice/` as the reference package. Its slides, student worksheet, teacher answer key, Tinkercad guide, physical lab, generated schematics, handbook links, metadata, and website hub demonstrate the intended division of roles and the full evidence cycle.

#let render(colour: true) = {
  let black = rgb("#000000")
  let white = rgb("#FFFFFF")
  let navy = rgb("#1D2347")
  let blue = rgb("#0072B2")
  let gold = rgb("#FCD937")
  let pale-gold = rgb("#FFF8D8")
  let primary = if colour { navy } else { black }
  let secondary = if colour { blue } else { black }
  let accent = if colour { gold } else { black }
  let header-fill = if colour { gold } else { white }
  let eval-fill = if colour { pale-gold } else { white }
  let footer-ink = if colour { rgb("#3C454D") } else { black }

  set page(
    paper: "us-letter",
    flipped: true,
    margin: (top: 0.30in, bottom: 0.46in, x: 0.42in),
    footer: context [
      #set text(
        font: ("Arial", "Liberation Sans", "DejaVu Sans"),
        size: 6.5pt,
        fill: footer-ink,
        hyphenate: false,
      )
      #grid(
        columns: (1fr, auto),
        column-gutter: 12pt,
        [Technology Commons - Weekly SMART Goal + Learning Skills],
        [Page #counter(page).display("1 of 1", both: true)]
      )
    ]
  )

  set text(
    font: ("Arial", "Liberation Sans", "DejaVu Sans"),
    size: 8.4pt,
    fill: black,
    hyphenate: false,
  )
  set par(leading: 0.48em, justify: false)

  let identity-fields(score: true) = [
    #grid(
      columns: (1fr, 1fr, 1fr, auto),
      column-gutter: 14pt,
      align: horizon,
      [
        #text(weight: "bold")[Name:]
        #h(5pt)
        #line(length: 2.10in, stroke: 0.7pt + black)
      ],
      [
        #text(weight: "bold")[Course:]
        #h(5pt)
        #line(length: 1.70in, stroke: 0.7pt + black)
      ],
      [
        #text(weight: "bold")[Week of:]
        #h(5pt)
        #line(length: 1.70in, stroke: 0.7pt + black)
      ],
      [#if score [#text(size: 10pt, weight: "bold")[/20]]],
    )
  ]

  let page-header(title, subtitle, score: true, title-size: 22pt) = [
    #grid(
      columns: (1fr, 2.75in),
      column-gutter: 18pt,
      align: top,
      [
        #text(size: title-size, weight: "bold", fill: primary)[#title]
        #v(2pt)
        #text(size: 10pt, weight: "bold")[#subtitle]
        #v(5pt)
        #line(length: 0.66in, stroke: 3pt + accent)
      ],
      [
        #grid(
          columns: (0.58in, 1fr),
          column-gutter: 8pt,
          align: horizon,
          [#image("technology-department-emblem.svg", width: 0.54in)],
          [
            #text(size: 8.4pt, weight: "bold", fill: primary)[Technology Commons]
            #linebreak()
            #text(size: 7.7pt)[Port Credit Secondary School]
            #linebreak()
            #text(size: 7.5pt, weight: "bold")[May the Light Never Fail.]
          ],
        )
      ],
    )
    #v(4pt)
    #line(length: 100%, stroke: 1.2pt + secondary)
    #v(6pt)
    #identity-fields(score: score)
    #v(8pt)
  ]

  let goal-lines = [
    #text(size: 7.8pt, weight: "bold")[Specific]
    #v(4pt)
    #line(length: 100%, stroke: 0.65pt + black)
    #v(7pt)
    #text(size: 7.4pt, weight: "bold")[Measurable (by end of class, I will have)]
    #v(4pt)
    #line(length: 100%, stroke: 0.65pt + black)
    #v(7pt)
    #text(size: 7.4pt, weight: "bold")[Attainable, Realistic, Timely]
    #v(4pt)
    #line(length: 100%, stroke: 0.65pt + black)
  ]

  let progress-lines = [
    #text(size: 7.8pt, weight: "bold")[In detail, explain what you accomplished / learned today.]
    #v(7pt)
    #line(length: 100%, stroke: 0.65pt + black)
    #v(10pt)
    #line(length: 100%, stroke: 0.65pt + black)
    #v(10pt)
    #line(length: 100%, stroke: 0.65pt + black)
    #v(10pt)
    #line(length: 100%, stroke: 0.65pt + black)
  ]

  let evaluation-box = block(
    width: 100%,
    fill: eval-fill,
    stroke: 0.8pt + primary,
    radius: 4pt,
    inset: 6pt,
    [
      #text(size: 8pt, weight: "bold", fill: primary)[Teacher evaluation]
      #v(5pt)
      #grid(
        columns: (1fr, auto),
        row-gutter: 4pt,
        [#text(size: 7pt)[Neatly written]], [#box(width: 8pt, height: 8pt, stroke: 0.7pt + primary)],
        [#text(size: 7pt)[Detailed information]], [#box(width: 8pt, height: 8pt, stroke: 0.7pt + primary)],
        [#text(size: 7pt)[Technical terms]], [#box(width: 8pt, height: 8pt, stroke: 0.7pt + primary)],
      )
      #v(5pt)
      #text(size: 7pt, weight: "bold")[Level]
      #h(6pt)
      #text(size: 7pt)[1]
      #box(width: 7pt, height: 7pt, stroke: 0.7pt + primary)
      #h(4pt)
      #text(size: 7pt)[2]
      #box(width: 7pt, height: 7pt, stroke: 0.7pt + primary)
      #h(4pt)
      #text(size: 7pt)[3]
      #box(width: 7pt, height: 7pt, stroke: 0.7pt + primary)
      #h(4pt)
      #text(size: 7pt)[4]
      #box(width: 7pt, height: 7pt, stroke: 0.7pt + primary)
    ]
  )

  let daily-card(day) = block(
    width: 100%,
    height: 1.78in,
    fill: white,
    stroke: 1pt + primary,
    radius: 5pt,
    inset: 0pt,
    clip: true,
    [
      #block(
        width: 100%,
        height: 0.30in,
        fill: header-fill,
        inset: (x: 8pt, y: 4pt),
        [
          #grid(
            columns: (1.10in, 1fr),
            column-gutter: 8pt,
            align: horizon,
            [#text(size: 12.5pt, weight: "bold", fill: primary)[#day]],
            [#text(size: 8pt, weight: "bold")[Set a SMART goal for today]],
          )
        ],
      )
      #line(length: 100%, stroke: 0.7pt + primary)
      #v(5pt)
      #pad(x: 8pt)[
        #grid(
          columns: (3.08in, 1fr, 1.55in),
          column-gutter: 12pt,
          align: top,
          [#goal-lines],
          [#progress-lines],
          [#evaluation-box],
        )
      ]
    ]
  )

  let weekly-review = block(
    width: 100%,
    height: 1.72in,
    fill: white,
    stroke: 1pt + primary,
    radius: 5pt,
    inset: 8pt,
    [
      #text(size: 13pt, weight: "bold", fill: primary)[Weekly Progress Check]
      #v(2pt)
      #line(length: 0.48in, stroke: 2.4pt + accent)
      #v(6pt)
      #text(size: 8pt, weight: "bold")[What progress did you make toward your goals this week?]
      #v(6pt)
      #line(length: 100%, stroke: 0.65pt + black)
      #v(10pt)
      #line(length: 100%, stroke: 0.65pt + black)
      #v(10pt)
      #line(length: 100%, stroke: 0.65pt + black)
      #v(10pt)
      #text(size: 8pt, weight: "bold")[What is one specific next step for next week?]
      #v(6pt)
      #line(length: 100%, stroke: 0.65pt + black)
      #v(10pt)
      #line(length: 100%, stroke: 0.65pt + black)
    ]
  )

  let reflection-box(title, prompt) = block(
    width: 100%,
    height: 2.62in,
    fill: white,
    stroke: 1pt + primary,
    radius: 5pt,
    inset: 0pt,
    clip: true,
    [
      #block(
        width: 100%,
        height: 0.34in,
        fill: header-fill,
        inset: (x: 8pt, y: 5pt),
        [#text(size: 13pt, weight: "bold", fill: primary)[#title]],
      )
      #line(length: 100%, stroke: 0.7pt + primary)
      #pad(x: 8pt, top: 6pt)[
        #text(size: 7.8pt, weight: "medium")[#prompt]
      ]
    ]
  )

  let rating-box = block(
    width: 100%,
    fill: eval-fill,
    stroke: 0.8pt + primary,
    radius: 4pt,
    inset: 6pt,
    [
      #text(size: 7.4pt, weight: "bold", fill: primary)[RATING]
      #v(10pt)
      #text(size: 8pt, weight: "bold")[E]
      #box(width: 9pt, height: 9pt, stroke: 0.7pt + primary)
      #h(7pt)
      #text(size: 8pt, weight: "bold")[G]
      #box(width: 9pt, height: 9pt, stroke: 0.7pt + primary)
      #h(7pt)
      #text(size: 8pt, weight: "bold")[S]
      #box(width: 9pt, height: 9pt, stroke: 0.7pt + primary)
      #h(7pt)
      #text(size: 8pt, weight: "bold")[N]
      #box(width: 9pt, height: 9pt, stroke: 0.7pt + primary)
    ]
  )

  let skill-card(title, description) = block(
    width: 100%,
    height: 0.79in,
    fill: white,
    stroke: 0.9pt + primary,
    radius: 4pt,
    inset: 8pt,
    [
      #grid(
        columns: (3.25in, 1fr, 1.55in),
        column-gutter: 12pt,
        align: top,
        [
          #text(size: 10.5pt, weight: "bold", fill: primary)[#title]
          #v(5pt)
          #text(size: 7pt)[#description]
        ],
        [
          #text(size: 8pt, weight: "bold")[How have you demonstrated or improved this?]
          #v(9pt)
          #line(length: 100%, stroke: 0.65pt + black)
          #v(10pt)
          #line(length: 100%, stroke: 0.65pt + black)
        ],
        [#rating-box],
      )
    ]
  )

  page-header(
    [Weekly SMART Goal & Progress Log],
    [Set the Goal. Follow the Way. Reflect.],
    score: true,
  )
  daily-card([Monday])
  v(7pt)
  daily-card([Tuesday])
  v(7pt)
  daily-card([Wednesday])

  pagebreak()

  page-header(
    [Weekly SMART Goal & Progress Log],
    [Set the Goal. Follow the Way. Reflect.],
    score: true,
  )
  daily-card([Thursday])
  v(7pt)
  daily-card([Friday])
  v(7pt)
  weekly-review

  pagebreak()

  page-header(
    [Weekly SMART Goal & Progress Log],
    [Set the Goal. Follow the Way. Reflect.],
    score: true,
  )
  reflection-box(
    [Highlight of the Week],
    [Show your best moment, success, or something you are proud of. Use words, drawings, diagrams, or symbols.],
  )
  v(8pt)
  reflection-box(
    [What could have been better?],
    [Reflect on a challenge, a missed opportunity, or one thing you want to improve next time.],
  )

  pagebreak()

  page-header(
    [Warrior Work Ethic: Proof of My Learning Skills],
    [How have you demonstrated and improved?],
    score: false,
    title-size: 19.5pt,
  )
  text(size: 7.8pt, weight: "bold")[
    Circle one rating: E = Excellent, G = Good, S = Satisfactory, N = Needs Improvement
  ]
  v(6pt)

  skill-card(
    [Responsibility],
    [Getting things done without anyone reminding you. Not just submitting tasks - but showing you are in control of your life.],
  )
  v(5pt)
  skill-card(
    [Organization],
    [Keeping track of goals, tools & materials on your own. Using your planner/log so your life is not chaos in a backpack.],
  )
  v(5pt)
  skill-card(
    [Independent work],
    [Starting right away, staying focused, keeping goals. Figuring things out yourself before looking for help.],
  )
  v(5pt)
  skill-card(
    [Initiative],
    [Doing what needs to be done without being asked/assigned. Asking good questions and seeking ways to grow.],
  )
  v(5pt)
  skill-card(
    [Collaboration],
    [Being someone others actually want to work with. Helping others improve their weaknesses & learning from their strengths.],
  )
  v(5pt)
  skill-card(
    [Self-regulation],
    [No phones unless absolutely necessary - you stay in control, not distracted. Finding the middle path and maintaining balance.],
  )
}

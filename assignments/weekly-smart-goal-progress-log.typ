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
    margin: (top: 0.30in, bottom: 0.46in, x: 0.25in),
    footer: context [
      #set text(
        font: ("Arial", "Liberation Sans", "DejaVu Sans"),
        size: 6.5pt,
        fill: footer-ink,
        hyphenate: false,
      )
      #line(length: 100%, stroke: 0.65pt + primary)
      #v(3pt)
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
    size: 8.2pt,
    fill: black,
    hyphenate: false,
  )
  set par(leading: 0.48em, justify: false)

  let identity-fields(score: true) = [
    #grid(
      columns: (2.45in, 1.95in, 2.30in, auto),
      column-gutter: 11pt,
      align: horizon,
      [
        #text(weight: "bold")[Name:]
        #h(7pt)
        #line(length: 1.88in, stroke: 0.7pt + secondary)
      ],
      [
        #text(weight: "bold")[Course:]
        #h(7pt)
        #line(length: 1.35in, stroke: 0.7pt + secondary)
      ],
      [
        #text(weight: "bold")[Week of:]
        #h(7pt)
        #line(length: 1.42in, stroke: 0.7pt + secondary)
      ],
      [#if score [#text(size: 9pt, weight: "bold")[/20]]],
    )
  ]

  let page-header(title, subtitle, score: true, title-size: 21pt) = [
    #grid(
      columns: (1fr, 2.55in),
      column-gutter: 14pt,
      align: top,
      [
        #text(size: title-size, weight: "bold", fill: primary)[#title]
        #v(2pt)
        #text(size: 10.2pt, weight: "bold")[#subtitle]
        #v(5pt)
        #line(length: 0.72in, stroke: 3pt + accent)
      ],
      [
        #grid(
          columns: (0.55in, 1fr),
          column-gutter: 8pt,
          align: horizon,
          [#image("technology-department-emblem.svg", width: 0.50in)],
          [
            #text(size: 8.2pt, weight: "bold")[Technology Commons]
            #linebreak()
            #text(size: 7.5pt)[Port Credit Secondary School]
            #linebreak()
            #text(size: 7.4pt, weight: "bold")[May the Light Never Fail.]
          ],
        )
      ],
    )
    #v(4pt)
    #line(length: 100%, stroke: 1pt + secondary)
    #v(7pt)
    #identity-fields(score: score)
    #v(10pt)
  ]

  let two-write-lines() = [
    #v(6pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(9pt)
    #line(length: 100%, stroke: 0.6pt + black)
  ]

  let goal-lines = [
    #text(size: 7.4pt, weight: "bold")[Specific]
    #two-write-lines()
    #v(6pt)
    #text(size: 7.2pt, weight: "bold")[Measurable (by end of class, I will have)]
    #two-write-lines()
    #v(6pt)
    #text(size: 7.2pt, weight: "bold")[Attainable, Realistic, Timely]
    #two-write-lines()
  ]

  let progress-lines = [
    #text(size: 7.4pt, weight: "bold")[In detail, explain what you accomplished / learned today.]
    #v(8pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(10pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(10pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(10pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(10pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(10pt)
    #line(length: 100%, stroke: 0.6pt + black)
  ]

  let checkbox(size: 7.5pt) = box(
    width: size,
    height: size,
    stroke: 0.75pt + primary,
  )

  let evaluation-box = block(
    width: 100%,
    height: 1.72in,
    fill: eval-fill,
    stroke: 0.9pt + primary,
    radius: 5pt,
    inset: 7pt,
    [
      #text(size: 8.2pt, weight: "bold", fill: primary)[Teacher evaluation]
      #v(7pt)
      #grid(
        columns: (1fr, auto),
        row-gutter: 6pt,
        align: horizon,
        [#text(size: 7pt)[Neatly written]], [#checkbox()],
        [#text(size: 7pt)[Detailed information]], [#checkbox()],
        [#text(size: 7pt)[Technical terms]], [#checkbox()],
      )
      #v(8pt)
      #line(length: 100%, stroke: 0.5pt + primary)
      #v(6pt)
      #grid(
        columns: (auto, 1fr),
        column-gutter: 6pt,
        align: horizon,
        [#text(size: 7.2pt, weight: "bold")[Level]],
        [
          #text(size: 7pt)[1] #checkbox(size: 6.5pt)
          #h(4pt)
          #text(size: 7pt)[2] #checkbox(size: 6.5pt)
          #h(4pt)
          #text(size: 7pt)[3] #checkbox(size: 6.5pt)
          #h(4pt)
          #text(size: 7pt)[4] #checkbox(size: 6.5pt)
        ],
      )
    ]
  )

  let daily-card(day) = block(
    width: 100%,
    height: 2.43in,
    fill: white,
    stroke: 1pt + primary,
    radius: 6pt,
    inset: 0pt,
    clip: true,
    [
      #block(
        width: 100%,
        height: 0.38in,
        fill: header-fill,
        inset: (x: 9pt, y: 5pt),
        [
          #grid(
            columns: (1.10in, 1fr),
            column-gutter: 9pt,
            align: horizon,
            [#text(size: 13.5pt, weight: "bold", fill: primary)[#day]],
            [#text(size: 8pt, weight: "bold")[Set a SMART goal for today]],
          )
        ],
      )
      #pad(x: 9pt, top: 6pt)[
        #grid(
          columns: (2.52in, 1fr, 1.50in),
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
    height: 3.02in,
    fill: white,
    stroke: 1pt + primary,
    radius: 6pt,
    inset: 9pt,
    [
      #text(size: 13.5pt, weight: "bold", fill: primary)[Weekly Progress Check]
      #v(3pt)
      #line(length: 0.65in, stroke: 2.5pt + accent)
      #v(12pt)
      #text(size: 8pt, weight: "bold")[What progress did you make toward your goals this week?]
      #v(9pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(11pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(11pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(15pt)
      #text(size: 8pt, weight: "bold")[What is one specific next step for next week?]
      #v(9pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(11pt)
      #line(length: 100%, stroke: 0.6pt + black)
    ]
  )

  let reflection-box(title, prompt) = block(
    width: 100%,
    height: 3.68in,
    fill: white,
    stroke: 1pt + primary,
    radius: 6pt,
    inset: 0pt,
    clip: true,
    [
      #block(
        width: 100%,
        height: 0.38in,
        fill: header-fill,
        inset: (x: 9pt, y: 5pt),
        [#text(size: 13pt, weight: "bold", fill: primary)[#title]],
      )
      #pad(x: 9pt, top: 7pt)[
        #text(size: 7.8pt)[#prompt]
      ]
    ]
  )

  let rating-box = block(
    width: 100%,
    height: 0.90in,
    fill: eval-fill,
    stroke: 0.9pt + primary,
    radius: 5pt,
    inset: 8pt,
    [
      #text(size: 7.5pt, weight: "bold", fill: primary)[RATING]
      #v(16pt)
      #grid(
        columns: (auto, auto, auto, auto, auto, auto, auto, auto),
        column-gutter: 5pt,
        align: horizon,
        [#text(size: 8pt, weight: "bold")[E]], [#checkbox(size: 8pt)],
        [#text(size: 8pt, weight: "bold")[G]], [#checkbox(size: 8pt)],
        [#text(size: 8pt, weight: "bold")[S]], [#checkbox(size: 8pt)],
        [#text(size: 8pt, weight: "bold")[N]], [#checkbox(size: 8pt)],
      )
    ]
  )

  let skill-card(title, description) = block(
    width: 100%,
    height: 1.12in,
    fill: white,
    stroke: 0.9pt + primary,
    radius: 5pt,
    inset: 9pt,
    [
      #grid(
        columns: (1.90in, 1fr, 1.48in),
        column-gutter: 13pt,
        align: top,
        [
          #text(size: 10.5pt, weight: "bold", fill: primary)[#title]
          #v(9pt)
          #text(size: 6.8pt)[#description]
        ],
        [
          #text(size: 7.2pt, weight: "bold")[How have you demonstrated or improved this?]
          #v(11pt)
          #line(length: 100%, stroke: 0.6pt + black)
          #v(10pt)
          #line(length: 100%, stroke: 0.6pt + black)
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
    title-size: 18.5pt,
  )
  text(size: 7.8pt, weight: "bold")[
    Circle one rating: E = Excellent, G = Good, S = Satisfactory, N = Needs Improvement
  ]
  v(8pt)

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

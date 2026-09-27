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
    margin: (top: 0.30in, bottom: 0.46in, left: 0.75in, right: 0.25in),
    footer: context [
      #set text(
        font: "Source Sans 3",
        size: 6.5pt,
        fill: footer-ink,
        hyphenate: false,
      )
      #line(length: 100%, stroke: 0.65pt + primary)
      #v(3pt)
      #grid(
        columns: (1fr, auto),
        column-gutter: 12pt,
        [
          #text(weight: "bold")[Technology Commons - Weekly SMART Goal + Learning Skills]
          #linebreak()
          #text(size: 5.7pt)[CC BY-SA 4.0 · Modified versions remain CC BY-SA 4.0 · andrewandrade.ca + github.com/mrandrewandrade · Add your name/links · Sharing is caring]
        ],
        [Page #counter(page).display("1 of 1", both: true)]
      )
    ]
  )

  set text(
    font: "Source Sans 3",
    size: 8.2pt,
    fill: black,
    hyphenate: false,
  )
  set par(leading: 0.48em, justify: false)

  let checkbox(size: 7.5pt) = box(
    width: size,
    height: size,
    stroke: 0.75pt + primary,
  )

  let identity-fields(score: true) = [
    #grid(
      columns: (2.75in, 1.95in, 1.85in, auto),
      column-gutter: 11pt,
      align: horizon,
      [
        #text(weight: "bold")[Student Number:]
        #h(7pt)
        #line(length: 1.55in, stroke: 0.7pt + secondary)
      ],
      [
        #text(weight: "bold")[Course:]
        #h(7pt)
        #line(length: 1.35in, stroke: 0.7pt + secondary)
      ],
      [
        #text(weight: "bold")[Week \#: ]
        #h(7pt)
        #line(length: 0.92in, stroke: 0.7pt + secondary)
      ],
      [#if score [#text(size: 9pt, weight: "bold")[/20]]],
    )
  ]

  let weekly-quick-mark = block(
    width: 100%,
    height: 0.46in,
    fill: white,
    stroke: 0.8pt + primary,
    radius: 5pt,
    inset: (x: 8pt, y: 4pt),
    [
      #grid(
        columns: (1.12in, 1fr),
        column-gutter: 8pt,
        align: horizon,
        [#text(size: 7.3pt, weight: "bold", fill: primary)[Weekly quick mark]],
        [#text(size: 6.2pt)[C = clear / legible · D = detailed · T = technical terms · L = overall level]],
      )
      #v(2pt)
      #grid(
        columns: (1fr, 1fr, 1fr, 1fr, 1fr),
        column-gutter: 5pt,
        align: horizon,
        [
          #text(size: 6.3pt, weight: "bold")[Mon]
          #h(2pt) #text(size: 5.8pt)[C] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[D] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[T] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[L]
          #h(1pt) #line(length: 0.18in, stroke: 0.6pt + black)
        ],
        [
          #text(size: 6.3pt, weight: "bold")[Tue]
          #h(2pt) #text(size: 5.8pt)[C] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[D] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[T] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[L]
          #h(1pt) #line(length: 0.18in, stroke: 0.6pt + black)
        ],
        [
          #text(size: 6.3pt, weight: "bold")[Wed]
          #h(2pt) #text(size: 5.8pt)[C] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[D] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[T] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[L]
          #h(1pt) #line(length: 0.18in, stroke: 0.6pt + black)
        ],
        [
          #text(size: 6.3pt, weight: "bold")[Thu]
          #h(2pt) #text(size: 5.8pt)[C] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[D] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[T] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[L]
          #h(1pt) #line(length: 0.18in, stroke: 0.6pt + black)
        ],
        [
          #text(size: 6.3pt, weight: "bold")[Fri]
          #h(2pt) #text(size: 5.8pt)[C] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[D] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[T] #checkbox(size: 5.5pt)
          #h(1pt) #text(size: 5.8pt)[L]
          #h(1pt) #line(length: 0.18in, stroke: 0.6pt + black)
        ]
      )
    ]
  )

  let page-header(title, subtitle, score: true, title-size: 21pt, quick-mark: false) = [
    #grid(
      columns: (1fr, 2.55in),
      column-gutter: 14pt,
      align: top,
      [
        #text(size: title-size, weight: "bold", fill: primary)[#title]
        #v(2pt)
        #text(size: 10.2pt, weight: "bold")[#subtitle]
      ],
      [
        #grid(
          columns: (0.55in, 1fr),
          column-gutter: 8pt,
          align: horizon,
          [#image("technology-commons-header-logo.svg", width: 0.50in)],
          [
            #text(size: 8.2pt, weight: "bold")[Technology Commons]
            #linebreak()
            #text(size: 7.5pt)[Port Credit Secondary School]
            #linebreak()
            #text(size: 7.4pt, weight: "bold")[May The Light Never Be Lacking]
          ],
        )
      ],
    )
    #v(7pt)
    #identity-fields(score: score)
    #if quick-mark [
      #v(6pt)
      #weekly-quick-mark
    ]
    #v(8pt)
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
    #text(size: 8.2pt, weight: "bold", fill: primary)[Daily Progress]
    #v(2pt)
    #text(size: 6.9pt, weight: "bold")[What I did / learned]
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(8pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(8pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(6pt)
    #text(size: 6.9pt, weight: "bold")[What could have been better?]
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(8pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(6pt)
    #text(size: 6.9pt, weight: "bold")[What's next?]
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(8pt)
    #line(length: 100%, stroke: 0.6pt + black)
  ]

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
          columns: (2.48in, 1fr),
          column-gutter: 14pt,
          align: top,
          [#goal-lines],
          [#progress-lines],
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
      #v(9pt)
      #text(size: 7.8pt, weight: "bold")[What progress did you make toward your goals this week?]
      #v(7pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(9pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(10pt)
      #text(size: 7.8pt, weight: "bold")[What still needs attention, practice, or another try?]
      #v(7pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(9pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(10pt)
      #text(size: 7.8pt, weight: "bold")[What is one useful thing you can do over the weekend?]
      #v(3pt)
      #text(size: 6.8pt)[Catch up · practise · revise / improve · organize / prepare · explore / learn more]
      #v(7pt)
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
          #v(6pt)
          #text(size: 7.8pt)[#description]
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
    [Set the Goal. Follow the Way. Take Action.],
    score: true,
    quick-mark: true,
  )
  daily-card([Monday])
  v(7pt)
  daily-card([Tuesday])
  v(7pt)
  daily-card([Wednesday])

  pagebreak()

  page-header(
    [Weekly SMART Goal & Progress Log],
    [Set the Goal. Follow the Way. Take Action.],
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
    [Set the Goal. Follow the Way. Take Action.],
    score: true,
  )
  grid(
    columns: (1fr, 1fr),
    column-gutter: 8pt,
    row-gutter: 8pt,
    reflection-box(
      [Highlight of the Week],
      [Something you made, learned, solved, improved, or are proud of. Use words, drawings, diagrams, or symbols.],
    ),
    reflection-box(
      [Thankful + Credit],
      [Who or what are you thankful for this week? Give credit to a classmate, source, tool, example, or idea that helped you learn or make progress.],
    ),
    reflection-box(
      [What Helped Me Work Well?],
      [A routine, workspace choice, break, tool, teamwork habit, or way of working that helped you focus, stay safe, or feel balanced.],
    ),
    reflection-box(
      [Reset for Next Week],
      [One thing you will adjust to make your learning or work smoother, safer, or less stressful.],
    ),
  )

  pagebreak()

  page-header(
    [Warrior Work Ethic: Proof of My Learning Skills],
    [Set the Goal. Follow the Way. Take Action.],
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

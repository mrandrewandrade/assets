#let render(colour: true, feedback-qr: none) = {
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
    margin: (top: 0.18in, bottom: 0.46in, left: 0.75in, right: 0.25in),
    footer-descent: 0.18in,
    footer: context [
      #set text(
        font: "Source Sans 3",
        size: 6.5pt,
        fill: footer-ink,
        hyphenate: false,
      )
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
    #set text(size: 11pt)
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
      [#if score [#text(size: 11pt, weight: "bold")[/20]]],
    )
  ]

  let weekly-quick-mark = block(
    width: 100%,
    height: 0.75in,
    fill: white,
    stroke: 0.8pt + primary,
    radius: 5pt,
    inset: (x: 8pt, y: 4pt),
    [
      #text(size: 12pt, weight: "bold", fill: primary)[Expectations]
      #v(-6pt)
      #text(size: 10pt)[Make your work easy to see: write clearly, add useful details, and use the right technical words. If I cannot read it, the mark is 0. Use this sheet to plan your class time. I give you enough time in class, so I do not normally assign homework. Want to get more from the course? Practise, build, and keep learning outside class too. Be intentional - you can do more than you think.]
    ]
  )

  let page-header(title, subtitle, score: true, title-size: 21pt, quick-mark: false) = [
    #grid(
      columns: (4.65in, 1fr),
      column-gutter: 14pt,
      align: top,
      [
        #text(size: title-size, weight: "bold", fill: primary)[#title]
        #v(-12pt)
        #text(size: 11pt, weight: "bold")[#subtitle]
      ],
      [
        #grid(
          columns: (0.55in, 1fr),
          column-gutter: 8pt,
          align: horizon,
          [#image("tech-edu-resources.png", width: 0.50in)],
          [
            #text(size: 10pt, weight: "bold")[Technology Commons]
            #linebreak()
            #text(size: 10pt)[Port Credit Secondary School]
            #linebreak()
            #text(size: 10pt, weight: "bold")[May The Light Never Be Lacking]
          ],
        )
      ],
    )
    #v(-1pt)
    #identity-fields(score: score)
    #if quick-mark [
      #v(0pt)
      #weekly-quick-mark
    ]
    #v(1pt)
  ]

  // Every daily writing line uses the same measured vertical interval.
  let four-write-lines = [
    #line(length: 100%, stroke: 0.6pt + black)
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
  ]

  let three-write-lines = [
    #line(length: 100%, stroke: 0.6pt + black)
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
  ]

  let two-write-lines = [
    #line(length: 100%, stroke: 0.6pt + black)
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
  ]

  let left-top-write-lines = [
    #hide(line(length: 100%, stroke: 0.6pt + black))
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
  ]

  let offset-two-write-lines = [
    #hide(line(length: 100%, stroke: 0.6pt + black))
    #v(4pt)
    #line(length: 100%, stroke: 0.6pt + black)
  ]

  let standard-four-line-section(prompt) = [
    #block(height: 0.18in)[
      #text(size: 10pt, weight: "bold")[#prompt]
    ]
    #four-write-lines
  ]

  let standard-two-line-section(prompt) = [
    #block(height: 0.18in)[
      #text(size: 10pt, weight: "bold")[#prompt]
    ]
    #two-write-lines
  ]

  let goal-lines = [
    #standard-four-line-section([What will I do? Be specific.])
    #standard-two-line-section([Is it attainable, relevant, and timely?])
    #block(height: 0.18in)[
      #text(size: 10pt, weight: "bold")[Measurable: What is done by end of class?]
    ]
    #two-write-lines
  ]

  let progress-lines = [
    #standard-four-line-section([What I did / learned this period])
    #standard-two-line-section([What could have been better?])
    #block(height: 0.22in)[
      #text(size: 10pt, weight: "bold")[What's next?]
      #v(-7pt)
      #text(size: 10pt)[Finish, practice, or explore more after school if you choose.]
    ]
    #offset-two-write-lines
  ]

  let daily-card(day) = block(
    width: 100%,
    height: 2.66in,
    fill: white,
    stroke: 1pt + primary,
    radius: 6pt,
    inset: 0pt,
    clip: true,
    [
      #block(
        width: 100%,
        height: 0.36in,
        fill: header-fill,
        inset: (x: 9pt, y: 3pt),
        [
          #grid(
            columns: (2.48in, 1fr),
            column-gutter: 14pt,
            align: horizon,
            [
              #grid(
                columns: (0.98in, 1fr),
                column-gutter: 5pt,
                align: horizon,
                [#text(size: 13.5pt, weight: "bold", fill: primary)[#day]],
                [#text(size: 10pt, weight: "bold")[Set a SMART Goal]],
              )
            ],
            [#text(size: 13.5pt, weight: "bold", fill: primary)[Daily Progress]],
          )
        ],
      )
      #pad(x: 9pt, top: -6pt)[
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
    height: 3.35in,
    fill: white,
    stroke: 1pt + primary,
    radius: 6pt,
    inset: 9pt,
    [
      #text(size: 13.5pt, weight: "bold", fill: primary)[Weekly Progress Check]
      #v(4pt)
      #text(size: 10pt, weight: "bold")[What progress did you make toward your goals this week?]
      #v(3pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(4pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(4pt)
      #text(size: 10pt, weight: "bold")[What still needs attention, practice, or another try?]
      #v(3pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(4pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(4pt)
      #text(size: 10pt, weight: "bold")[How can you balance getting work done, being present, and taking care of yourself over the weekend?]
      #v(1pt)
      #text(size: 10pt)[Catch up · practice · prepare · rest · connect · be fully present]
      #v(2pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(2pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(2pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(2pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(2pt)
      #line(length: 100%, stroke: 0.6pt + black)
      #v(2pt)
      #line(length: 100%, stroke: 0.6pt + black)
    ]
  )

  let reflection-box(title, prompt) = block(
    width: 100%,
    height: 2.65in,
    fill: white,
    stroke: 1pt + primary,
    radius: 6pt,
    inset: 0pt,
    clip: true,
    [
      #block(
        width: 100%,
        height: 0.32in,
        fill: header-fill,
        inset: (x: 9pt, y: 4pt),
        [#text(size: 13pt, weight: "bold", fill: primary)[#title]],
      )
      #pad(x: 9pt, top: -12pt)[
        #text(size: 11pt)[#prompt]
      ]
    ]
  )

  let rating-box = block(
    width: 100%,
    height: 0.96in,
    inset: 0pt,
    [
      #text(size: 10pt, weight: "bold", fill: primary)[RATING]
      #v(2pt)
      #grid(
        columns: (auto, auto),
        column-gutter: 6pt,
        row-gutter: 1pt,
        align: horizon,
        [#text(size: 10pt, weight: "bold")[E]], [#checkbox(size: 10pt)],
        [#text(size: 10pt, weight: "bold")[G]], [#checkbox(size: 10pt)],
        [#text(size: 10pt, weight: "bold")[S]], [#checkbox(size: 10pt)],
        [#text(size: 10pt, weight: "bold")[N]], [#checkbox(size: 10pt)],
      )
    ]
  )

  let skill-card(title, description) = block(
    width: 100%,
    height: 1.22in,
    fill: white,
    stroke: 0.9pt + primary,
    radius: 5pt,
    inset: 9pt,
    [
      #grid(
        columns: (2.15in, 1fr, 0.70in),
        column-gutter: 10pt,
        align: top,
        [
          #text(size: 10.5pt, weight: "bold", fill: primary)[#title]
          #v(6pt)
          #text(size: 10.5pt)[#description]
        ],
        [
          #text(size: 10pt, weight: "bold")[How have you demonstrated or improved this?]
          #v(5pt)
          #line(length: 100%, stroke: 0.6pt + black)
          #v(4pt)
          #line(length: 100%, stroke: 0.6pt + black)
          #v(4pt)
          #line(length: 100%, stroke: 0.6pt + black)
          #v(4pt)
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
  v(1pt)
  daily-card([Tuesday])
  v(1pt)
  daily-card([Wednesday])

  pagebreak()

  page-header(
    [Weekly SMART Goal & Progress Log],
    [Set the Goal. Follow the Way. Take Action.],
    score: true,
  )
  daily-card([Thursday])
  v(1pt)
  daily-card([Friday])
  v(1pt)
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
  v(8pt)
  if feedback-qr == none [
    #block(
      width: 100%,
      height: 2.85in,
      fill: white,
      stroke: 1pt + primary,
      radius: 6pt,
      inset: 9pt,
      [#text(size: 11pt, weight: "bold")[Something fun I want to do this weekend]],
    )
  ] else [
    #grid(
      columns: (1fr, 1fr),
      column-gutter: 8pt,
      block(
        width: 100%,
        height: 2.85in,
        fill: white,
        stroke: 1pt + primary,
        radius: 6pt,
        inset: 9pt,
        [#text(size: 11pt, weight: "bold")[Something fun I want to do this weekend]],
      ),
      block(
        width: 100%,
        height: 2.85in,
        fill: white,
        stroke: 1pt + primary,
        radius: 6pt,
        inset: 9pt,
        [
          #align(center)[
            #text(size: 11pt, weight: "bold", fill: primary)[Anonymous Feedback Survey]
            #v(2pt)
            #text(size: 9pt)[Scan to share honest, anonymous feedback about the class.]
            #v(5pt)
            #image(feedback-qr, width: 1.72in)
          ]
        ],
      ),
    )
  ]

  pagebreak()

  page-header(
    [Warrior Work Ethic: Learning Skills Proof],
    [Set the Goal. Follow the Way. Take Action.],
    score: false,
    title-size: 18.5pt,
  )
  text(size: 10pt, weight: "bold")[
    Circle one rating: E = Excellent, G = Good, S = Satisfactory, N = Needs Improvement
  ]
  v(2pt)
  text(size: 10pt)[
    Rate the evidence honestly. Giving yourself all Es without earning them will lose you marks. For example, if the class is asked to participate and you do not, Initiative and Collaboration should be N, not E.
  ]
  v(5pt)

  skill-card(
    [Responsibility],
    [Getting things done without anyone reminding you. Not just submitting tasks - but showing you are in control of your life.],
  )
  v(1pt)
  skill-card(
    [Organization],
    [Keeping track of goals, tools & materials on your own. Using your planner/log so your life is not chaos in a backpack.],
  )
  v(1pt)
  skill-card(
    [Independent work],
    [Starting right away, staying focused, keeping goals. Figuring things out yourself before looking for help.],
  )
  v(1pt)
  skill-card(
    [Initiative],
    [Doing what needs to be done without being asked/assigned. Asking good questions and seeking ways to grow.],
  )
  v(1pt)
  skill-card(
    [Collaboration],
    [Being someone others actually want to work with. Helping others improve their weaknesses & learning from their strengths.],
  )
  v(1pt)
  skill-card(
    [Self-regulation],
    [No phones unless absolutely necessary - you stay in control, not distracted. Finding the middle path and maintaining balance.],
  )
}

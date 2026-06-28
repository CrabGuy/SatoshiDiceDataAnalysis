// Rosé Pine Dawn theme for Quarto Typst PDF

#let rpdBase = rgb("#FAF4ED")
#let rpdSurface = rgb("#FFFAF3")
#let rpdOverlay = rgb("#F2E9E1")
#let rpdMuted = rgb("#9893A5")
#let rpdSubtle = rgb("#797593")
#let rpdText = rgb("#575279")
#let rpdLove = rgb("#B4637A")
#let rpdGold = rgb("#EA9D34")
#let rpdRose = rgb("#D7827E")
#let rpdPine = rgb("#286983")
#let rpdFoam = rgb("#56949F")
#let rpdIris = rgb("#907AA9")

#set page(
  fill: rpdBase,
  margin: (top: 1in, bottom: 1in, x: 1in),
)
#set text(fill: rpdText, font: "Inter", size: 11pt)

// Headings in rose accent
#show heading: set text(fill: rpdRose)

// Links in rose
#show link: set text(fill: rpdRose)

// Code blocks: rounded, soft overlay background, no overflow
#show raw.where(block: true): it => block(
  fill: rpdOverlay,
  inset: 10pt,
  radius: 4pt,
  width: 100%,
  it
)

// Inline code: subtle background, no harsh box
#show raw.where(block: false): it => box(
  fill: rpdOverlay,
  outset: (y: 2pt),
  inset: (x: 3pt),
  radius: 2pt,
  it
)

// Avoid orphan/widow lines
#set par(justify: true)
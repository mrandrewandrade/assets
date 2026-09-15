# Brand fonts

Unmodified Source Sans 3 and Source Code Pro fonts from the established
`mrandrewandrade/commons` brand kit (`site/assets/fonts/`). Both families
are distributed under the SIL Open Font License 1.1; see `OFL-1.1.txt`.

Source Sans 3 is the document body and heading family. Source Code Pro is
the code family. Static Regular and SemiBold Source Sans 3 faces avoid
variable-font limitations in Typst. Quarto reads this directory through
`assignments/_metadata.yml`, and
`render.sh` also sets `TYPST_FONT_PATHS` for direct Typst invocations.

Upstream: https://github.com/adobe-fonts/source-sans and
https://github.com/adobe-fonts/source-code-pro.

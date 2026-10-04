$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
New-Item -ItemType Directory -Force -Path (Join-Path $repoRoot 'dist') | Out-Null

$magick = Get-Command magick -ErrorAction SilentlyContinue
if (-not $magick) { throw 'ImageMagick is required to create print-ready schematic PDFs.' }
$pdflatex = Get-Command pdflatex -ErrorAction SilentlyContinue
if (-not $pdflatex) { throw 'pdfLaTeX is required to generate CircuitikZ schematics.' }
$dvisvgm = Get-Command dvisvgm -ErrorAction SilentlyContinue
if (-not $dvisvgm) { throw 'dvisvgm is required to generate vector SVG schematics.' }
$quarto = Get-Command quarto.exe -ErrorAction SilentlyContinue
if (-not $quarto) { $quarto = Get-Command quarto -ErrorAction SilentlyContinue }
if (-not $quarto) { throw 'Quarto is required to render the electronics assets.' }

$schematicBuild = Join-Path $repoRoot 'tmp/schematics'
New-Item -ItemType Directory -Force -Path $schematicBuild | Out-Null

Get-ChildItem -LiteralPath 'electronics/schematics' -Filter '*.tex' | ForEach-Object {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
    & $pdflatex.Source '-interaction=nonstopmode' '-halt-on-error' "-output-directory=$schematicBuild" $_.FullName | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "CircuitikZ PDF generation failed for $($_.FullName)" }
    $generatedPdf = Join-Path $schematicBuild "$baseName.pdf"
    $pdfPath = Join-Path $_.DirectoryName "$baseName.pdf"
    $svgPath = Join-Path $_.DirectoryName "$baseName.svg"
    Copy-Item -LiteralPath $generatedPdf -Destination $pdfPath -Force
    & $dvisvgm.Source '--pdf' '--no-fonts' '--exact-bbox' '--bbox=min' "--output=$svgPath" $generatedPdf
    if ($LASTEXITCODE -ne 0) { throw "CircuitikZ SVG generation failed for $($_.FullName)" }
}

Get-ChildItem -LiteralPath 'electronics/schematics' -Filter '*.svg' | ForEach-Object {
    $texPath = [System.IO.Path]::ChangeExtension($_.FullName, '.tex')
    if (Test-Path -LiteralPath $texPath) { return }
    $pdfPath = [System.IO.Path]::ChangeExtension($_.FullName, '.pdf')
    & $magick.Source -density 144 $_.FullName -background white -alpha remove -alpha off -compress Zip $pdfPath
    if ($LASTEXITCODE -ne 0) { throw "Schematic conversion failed for $($_.FullName)" }
}

function Render-Pdf {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Output
    )

    & $quarto.Source render $Source --to pdf --output $Output
    if ($LASTEXITCODE -ne 0) { throw "Quarto PDF render failed for $Source" }
    Move-Item -LiteralPath $Output -Destination (Join-Path 'dist' $Output) -Force
}

Render-Pdf 'electronics/reference/TEJ-Electronics-Quick-Reference.qmd' 'TEJ-Electronics-Quick-Reference.pdf'
Render-Pdf 'electronics/reference/TEJ-Electronics-Reference-Handbook.qmd' 'TEJ-Electronics-Reference-Handbook.pdf'
Push-Location -LiteralPath 'electronics/reference'
try {
    & $quarto.Source render 'TEJ-Electronics-Reference-Handbook.qmd' --to html --output 'TEJ-Electronics-Reference-Handbook.html'
    if ($LASTEXITCODE -ne 0) { throw 'Quarto HTML render failed for the reference handbook' }
}
finally {
    Pop-Location
}
Move-Item -LiteralPath 'electronics/reference/TEJ-Electronics-Reference-Handbook.html' -Destination 'dist/TEJ-Electronics-Reference-Handbook.html' -Force

Render-Pdf 'electronics/worksheets/TEJ-Basic-Circuit-Calculations-Student-Worksheet.qmd' 'TEJ_Basic_Circuit_Calculations_Student_Worksheet.pdf'
Render-Pdf 'electronics/worksheets/TEJ-Basic-Circuit-Calculations-Answer-Key.qmd' 'TEJ_Basic_Circuit_Calculations_Answer_Key.pdf'

$moduleDir = 'electronics/modules/H01-safety-lab-practice'
Render-Pdf "$moduleDir/H01_Safety_Lab_Practice_Student_Worksheet.qmd" 'H01_Safety_Lab_Practice_Student_Worksheet.pdf'
Render-Pdf "$moduleDir/H01_Safety_Lab_Practice_Answer_Key.qmd" 'H01_Safety_Lab_Practice_Answer_Key.pdf'
Render-Pdf "$moduleDir/H01_Safety_Lab_Practice_Lab.qmd" 'H01_Safety_Lab_Practice_Lab.pdf'
Render-Pdf "$moduleDir/H01_Safety_Lab_Practice_Tinkercad_Guide.qmd" 'H01_Safety_Lab_Practice_Tinkercad_Guide.pdf'

$digitalDir = 'electronics/modules/D01-digital-inputs'
Render-Pdf "$digitalDir/D01_Digital_Inputs_Student_Worksheet.qmd" 'D01_Digital_Inputs_Student_Worksheet.pdf'
Render-Pdf "$digitalDir/D01_Digital_Inputs_Answer_Key.qmd" 'D01_Digital_Inputs_Answer_Key.pdf'

$controlDir = 'electronics/modules/C06-control-systems'
Render-Pdf "$controlDir/C06_Control_Methods_Comparison_Student.qmd" 'C06_Control_Methods_Comparison_Student.pdf'
Render-Pdf "$controlDir/C06_Control_Methods_Comparison_Answer_Key.qmd" 'C06_Control_Methods_Comparison_Answer_Key.pdf'

$computerSystemsDir = 'electronics/computer-systems'
Render-Pdf "$computerSystemsDir/TEJ-Basic-Computer-Systems-Student-Activity-Packages.qmd" 'TEJ-Basic-Computer-Systems-Student-Activity-Packages.pdf'
Render-Pdf "$computerSystemsDir/TEJ-Basic-Computer-Systems-Teacher-Guide.qmd" 'TEJ-Basic-Computer-Systems-Teacher-Guide.pdf'

Get-ChildItem -LiteralPath 'electronics/schematics' -File |
    Where-Object { $_.Extension -in @('.svg', '.pdf') } |
    ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path 'dist' $_.Name) -Force
    }

Write-Host 'Rendered TEJ electronics assets to dist/.'

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot
New-Item -ItemType Directory -Force -Path (Join-Path $repoRoot 'dist') | Out-Null

$magick = Get-Command magick -ErrorAction SilentlyContinue
if (-not $magick) { throw 'ImageMagick is required to create print-ready schematic PDFs.' }

Get-ChildItem -LiteralPath 'electronics/schematics' -Filter '*.svg' | ForEach-Object {
    $pdfPath = [System.IO.Path]::ChangeExtension($_.FullName, '.pdf')
    & $magick.Source -background white -density 144 $_.FullName $pdfPath
    if ($LASTEXITCODE -ne 0) { throw "Schematic conversion failed for $($_.FullName)" }
}

function Render-Pdf {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Output
    )

    quarto render $Source --to pdf --output $Output
    if ($LASTEXITCODE -ne 0) { throw "Quarto PDF render failed for $Source" }
    Move-Item -LiteralPath $Output -Destination (Join-Path 'dist' $Output) -Force
}

Render-Pdf 'electronics/reference/TEJ-Electronics-Formula-Reference.qmd' 'TEJ-Electronics-Formula-Reference.pdf'
Push-Location -LiteralPath 'electronics/reference'
try {
    quarto render 'TEJ-Electronics-Formula-Reference.qmd' --to html --output 'TEJ-Electronics-Formula-Reference.html'
    if ($LASTEXITCODE -ne 0) { throw 'Quarto HTML render failed for the formula reference' }
}
finally {
    Pop-Location
}
Move-Item -LiteralPath 'electronics/reference/TEJ-Electronics-Formula-Reference.html' -Destination 'dist/TEJ-Electronics-Formula-Reference.html' -Force

Render-Pdf 'electronics/worksheets/TEJ-Basic-Circuit-Calculations-Student-Worksheet.qmd' 'TEJ_Basic_Circuit_Calculations_Student_Worksheet.pdf'
Render-Pdf 'electronics/worksheets/TEJ-Basic-Circuit-Calculations-Answer-Key.qmd' 'TEJ_Basic_Circuit_Calculations_Answer_Key.pdf'

$moduleDir = 'electronics/modules/H01-safety-lab-practice'
Render-Pdf "$moduleDir/H01_Safety_Lab_Practice_Student_Worksheet.qmd" 'H01_Safety_Lab_Practice_Student_Worksheet.pdf'
Render-Pdf "$moduleDir/H01_Safety_Lab_Practice_Answer_Key.qmd" 'H01_Safety_Lab_Practice_Answer_Key.pdf'
Render-Pdf "$moduleDir/H01_Safety_Lab_Practice_Lab.qmd" 'H01_Safety_Lab_Practice_Lab.pdf'
Render-Pdf "$moduleDir/H01_Safety_Lab_Practice_Tinkercad_Guide.qmd" 'H01_Safety_Lab_Practice_Tinkercad_Guide.pdf'

Copy-Item -LiteralPath 'electronics/schematics/H01_Safety_Lab_Practice_Schematic.svg' -Destination 'dist/H01_Safety_Lab_Practice_Schematic.svg' -Force
Copy-Item -LiteralPath 'electronics/schematics/H01_Blade_Fuse_Cutaway.svg' -Destination 'dist/H01_Blade_Fuse_Cutaway.svg' -Force
Copy-Item -LiteralPath 'electronics/schematics/Circuit_Calculations_Parallel_Schematic.svg' -Destination 'dist/Circuit_Calculations_Parallel_Schematic.svg' -Force
Copy-Item -LiteralPath 'electronics/schematics/H01_Safety_Lab_Practice_Schematic.pdf' -Destination 'dist/H01_Safety_Lab_Practice_Schematic.pdf' -Force
Copy-Item -LiteralPath 'electronics/schematics/H01_Blade_Fuse_Cutaway.pdf' -Destination 'dist/H01_Blade_Fuse_Cutaway.pdf' -Force
Copy-Item -LiteralPath 'electronics/schematics/Circuit_Calculations_Parallel_Schematic.pdf' -Destination 'dist/Circuit_Calculations_Parallel_Schematic.pdf' -Force

Write-Host 'Rendered TEJ electronics assets to dist/.'

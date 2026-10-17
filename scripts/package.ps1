param([string]$OutputDirectory, [switch]$Force)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not $OutputDirectory) {
  $OutputDirectory = Split-Path -Parent (Split-Path -Parent $projectRoot)
}
$manifest = Get-Content -LiteralPath (Join-Path $projectRoot 'manifest.json') -Raw | ConvertFrom-Json
$slug = 'winter-whisper-theme'
$zipPath = Join-Path $OutputDirectory "$slug-$($manifest.version).zip"
if ((Test-Path -LiteralPath $zipPath) -and -not $Force) { throw "Archive already exists: $zipPath" }
$relative = @('manifest.json','logo','README.md','scripts','store-assets','LICENSE','.gitignore')
$items = $relative | ForEach-Object { Join-Path $projectRoot $_ }
Add-Type -AssemblyName System.IO.Compression.FileSystem
Compress-Archive -LiteralPath $items -DestinationPath $zipPath -Force
$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
  $names = @($zip.Entries | ForEach-Object { $_.FullName -replace '\\', '/' })
  if ($names -notcontains 'manifest.json') { throw 'Manifest must sit at the ZIP root' }
  if ($names | Where-Object { $_ -match '(^|/)(\.git|\.codebuddy|__pycache__)/|\.(pak|zip|pyc)$' }) { throw 'Unwanted files in archive' }
  $entry = $zip.Entries | Where-Object { $_.FullName -eq 'manifest.json' }
  $reader = New-Object System.IO.StreamReader($entry.Open())
  try { $inside = $reader.ReadToEnd() | ConvertFrom-Json } finally { $reader.Dispose() }
  if ($inside.name -ne $manifest.name -or $inside.version -ne $manifest.version) { throw 'Manifest mismatch' }
  foreach ($ref in $inside.icons.PSObject.Properties.Value) {
    if ($names -notcontains $ref) { throw "Missing manifest reference: $ref" }
  }
} finally { $zip.Dispose() }
Get-Item -LiteralPath $zipPath | Select-Object FullName,Length



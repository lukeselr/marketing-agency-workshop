# marketing-agency-workshop installer (Windows).
# Module 3 of the Selr AI Workshop. Copies the marketing-agency skill into
# %USERPROFILE%\.claude\skills\ and runs its internal installer.

$ErrorActionPreference = "Stop"

$SRC = $PSScriptRoot
$SkillSrc = Join-Path $SRC "skill"
$SkillDst = Join-Path $HOME ".claude\skills\marketing-agency"

if (-not (Test-Path $SkillSrc)) {
  Write-Error "[fail] expected skill source at $SkillSrc"
  exit 1
}

Write-Host "==> Installing marketing-agency skill to $SkillDst"
New-Item -ItemType Directory -Force -Path (Split-Path $SkillDst -Parent) | Out-Null

if (Test-Path $SkillDst) {
  Remove-Item -Recurse -Force $SkillDst
}
Copy-Item -Recurse -Path $SkillSrc -Destination $SkillDst

Write-Host "==> Running skill installer"
$Installer = Join-Path $SkillDst "install.ps1"
if (Test-Path $Installer) {
  & pwsh -File $Installer
} else {
  & bash (Join-Path $SkillDst "install.sh")
}

Write-Host ""
Write-Host "Module 3 install complete."
Write-Host ""
Write-Host "Next: in Claude Code, type"
Write-Host "  /marketing-agency"
Write-Host "and paste your business website URL when asked."

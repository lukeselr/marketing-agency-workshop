$Repo = if ($env:MA_REPO) { $env:MA_REPO } else { "lukeselr/marketing-agency-workshop" }
$Tmp = New-Item -ItemType Directory -Path "$env:TEMP\ma-update-$(Get-Random)" -Force
Set-Location $Tmp
git clone "https://github.com/$Repo" .
if (Test-Path "install.ps1") {
  pwsh "install.ps1"
} elseif (Test-Path "skills/marketing-agency") {
  pwsh "skills/marketing-agency/install.ps1"
} elseif (Test-Path "marketing-agency") {
  pwsh "marketing-agency/install.ps1"
}
Remove-Item -Recurse -Force $Tmp

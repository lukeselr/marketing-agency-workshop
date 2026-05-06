# marketing-agency installer (Windows PowerShell).
# Usage:  pwsh install.ps1
$ErrorActionPreference = "Stop"
$SkillDir = "$env:USERPROFILE\.claude\skills\marketing-agency"
$Src = (Get-Item -Path $PSScriptRoot).FullName

Write-Host "Installing marketing-agency to $SkillDir"
New-Item -ItemType Directory -Path $SkillDir -Force | Out-Null
robocopy $Src $SkillDir /MIR /XD .state dist __pycache__ node_modules /XF .env | Out-Null

$Tokens = "$env:USERPROFILE\.marketing-agency\tokens"
New-Item -ItemType Directory -Path $Tokens -Force | Out-Null

Write-Host "Installed. Next: open Claude Code and say:"
Write-Host "  > Run the marketing-agency skill against my business at <URL>"

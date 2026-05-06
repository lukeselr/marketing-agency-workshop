$SkillDir = "$env:USERPROFILE\.claude\skills\marketing-agency"
$confirm = Read-Host "Remove $SkillDir? [y/N]"
if ($confirm -eq "y") {
  Remove-Item -Recurse -Force $SkillDir
  Write-Host "Removed. Tokens preserved at ~/.marketing-agency/tokens/."
}

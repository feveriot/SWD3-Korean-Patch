$ErrorActionPreference='Stop'
$g=$args[0]; $p=Join-Path $g 'Mods\modlist.txt'
if(Test-Path $p){$t=[IO.File]::ReadAllText($p);foreach($m in @('swd3_ko.ssmod','swd3_ko_qol.ssmod')){$t=[regex]::Replace($t,"(?m)^-?\d+\s+$([regex]::Escape($m))\r?\n?",'')};[IO.File]::WriteAllText($p,$t,(New-Object System.Text.UTF8Encoding($true)))}

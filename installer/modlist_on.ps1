$ErrorActionPreference='Stop'
$g=$args[0]; $p=Join-Path $g 'Mods\modlist.txt'
$utf8=New-Object System.Text.UTF8Encoding($true)
if(Test-Path $p){$t=[IO.File]::ReadAllText($p)}else{$t=[IO.File]::ReadAllText((Join-Path $g 'KoreanPatch\files\modlist_header.txt'))}
foreach($m in @('swd3_ko.ssmod','swd3_ko_qol.ssmod')){
  $e=[regex]::Escape($m)
  if($t -match "(?m)^-?\d+\s+$e\s*$"){$t=[regex]::Replace($t,"(?m)^-?\d+(\s+$e)",'1$1')}else{if(-not $t.EndsWith("`n")){$t+="`r`n"};$t+="1 $m`r`n"}
}
[IO.File]::WriteAllText($p,$t,$utf8)

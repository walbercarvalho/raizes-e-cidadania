# Instala as skills do raizes-e-cidadania no Windows.
# Uso (PowerShell, dentro da pasta do repositório):
#   .\install.ps1                  instala para Claude Code, Codex e Antigravity
#   .\install.ps1 -Destino Claude  só para uma ferramenta (Claude, Codex, Antigravity)
param(
    [ValidateSet("Todos", "Claude", "Codex", "Antigravity")]
    [string]$Destino = "Todos"
)

$ErrorActionPreference = "Stop"
$origem = Join-Path $PSScriptRoot "skills"
$alvos = @{
    "Claude"      = Join-Path $HOME ".claude\skills"
    "Codex"       = Join-Path $HOME ".agents\skills"
    "Antigravity" = Join-Path $HOME ".gemini\antigravity\skills"
}
$escolhidos = if ($Destino -eq "Todos") { $alvos.Keys } else { @($Destino) }

foreach ($nome in $escolhidos) {
    $pasta = $alvos[$nome]
    New-Item -ItemType Directory -Force -Path $pasta | Out-Null
    foreach ($skill in Get-ChildItem -Directory $origem) {
        $dest = Join-Path $pasta $skill.Name
        if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
        Copy-Item -Recurse $skill.FullName $dest
    }
    Write-Host "$nome : skills instaladas em $pasta"
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "Aviso: Python não encontrado. A árvore em HTML precisa dele."
    Write-Host "Instale com: winget install Python.Python.3.12"
}
Write-Host ""
Write-Host "Pronto. Abra uma pasta nova no Claude Code, Codex ou Antigravity e diga: quero montar a árvore da minha família."

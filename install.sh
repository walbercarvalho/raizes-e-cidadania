#!/usr/bin/env sh
# Instala as skills do raizes-e-cidadania no macOS ou Linux.
# Uso: sh install.sh [todos|claude|codex|antigravity]
set -e
destino="${1:-todos}"
origem="$(cd "$(dirname "$0")" && pwd)/skills"

instalar() {
  pasta="$1"
  mkdir -p "$pasta"
  for skill in "$origem"/*/; do
    nome="$(basename "$skill")"
    rm -rf "$pasta/$nome"
    cp -R "$skill" "$pasta/$nome"
  done
  echo "skills instaladas em $pasta"
}

case "$destino" in
  todos)
    instalar "$HOME/.claude/skills"
    instalar "$HOME/.agents/skills"
    instalar "$HOME/.gemini/antigravity/skills" ;;
  claude) instalar "$HOME/.claude/skills" ;;
  codex) instalar "$HOME/.agents/skills" ;;
  antigravity) instalar "$HOME/.gemini/antigravity/skills" ;;
  *) echo "uso: sh install.sh [todos|claude|codex|antigravity]"; exit 1 ;;
esac

command -v python3 >/dev/null 2>&1 || echo "Aviso: python3 não encontrado. A árvore em HTML precisa dele."
echo "Pronto. Abra uma pasta nova no Claude Code, Codex ou Antigravity e diga: quero montar a árvore da minha família."

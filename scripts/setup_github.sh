#!/usr/bin/env bash
# Configura repo remoto, variables de Actions y primer push a GitHub Pages.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export PATH="${HOME}/.local/bin:${PATH}"

if ! command -v gh >/dev/null 2>&1; then
  echo "Instalá GitHub CLI: https://cli.github.com/"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Ejecutá primero: gh auth login"
  exit 1
fi

USER="$(gh api user -q .login)"
REPO="jugar-argentina"

echo "→ Creando repo ${USER}/${REPO} (si no existe)..."
gh repo create "${REPO}" --public --source=. --remote=origin --push 2>/dev/null || {
  git remote remove origin 2>/dev/null || true
  git remote add origin "git@github.com:${USER}/${REPO}.git"
  git push -u origin main
}

echo "→ Variables de Actions..."
gh variable set PUBLIC_SITE_URL --body "https://${USER}.github.io" --repo "${USER}/${REPO}"
gh variable set PUBLIC_BASE_PATH --body "/jugar-argentina/" --repo "${USER}/${REPO}"

echo "→ Habilitá Pages con source GitHub Actions en:"
echo "   https://github.com/${USER}/${REPO}/settings/pages"
echo ""
echo "→ Producción: https://${USER}.github.io/jugar-argentina/"
echo "→ Workflow: https://github.com/${USER}/${REPO}/actions"

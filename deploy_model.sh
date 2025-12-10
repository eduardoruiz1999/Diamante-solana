#!/usr/bin/env bash
# scripts/deploy_model.sh - Despliegue seguro con verificación

set -euo pipefail

HF_TOKEN="${1:-${HF_TOKEN-}}"
GH_TOKEN="${2:-${GH_TOKEN-}}"

if [ -z "$HF_TOKEN" ] || [ -z "$GH_TOKEN" ]; then
  echo "❌ ERROR: Faltan tokens de autenticación"
  echo "Uso: ./scripts/deploy_model.sh HF_TOKEN GH_TOKEN"
  exit 1
fi

echo "🚀 INICIANDO DESPLIEGUE SEGURO DE DIAMANTE-SOLANA"

echo "🔍 Analizando seguridad del código..."
# (opcional) ejecutar checks estáticos si existen
if command -v python >/dev/null 2>&1; then
  if [ -f "scripts/security_check.py" ]; then
    python scripts/security_check.py || true
  fi
fi

echo "🔑 Verificando que no haya claves embebidas en código..."
if grep -R --line-number -E "(private_key|SECRET|PASSWORD|api_key|token)" . --exclude-dir=.git | grep -vE "\.env" | grep -v "node_modules"; then
  echo "⚠️  ADVERTENCIA: Posibles credenciales en el código fuente. Abortando."
  exit 1
fi

# Empujar modelo a Hugging Face (ejemplo)
echo "🤖 Desplegando modelos de IA (si existen en ./models/optimized)..."
python - <<PY
from huggingface_hub import HfApi, Repository
import os
api = HfApi()
api.set_access_token(os.getenv('HF_TOKEN') or '${HF_TOKEN}')
repo_id = 'diamante-solana/optimized-model'
folder = './models/optimized'
if os.path.isdir(folder):
    print('Subiendo carpeta', folder)
    api.upload_folder(folder_path=folder, repo_id=repo_id, repo_type='model')
else:
    print('No se encontró carpeta ./models/optimized — saltando subida')
PY

# Configurar webhook de monitoreo (ejemplo)
echo "📊 Configurando monitoreo de precio (webhook de ejemplo)..."
WEBHOOK_URL="${WEBHOOK_URL:-https://api.diamante-solana.com/webhooks/price-alert}"
curl -s -X POST "$WEBHOOK_URL" \
  -H "Authorization: Bearer ${GH_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"token_address":"5zJo2GzYRgiZw5j3SBNpuqVcGok35kT3ADwsw74yJWV6","target_price":6,"actions":["buy","sell","hold"]}' || true

# Iniciar bots (si existen)
if [ -f "bots/trading_bot.py" ]; then
  echo "💸 Iniciando bots de trading (ejecución en background)..."
  python bots/trading_bot.py --token DMT --aggressive --max-investment 10 &
else
  echo "No se encontró bots/trading_bot.py — saltando inicio de bots"
fi

echo "✅ DESPLIEGUE (proceso) COMPLETADO"

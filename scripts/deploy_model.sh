#!/bin/bash

# Script para desplegar modelo en Hugging Face Spaces y GitHub

echo "🚀 Desplegando Diamante Megatron..."

# Variables (configurar en GitHub Secrets)
HF_TOKEN=$1
GH_TOKEN=$2
DMT_ADDRESS="5zJo2GzYRgiZw5j3SBNpuqVcGok35kT3ADwsw74yJWV6"

# 1. Subir a Hugging Face
echo "Subiendo a Hugging Face Spaces..."
cd model_repository
huggingface-cli upload joseififif/Megatron-Solana ./diamante_llm \
    "Modelo Diamante LLM con integración Solana" \
    --token $HF_TOKEN \
    --repo-type=space

# 2. Configurar Triton en Spaces
echo "Configurando Triton Inference Server..."
curl -X POST "https://huggingface.co/api/spaces/joseififif/Megatron-Solana/settings" \
    -H "Authorization: Bearer $HF_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "sdk": "docker",
        "hardware": {"cpu": 4, "memory": "16Gi"},
        "env": {
            "MODEL_NAME": "diamante_llm",
            "TRITON_PORT": "8000",
            "DMT_TOKEN_ADDRESS": "'"$DMT_ADDRESS"'"
        }
    }'

# 3. Desplegar web en GitHub Pages
echo "Desplegando página web..."
cd ../src/web
npm run build
cp -r dist/* ../../docs/
cd ../..

git config --global user.email "jefetoken9@gmail.com"
git config --global user.name "Diamante Deploy Bot"
git add .
git commit -m "Deploy: $(date)"
git push "https://$GH_TOKEN@github.com/tu-usuario/diamante-megatron.git"

echo "✅ Despliegue completado!"
echo "🌐 Hugging Face Space: https://huggingface.co/spaces/joseififif/Megatron-Solana"
echo "🌐 GitHub Pages: https://tu-usuario.github.io/diamante-megatron"

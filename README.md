# Diamante-solana

git  clone https://github.com/eduardoruiz1999/Diamante-solana

# .env file 
WALLET_PRIVATE_KEY=tu_nueva_llave_privada
DMT_TOKEN_ADDRESS=5zJo2GzYRgiZw5j3SBNpuqVcGok35kT3ADwsw74yJWV6
HF_TOKEN=hf_tu_token_aqui
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

from adapters import AutoAdapterModel

model = AutoAdapterModel.from_pretrained("undefined")
model.load_adapter("DeepDemon/MegaSol", set_active=True)

git clone https://huggingface.co/spaces/joseififif/Megatron-keras

git clone https://huggingface.co/spaces/joseififif/Megatron-So


# despliegue seguro
chmod +x scripts/deploy_model.sh
./scripts/deploy_model.sh $HF_TOKEN $GH_TOKEN

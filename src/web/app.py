import gradio as gr
import os
from src.inference.triton_client import DiamanteTritonClient
from src.solana_integration.token_utils import DMTTokenManager

# Inicializar cliente
triton_client = DiamanteTritonClient()
token_manager = DMTTokenManager()

def generate_ui():
    """Interfaz de usuario para generación de código"""
    
    def generate_code_with_dmt(prompt, dmt_amount):
        # Verificar balance DMT
        if not token_manager.has_sufficient_balance(dmt_amount):
            return "Error: Saldo DMT insuficiente"
        
        # Generar código
        code = triton_client.generate_code(prompt)
        
        # Registrar transacción en blockchain
        tx_hash = token_manager.charge_for_generation(dmt_amount)
        
        return f"Código generado:\n\n{code}\n\nTX: {tx_hash}"
    
    # Interfaz Gradio
    with gr.Blocks(title="Diamante Megatron Generator") as demo:
        gr.Markdown("# 🚀 Generador de Código con DMT")
        gr.Markdown("Usa tokens DMT para generar código con WizardLM + Megatron")
        
        with gr.Row():
            with gr.Column():
                prompt = gr.Textbox(
                    label="Prompt de código",
                    placeholder="Escribe aquí lo que quieres generar...",
                    lines=5
                )
                dmt_amount = gr.Slider(
                    minimum=1,
                    maximum=100,
                    value=10,
                    label="Cantidad de DMT a usar"
                )
                generate_btn = gr.Button("✨ Generar Código", variant="primary")
            
            with gr.Column():
                output = gr.Code(
                    label="Código Generado",
                    language="python",
                    interactive=False
                )
                tx_status = gr.Textbox(
                    label="Transacción Solana",
                    interactive=False
                )
        
        # Ejemplos
        examples = [
            ["Genera un contrato inteligente de Solana para un token deflacionario", 20],
            ["Crea una API FastAPI para inference de modelos de lenguaje", 15],
            ["Implementa un sistema de staking con recompensas en NFTs", 25]
        ]
        
        gr.Examples(examples=examples, inputs=[prompt, dmt_amount])
        
        # Eventos
        generate_btn.click(
            fn=generate_code_with_dmt,
            inputs=[prompt, dmt_amount],
            outputs=[output, tx_status]
        )
    
    return demo

if __name__ == "__main__":
    demo = generate_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True  # Crea enlace público
  )

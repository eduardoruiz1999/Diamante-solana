import tritonclient.http as httpclient
import numpy as np
from typing import Dict, Any

class DiamanteTritonClient:
    def __init__(self, url: str = "localhost:8000"):
        self.client = httpclient.InferenceServerClient(url=url)
        self.model_name = "diamante_llm"
        
    def generate_code(self, prompt: str, max_tokens: int = 500) -> str:
        """Generar código usando el modelo en Triton"""
        from .preprocess import DiamantePreprocessor
        from .postprocess import DiamantePostprocessor
        
        preprocessor = DiamantePreprocessor()
        postprocessor = DiamantePostprocessor()
        
        # Generación token por token
        generated_text = prompt
        
        for _ in range(max_tokens):
            # Preprocesar
            inputs = preprocessor.prepare_inputs(generated_text)
            
            # Configurar inputs para Triton
            triton_inputs = [
                httpclient.InferInput(
                    "input_ids",
                    inputs['input_ids'].shape,
                    "INT64"
                ).set_data_from_numpy(inputs['input_ids']),
                httpclient.InferInput(
                    "attention_mask",
                    inputs['attention_mask'].shape,
                    "INT64"
                ).set_data_from_numpy(inputs['attention_mask'])
            ]
            
            # Inferencia
            result = self.client.infer(
                model_name=self.model_name,
                inputs=triton_inputs
            )
            
            # Postprocesar
            logits = result.as_numpy("logits")
            next_token = postprocessor.decode_output(logits[0, -1, :])
            
            # Actualizar texto
            generated_text += next_token
            
            # Condición de parada
            if next_token in ['</s>', '<|endoftext|>']:
                break
                
        return generated_text
    
    def generate_dmt_contract(self, requirements: Dict[str, Any]) -> str:
        """Generar contrato inteligente para token DMT"""
        prompt = f"""
        Genera un contrato inteligente de Solana para el token Diamante (DMT) con:
        - Address: {requirements.get('address')}
        - Decimales: {requirements.get('decimals', 9)}
        - Supply total: {requirements.get('total_supply', '1000000000')}
        - Funcionalidades: Staking, recompensas automáticas, quemado deflacionario
        - Integración con Megatron-ML para recompensas de entrenamiento
        
        El contrato debe incluir:
        1. Implementación SPL Token estándar
        2. Mecanismo de staking con APR dinámico
        3. Recompensas automáticas por participación en entrenamiento de IA
        4. Función de quemado por transacción
        5. Governance integrado
        """
        
        return self.generate_code(prompt)

import numpy as np
from transformers import AutoTokenizer

class DiamantePostprocessor:
    def __init__(self, model_name="QuixiAI/WizardLM-13B-Uncensored"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
    def decode_output(self, logits, temperature=0.7, top_p=0.9):
        """Decodificar salidas del modelo"""
        # Aplicar sampling
        logits = logits / temperature
        probs = torch.softmax(torch.tensor(logits), dim=-1)
        
        # Top-p sampling
        sorted_probs, sorted_indices = torch.sort(probs, descending=True)
        cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
        
        sorted_indices_to_remove = cumulative_probs > top_p
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0
        
        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        probs[indices_to_remove] = 0
        probs = probs / probs.sum()
        
        # Muestrear
        next_token_id = torch.multinomial(probs, 1).item()
        return self.tokenizer.decode([next_token_id])

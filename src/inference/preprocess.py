import torch
from transformers import AutoTokenizer

class DiamantePreprocessor:
    def __init__(self, model_name="QuixiAI/WizardLM-13B-Uncensored"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
    def prepare_inputs(self, text, max_length=1024):
        """Preparar inputs para Triton"""
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].numpy().astype('int64'),
            'attention_mask': encoding['attention_mask'].numpy().astype('int64')
      }

import os
import yaml
import torch
from transformers import AutoTokenizer
from megatron.core import parallel_state
from megatron.core.tensor_parallel.random import model_parallel_cuda_manual_seed
from megatron.training import train_step
from megatron.initialize import initialize_megatron

class DiamanteMegatronTrainer:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Inicializar Megatron
        self._initialize_megatron()
        
        # Configurar token DMT
        self.token_address = os.getenv('DMT_TOKEN_ADDRESS')
        self.private_key = os.getenv('WALLET_PRIVATE_KEY')  # NUNCA en código
        
    def _initialize_megatron(self):
        """Inicializar entorno paralelo de Megatron"""
        args = {
            'tensor_model_parallel_size': self.config['tensor_parallel'],
            'pipeline_model_parallel_size': self.config['pipeline_parallel'],
            'world_size': self.config.get('world_size', 8),
            'use_cpu_initialization': False,
            'micro_batch_size': self.config.get('micro_batch_size', 4),
            'global_batch_size': self.config.get('global_batch_size', 256),
            'lr': self.config.get('learning_rate', 6e-5),
            'train_iters': self.config.get('train_iters', 50000),
        }
        
        initialize_megatron(args)
        model_parallel_cuda_manual_seed(123)
    
    def load_model(self):
        """Cargar modelo WizardLM con adaptadores"""
        from adapters import AutoAdapterModel
        
        print("Cargando modelo base...")
        model = AutoAdapterModel.from_pretrained(
            self.config['base_model'],
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        print("Cargando adaptador MegaSol...")
        model.load_adapter("DeepDemon/MegaSol", set_active=True)
        
        # Congelar capas base, entrenar solo adaptador
        for param in model.parameters():
            param.requires_grad = False
            
        for param in model.active_adapters.parameters():
            param.requires_grad = True
            
        return model
    
    def train(self, model, dataset):
        """Ciclo de entrenamiento personalizado"""
        optimizer = torch.optim.AdamW(
            model.active_adapters.parameters(),
            lr=self.config['learning_rate']
        )
        
        for epoch in range(self.config['epochs']):
            for batch in dataset:
                # Paso de entrenamiento con Megatron
                loss = train_step(model, batch, optimizer)
                
                # Integración con Solana - Recompensas por progreso
                if epoch % 10 == 0:
                    self._reward_training_progress(loss)
                
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
    
    def _reward_training_progress(self, loss):
        """Integración con token DMT en Solana"""
        try:
            from solana.rpc.api import Client
            from solana.transaction import Transaction
            from solders.keypair import Keypair
            
            # Obtener clave desde variables de entorno
            private_key_bytes = bytes.fromhex(os.getenv('WALLET_PRIVATE_KEY'))
            keypair = Keypair.from_bytes(private_key_bytes)
            
            # Lógica de recompensa basada en mejora del loss
            # (Implementar según tu tokenomics)
            print(f"Progreso registrado en blockchain - Loss: {loss}")
            
        except Exception as e:
            print(f"Error en integración Solana: {e}")

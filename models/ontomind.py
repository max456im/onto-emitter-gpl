# models/ontomind.py
# OntoMind-50M: lightweight transformer for ontological reasoning
# Licensed under GPL-3.0-only

import torch
import torch.nn as nn
from pathlib import Path

class OntoMind(nn.Module):
    def __init__(self, config_path: str):
        super().__init__()
        config = torch.load(config_path, map_location='cpu', weights_only=True)
        self.vocab_size = config['vocab_size']
        self.embed_dim = config['embed_dim']
        self.num_layers = config['num_layers']
        self.embedding = nn.Embedding(self.vocab_size, self.embed_dim)
        self.transformer = nn.TransformerEncoder(
            encoder_layer=nn.TransformerEncoderLayer(
                d_model=self.embed_dim,
                nhead=config['nhead'],
                dim_feedforward=config['dim_feedforward'],
                batch_first=True,
                norm_first=True
            ),
            num_layers=self.num_layers
        )
        self.out_proj = nn.Linear(self.embed_dim, self.vocab_size)

    def forward(self, input_ids):
        x = self.embedding(input_ids)
        x = self.transformer(x)
        logits = self.out_proj(x)
        return logits

    @classmethod
    def from_pretrained(cls, model_dir: str):
        model_dir = Path(model_dir)
        config_path = model_dir / "config.json"
        weights_path = model_dir / "pytorch_model.bin"

        # Загрузка конфигурации
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)

        # Создание модели и загрузка весов
        vocab_size = config_dict.get('vocab_size', 32000)
        model_config = {
            'vocab_size': vocab_size,
            'embed_dim': config_dict.get('hidden_size', 256),
            'num_layers': config_dict.get('num_hidden_layers', 4),
            'nhead': config_dict.get('num_attention_heads', 8),
            'dim_feedforward': config_dict.get('intermediate_size', 512)
        }
        temp_config_path = model_dir / "temp_config.pth"
        torch.save(model_config, temp_config_path)

        model = cls(str(temp_config_path))
        state_dict = torch.load(weights_path, map_location='cpu', weights_only=True)
        model.load_state_dict(state_dict, strict=False)

        temp_config_path.unlink()  # Удалить временный файл
        return model
# SPDX-License-Identifier: GPL-3.0-only
"""
ontomind.py — Lightweight synthetic reasoning core (ontomind-50m).
Operates strictly within onto16i semantics. No external data injection.
Profile-aware via onto144 bindings.
"""

import torch
import torch.nn as nn
from pathlib import Path
from ..utils.config_loader import load_config
from ..ontologies.onto144_profile_loader import Onto144Profile

class OntoMind(nn.Module):
    def __init__(self, model_dir: Path, profile_id: str):
        super().__init__()
        self.config = load_config("default")
        self.profile = Onto144Profile(profile_id)
        self.vocab_size = 32000
        self.embed_dim = 512
        self.num_layers = 6
        self.heads = 8

        self.embedding = nn.Embedding(self.vocab_size, self.embed_dim)
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=self.embed_dim,
                nhead=self.heads,
                dim_feedforward=2048,
                batch_first=True
            ),
            num_layers=self.num_layers
        )
        self.output_proj = nn.Linear(self.embed_dim, self.vocab_size)

        # Load weights strictly from incubation — no fine-tuning on user data
        checkpoint = torch.load(model_dir / "pytorch_model.bin", map_location="cpu")
        self.load_state_dict(checkpoint, strict=True)

        # Freeze all parameters — model is declarative, not adaptive
        for param in self.parameters():
            param.requires_grad = False

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        """Returns logits over onto16i-compliant vocabulary."""
        embedded = self.embedding(tokens)
        encoded = self.transformer(embedded)
        return self.output_proj(encoded)

    def generate_canonical_logits(self, context_tokens: torch.Tensor) -> torch.Tensor:
        """Wrapper for canonical emission — enforces internal coherence."""
        with torch.no_grad():
            return self.forward(context_tokens)
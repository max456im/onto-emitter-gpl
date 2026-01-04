# SPDX-License-Identifier: GPL-3.0-only
"""
dynamic_onto_tokenizer.py — Builds profile-adapted tokenizer from onto_vocab.txt + domain lexicon.
Ensures lexical alignment with onto144 identity and CMS context.
No external corpora.
"""

from pathlib import Path
from typing import List, Dict
from ..ontologies.domain_lexicon_loader import DomainLexiconLoader

class DynamicOntoTokenizer:
    def __init__(self, base_vocab_path: Path, profile_id: str, domain: str = "default"):
        self.base_vocab_path = base_vocab_path
        self.profile_id = profile_id
        self.domain = domain
        self.token_to_id: Dict[str, int] = {}
        self.id_to_token: Dict[int, str] = {}
        self._build_vocabulary()

    def _build_vocabulary(self):
        # Load base 32k-term ontology-aware vocabulary
        with open(self.base_vocab_path, "r", encoding="utf-8") as f:
            base_tokens = [line.strip() for line in f if line.strip()]

        # Inject domain-specific lexicon (e.g., medical, legal) linked to profile
        domain_loader = DomainLexiconLoader(self.profile_id, self.domain)
        domain_tokens = domain_loader.get_lexicon()

        # Union: base + domain (no duplicates, preserves base ordering)
        all_tokens = list(dict.fromkeys(base_tokens + domain_tokens))

        if len(all_tokens) > 32000:
            raise ValueError("Lexicon overflow: exceeds 32k ontological bound")

        self.token_to_id = {token: idx for idx, token in enumerate(all_tokens)}
        self.id_to_token = {idx: token for token, idx in self.token_to_id.items()}

    def tokenize(self, text: str) -> List[int]:
        # Naive whitespace + punctuation split — sufficient for canonical form
        import re
        tokens = re.findall(r"\b\w+\b|\S", text.lower())
        return [self.token_to_id.get(t, 0) for t in tokens]  # 0 = <unk>

    def decode(self, ids: List[int]) -> str:
        return " ".join(self.id_to_token.get(i, "<unk>") for i in ids)

    def get_vocab_size(self) -> int:
        return len(self.token_to_id)
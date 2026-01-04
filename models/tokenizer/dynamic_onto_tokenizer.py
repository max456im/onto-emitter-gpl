# models/tokenizer/dynamic_onto_tokenizer.py
# Dynamically constructs tokenizer based on onto144 profile and domain lexicon
# No user data. Only canonical ontological terms.

import re
from typing import List, Dict
from pathlib import Path

class DynamicOntoTokenizer:
    def __init__(self, base_vocab_path: str, profile_terms: List[str], domain_lexicon: List[str]):
        """
        profile_terms: from onto144 (identity kernel)
        domain_lexicon: from cms_context_injector or domain_lexicon_loader
        """
        self.vocab = self._build_vocab(base_vocab_path, profile_terms, domain_lexicon)
        self.token_to_id = {token: idx for idx, token in enumerate(self.vocab)}
        self.id_to_token = {idx: token for token, idx in self.token_to_id.items()}

    def _load_base_vocab(self, path: str) -> List[str]:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def _normalize_term(self, term: str) -> str:
        return re.sub(r'\s+', '_', term.lower())

    def _build_vocab(self, base_path: str, profile_terms: List[str], domain_lexicon: List[str]) -> List[str]:
        base = set(self._load_base_vocab(base_path))
        profile_norm = {self._normalize_term(t) for t in profile_terms}
        domain_norm = {self._normalize_term(t) for t in domain_lexicon}
        # Приоритет: профиль > домен > база
        combined = list(profile_norm) + list(domain_norm - profile_norm) + list(base - profile_norm - domain_norm)
        return combined[:32000]  # Ограничение, как в onto_vocab.txt

    def encode(self, text: str) -> List[int]:
        tokens = re.findall(r'\b\w+\b', text.lower())
        return [self.token_to_id.get(t, 0) for t in tokens]  # 0 = <unk>

    def decode(self, ids: List[int]) -> str:
        return ' '.join(self.id_to_token.get(i, '<unk>') for i in ids)
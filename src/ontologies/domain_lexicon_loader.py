# SPDX-License-Identifier: GPL-3.0-only
"""
Загружает доменный лексикон на основе привязки из конфигурации.
Лексиконы — необучаемые, только канонические термины (32k+ в onto_vocab.txt + доменные расширения).
"""

import os
from pathlib import Path
from typing import Set, List, Optional
import json

from ..utils.config_loader import load_config

class DomainLexiconLoader:
    def __init__(self, config_path: Optional[str] = None):
        self.config = load_config(config_path or "domain_bindings.yaml")
        self.lexicons_root = Path(self.config.get("lexicons_root", "./data/lexicons"))

    def load_domain_lexicon(self, domain_key: str) -> Set[str]:
        """
        Загружает термины для домена (например, 'legal', 'medical').
        Возвращает объединённый набор: базовый словарь + доменные термины.
        """
        base_vocab_path = Path("models/ontomind-50m/onto_vocab.txt")
        domain_vocab_path = self.lexicons_root / f"{domain_key}.json"

        terms = set()

        # Базовый словарь (обязательный)
        if base_vocab_path.exists():
            with open(base_vocab_path, "r", encoding="utf-8") as f:
                terms.update(line.strip() for line in f if line.strip())

        # Доменный лексикон (опциональный)
        if domain_vocab_path.exists():
            with open(domain_vocab_path, "r", encoding="utf-8") as f:
                domain_data = json.load(f)
                terms.update(domain_data.get("terms", []))

        return terms

    def get_allowed_terms(self, profile_lexicon_ref: str) -> Set[str]:
        """
        Получает разрешённые термины для профиля через привязку в конфиге.
        """
        domain_key = self.config.get("bindings", {}).get(profile_lexicon_ref, "default")
        return self.load_domain_lexicon(domain_key)
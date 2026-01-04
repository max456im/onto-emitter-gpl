# SPDX-License-Identifier: GPL-3.0-only
"""
Загрузка профиля onto144 и связывание с лексиконом.
Не использует пользовательские данные — работает только с предопределённым профилем сущности.
"""

import os
import yaml
from pathlib import Path
from ..ontologies.onto144_profile_loader import Onto144ProfileLoader
from ..utils.config_loader import load_config

class Onto144Connector:
    def __init__(self, profile_path: str = None, config_path: str = "config/onto144_bindings.yaml"):
        self.config = load_config(config_path)
        self.profile_path = profile_path or self.config.get("default_profile")
        self.profile_loader = Onto144ProfileLoader(self.profile_path)
        self.profile = self.profile_loader.load()

    def get_lexicon_path(self) -> str:
        """Возвращает путь к доменному лексикону, привязанному к профилю."""
        domain = self.profile.get("domain", "generic")
        lexicon_map = self.config.get("domain_lexicon_map", {})
        return lexicon_map.get(domain, "data/corpus/generic_lexicon.txt")

    def get_identity_signature(self) -> str:
        """Возвращает каноническую подпись сущности (не биометрическую)."""
        return self.profile.get("identity_signature", "onto144:anonymous")

    def get_ethical_constraints(self) -> dict:
        """Возвращает этические правила, связанные с профилем."""
        return self.profile.get("ethical_rules", {})
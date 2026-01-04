# SPDX-License-Identifier: GPL-3.0-only
"""
Загружает онтологический профиль из onto144.
Профиль определяет ядро субъективности, этические привязки и лексикон.
Не использует пользовательские данные — только идентификатор синтетического субъекта.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

from ..utils.config_loader import load_config

class Onto144ProfileLoader:
    def __init__(self, profile_id: str, base_path: Optional[str] = None):
        """
        :param profile_id: Идентификатор профиля в onto144 (например, 'sub_duo_alpha')
        :param base_path: Путь к корню onto144 (по умолчанию — окружение или config)
        """
        self.profile_id = profile_id
        self.base_path = base_path or os.getenv("ONTO144_ROOT", "./onto144_repo")
        self.profile_path = Path(self.base_path) / "profiles" / f"{profile_id}.yaml"
        if not self.profile_path.exists():
            raise FileNotFoundError(f"onto144 profile not found: {self.profile_path}")

    def load_profile(self) -> Dict[str, Any]:
        """Загружает полный профиль (онтологическое ядро, этика, домены)."""
        with open(self.profile_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_lexicon_ref(self) -> str:
        """Возвращает ссылку на лексикон (например, 'medical_core_v3')."""
        profile = self.load_profile()
        return profile.get("lexicon", "default")

    def get_ethical_context(self) -> Dict[str, Any]:
        """Извлекает этический контекст для VMA."""
        profile = self.load_profile()
        return profile.get("ethics", {})
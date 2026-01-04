# config_loader.py — GPL-3.0-only
"""
Загрузка конфигурации с валидацией и привязкой к контексту профиля onto144.
"""

import os
import yaml
from typing import Dict, Any

def load_config(config_path: str, profile_id: str = None) -> Dict[str, Any]:
    """
    Загружает YAML-конфиг и, если задан profile_id, применяет привязку из domain_bindings.yaml.
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Config not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if profile_id and config_path.endswith("default.yaml"):
        # Подгружаем domain_bindings для профиля
        bindings_path = os.path.join(os.path.dirname(config_path), "domain_bindings.yaml")
        if os.path.isfile(bindings_path):
            with open(bindings_path, "r", encoding="utf-8") as f:
                bindings = yaml.safe_load(f)
            if profile_id in bindings:
                config.setdefault("domain", {}).update(bindings[profile_id])

    return config
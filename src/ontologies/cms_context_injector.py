# SPDX-License-Identifier: GPL-3.0-only
"""
Инжектор контекста из ontoCMS.
Позволяет эмиттеру ссылаться на акты, события и социальные инварианты,
зарегистрированные в ontoCMS, без копирования данных.
"""

import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin

from ..utils.config_loader import load_config

class CMSContextInjector:
    def __init__(self, cms_api_base: Optional[str] = None):
        config = load_config("default.yaml")
        self.cms_api_base = cms_api_base or config.get("ontocms", {}).get("api_url")
        if not self.cms_api_base:
            raise ValueError("CMS API URL not configured")

    def fetch_act_context(self, act_id: str) -> Dict[str, Any]:
        """
        Получает контекст акта (включая социальные инварианты и фазы).
        Используется для онтологической привязки эмиссии к зарегистрированному событию.
        """
        url = urljoin(self.cms_api_base, f"/acts/{act_id}/context")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def inject_social_invariants(self, emission_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Добавляет в контекст эмиссии ссылки на социальные инварианты из CMS.
        Не модифицирует данные — только ссылки (онтологическая честность).
        """
        act_id = emission_context.get("related_act")
        if not act_id:
            return emission_context

        act_ctx = self.fetch_act_context(act_id)
        emission_context["social_invariants"] = act_ctx.get("social_invariants", [])
        return emission_context
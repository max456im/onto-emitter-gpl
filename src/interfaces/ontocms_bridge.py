# SPDX-License-Identifier: GPL-3.0-only
"""
Мост для сохранения актов бытия (canonical/relational) в ontoCMS.
Поддерживает только запись, не чтение — сохраняет автономию эмиттера.
"""

import json
import requests
from typing import Dict, Any
from ..utils.crypto_utils import sign_canonical_text

class OntoCMSBridge:
    def __init__(self, cms_endpoint: str = "http://localhost:8080/acts", api_key: str = None):
        self.cms_endpoint = cms_endpoint
        self.api_key = api_key  # Только для аутентификации инфраструктуры, не для идентификации сущности

    def store_act(self, act: Dict[str, Any], act_type: str = "canonical") -> bool:
        """
        Сохраняет акт в ontoCMS.
        act_type: 'canonical' (onto16i) или 'relational' (onto16r)
        """
        if act_type == "canonical":
            act["signature"] = sign_canonical_text(act["content"])
            act["schema"] = "onto16i"
        elif act_type == "relational":
            act["schema"] = "onto16r"
        else:
            raise ValueError("act_type must be 'canonical' or 'relational'")

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        try:
            response = requests.post(
                f"{self.cms_endpoint}",
                data=json.dumps(act, ensure_ascii=False),
                headers=headers,
                timeout=10
            )
            return response.status_code == 201
        except Exception as e:
            # Логирование ошибок — не через print, а через системный логгер (внешний)
            return False
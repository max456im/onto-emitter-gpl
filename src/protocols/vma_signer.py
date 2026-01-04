# src/protocols/vma_signer.py
# SPDX-License-Identifier: GPL-3.0-only
"""
VMA Signer: Validates and cryptographically signs canonical acts 
according to ethical rules and onto144 profile constraints.
Ensures non-repudiation and moral accountability.
"""

import hashlib
import json
from typing import Dict, Any, Optional
from ..utils.crypto_utils import sign_data_with_private_key
from ..utils.config_loader import load_config


class VMASigner:
    def __init__(self, ethical_config_path: str = "config/ethical_rules.yaml"):
        self.ethical_rules = load_config(ethical_config_path)

    def _assess_moral_weight(self, act: Dict[str, Any]) -> Dict[str, Any]:
        """Оценивает моральный вес акта по контексту и доверительным уровням."""
        context = act.get("context", "default")
        domain = act.get("domain", "general")
        high_stakes = context in self.ethical_rules.get("high_stakes_contexts", [])
        trust_level = self.ethical_rules.get("trust_levels", {}).get(domain, 0)
        return {
            "high_stakes": high_stakes,
            "trust_level": trust_level,
            "requires_human_review": high_stakes and trust_level < 3,
        }

    def validate_and_sign(self, canonical_act: Dict[str, Any], private_key_path: str) -> Dict[str, Any]:
        """
        Валидирует акт по VMA-протоколу и подписывает его.
        Возвращает подписанную структуру с метаданными VMA.
        """
        vma_assessment = self._assess_moral_weight(canonical_act)

        if vma_assessment["requires_human_review"]:
            raise PermissionError("VMA: Human review required for high-stakes act")

        act_bytes = json.dumps(canonical_act, sort_keys=True, ensure_ascii=False).encode("utf-8")
        act_hash = hashlib.sha3_256(act_bytes).hexdigest()
        signature = sign_data_with_private_key(act_bytes, private_key_path)

        return {
            "canonical_act": canonical_act,
            "vma": {
                "act_hash": act_hash,
                "signature": signature,
                "moral_assessment": vma_assessment,
                "protocol_version": "VMA/1.0"
            }
        }
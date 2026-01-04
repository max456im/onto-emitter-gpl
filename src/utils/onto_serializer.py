# onto_serializer.py — GPL-3.0-only
"""
Безопасная сериализация онтологических состояний.
Поддерживает onto16i (внутреннее) и onto16r (реляционное) без утечки энергетических значений.
"""

import json
from typing import Any, Dict, Union
from .crypto_utils import sign_canonical_bytes

def serialize_onto16(
    state: Dict[str, Any],
    mode: str = "onto16r",
    apply_vma: bool = False,
    private_key: Union[bytes, None] = None
) -> str:
    """
    Сериализует состояние в канонический JSON.
    mode: 'onto16i' или 'onto16r'
    Не включает энергетические значения в финальный вывод (согласно принципу недевальвации).
    """
    if mode not in ("onto16i", "onto16r"):
        raise ValueError("mode must be 'onto16i' or 'onto16r'")

    # Удаляем внутренние поля, недопустимые в финальных актах
    clean_state = {
        k: v for k, v in state.items()
        if not k.startswith("_") and k != "energy_value"
    }

    payload = {
        "schema": f"https://onto.org/specs/{mode}",
        "mode": mode,
        "content": clean_state
    }

    if apply_vma and private_key:
        canonical_bytes = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        signature = sign_canonical_bytes(canonical_bytes, private_key)
        payload["vma_signature"] = signature.hex()

    return json.dumps(payload, indent=2, ensure_ascii=False)
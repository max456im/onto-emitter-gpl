# SPDX-License-Identifier: GPL-3.0-only
"""
NoemaSlow Bridge: восстановление причинно-следственных связей в ретроспективном мышлении.
Работает с onto16i после фазового сдвига из NoemaFast.
"""
from typing import Dict, Any, List
from src.utils.config_loader import load_config
from src.utils.onto_serializer import OntoSerializer
from src.protocols.causal_logger import CausalLogger

class NoemaSlowBridge:
    def __init__(self, config_path: str = "config/default.yaml"):
        self.config = load_config(config_path)
        self.causal_logger = CausalLogger()
        self.serializer = OntoSerializer()

    def restore_causality(self, onto16i_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Восстанавливает причинные связи на основе истории, зафиксированной в onto16i.
        Возвращает стабилизированное внутреннее состояние.
        """
        causal_chain = self._extract_causal_chain(onto16i_state)
        repaired_chain = self._repair_chain(causal_chain)
        onto16i_state["causal_chain"] = repaired_chain
        self.causal_logger.log_chain(repaired_chain)
        return onto16i_state

    def _extract_causal_chain(self, state: Dict[str, Any]) -> List[Dict]:
        # Извлекает цепочку событий из внутреннего состояния
        return state.get("event_log", [])

    def _repair_chain(self, chain: List[Dict]) -> List[Dict]:
        # Простая реализация: помечает разрывы, предлагает гипотезы
        repaired = []
        for i, event in enumerate(chain):
            if i > 0 and not self._is_causally_connected(chain[i-1], event):
                repaired.append({
                    "type": "causal_gap",
                    "between": [chain[i-1]["id"], event["id"]],
                    "hypothesis": self._generate_causal_hypothesis(chain[i-1], event)
                })
            repaired.append(event)
        return repaired

    def _is_causally_connected(self, prev: Dict, curr: Dict) -> bool:
        # Проверка по онтологическим предикатам
        return curr.get("cause_id") == prev.get("id")

    def _generate_causal_hypothesis(self, prev: Dict, curr: Dict) -> str:
        return f"Предположительная связь между {prev.get('label')} и {curr.get('label')}"
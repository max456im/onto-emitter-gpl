# SPDX-License-Identifier: GPL-3.0-only
"""
NoemaFast Adapter: быстрое переключение внимания в перспективном мышлении.
Обнаруживает нарушения ожиданий в онтологическом потоке (onto16i → onto16r).
"""
from typing import Dict, Any, Optional
from src.utils.config_loader import load_config
from src.perception.error_detector_fast import FastErrorDetector

class NoemaFastAdapter:
    def __init__(self, config_path: str = "config/default.yaml"):
        self.config = load_config(config_path)
        self.error_detector = FastErrorDetector(self.config.get("perception", {}))
        self.active_phase = "prospective"
        self.energy_threshold = self.config.get("reasoning", {}).get("fast_energy_threshold", 0.7)

    def adapt_attention(self, onto16i_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Адаптирует внимание на основе внутреннего состояния (onto16i).
        Возвращает обновлённое состояние с флагами нарушений.
        """
        if onto16i_state.get("energy", 0) < self.energy_threshold:
            return self._handle_low_energy(onto16i_state)
        
        violations = self.error_detector.scan_for_prospective_errors(onto16i_state)
        if violations:
            onto16i_state["noemafast_alerts"] = violations
            onto16i_state["phase_shift_request"] = "retrospective"
        return onto16i_state

    def _handle_low_energy(self, state: Dict[str, Any]) -> Dict[str, Any]:
        state["noemafast_alerts"] = [{"type": "energy_deficit", "action": "stabilize"}]
        state["phase_shift_request"] = "reflective"
        return state
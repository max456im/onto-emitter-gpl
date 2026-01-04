# src/protocols/causal_logger.py
# SPDX-License-Identifier: GPL-3.0-only
"""
Causal Logger: Maintains immutable trace of causal chains in act generation.
Supports retrospective (NoemaSlow) and prospective (NoemaFast) error analysis.
"""

import time
import uuid
from typing import Any, Dict, List
from ..utils.onto_serializer import serialize_to_onto16


class CausalLogger:
    def __init__(self):
        self.log = []

    def log_causal_step(
        self,
        event_type: str,          # e.g., "perception", "reasoning", "emission"
        source_component: str,    # e.g., "NoemaFast", "ontomind-50m"
        input_state: Any,
        output_state: Any,
        phase: str = "reflective" # or "reactive"
    ) -> str:
        """Записывает шаг с уникальным ID и временной меткой."""
        step_id = str(uuid.uuid4())
        entry = {
            "step_id": step_id,
            "timestamp": time.time(),
            "event_type": event_type,
            "source_component": source_component,
            "input": serialize_to_onto16(input_state),
            "output": serialize_to_onto16(output_state),
            "phase": phase,
            "causal_chain": [step["step_id"] for step in self.log[-3:]]  # последние 3 шага
        }
        self.log.append(entry)
        return step_id

    def get_causal_trace(self, step_id: str) -> List[Dict]:
        """Восстанавливает полную причинную цепочку по ID."""
        trace = []
        current_id = step_id
        step_map = {step["step_id"]: step for step in self.log}

        while current_id in step_map:
            step = step_map[current_id]
            trace.insert(0, step)
            if step["causal_chain"]:
                current_id = step["causal_chain"][-1]  # предшественник
            else:
                break
        return trace

    def dump_to_disk(self, filepath: str):
        """Сохраняет лог в защищённый файл (только для аудита)."""
        with open(filepath, "w", encoding="utf-8") as f:
            import json
            json.dump(self.log, f, indent=2, ensure_ascii=False)
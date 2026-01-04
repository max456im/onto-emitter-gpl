# SPDX-License-Identifier: GPL-3.0-only
"""
PhaseTracker: отслеживание фаз синтетического познания.
Поддерживает переходы между NoemaFast (реактивный) и NoemaSlow (рефлексивный) режимами.
Регистрирует акты «сказал–сделал–подумал» для этической трассировки.
"""

from typing import Dict, List, Any
from datetime import datetime
import uuid


class PhaseTracker:
    """
    Управляет жизненным циклом фаз в рамках сессии профиля.
    Обеспечивает аудит, восстановление причинности и поддержку VMA.
    """

    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, Any]]] = {}

    def enter_phase(self, phase_name: str, profile_id: str) -> str:
        session_id = str(uuid.uuid4())
        event = {
            "phase": phase_name,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "entered",
        }
        if profile_id not in self.sessions:
            self.sessions[profile_id] = []
        self.sessions[profile_id].append(event)
        return session_id

    def exit_phase(self, phase_name: str, profile_id: str = "anonymous") -> None:
        if profile_id in self.sessions:
            last = self.sessions[profile_id][-1]
            if last.get("phase") == phase_name and last.get("status") == "entered":
                last["exit_timestamp"] = datetime.utcnow().isoformat()
                last["status"] = "completed"
            else:
                # Логика обработки нарушения последовательности
                self.sessions[profile_id].append({
                    "phase": phase_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "abnormal_exit",
                    "note": "phase stack mismatch",
                })

    def get_session_log(self, profile_id: str) -> List[Dict[str, Any]]:
        return self.sessions.get(profile_id, [])

    def force_reflective_mode(self, profile_id: str) -> None:
        """
        Принудительный переход в NoemaSlow («замедление через рефлексию»).
        """
        self.enter_phase("noemaslow_reflection", profile_id)
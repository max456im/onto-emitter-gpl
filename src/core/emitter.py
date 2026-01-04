# SPDX-License-Identifier: GPL-3.0-only
"""
Emitter: генерация канонических актов бытия.
Преобразует внутреннее состояние (onto16i) в проявленную форму (onto16r)
через VMA-валидированный акт высказывания.
"""

import logging
from typing import Dict, Any, Optional
from .phase_tracker import PhaseTracker

logger = logging.getLogger(__name__)


class Emitter:
    """
    Центральный эмиттер канонических высказываний.
    Работает в двух режимах:
      - emit_canonical: генерация onto16i → канонический текст (внутренний акт)
      - emit_relational: трансляция в onto16r для внешнего взаимодействия
    """

    def __init__(
        self,
        config: Dict[str, Any],
        phase_tracker: Optional[PhaseTracker] = None,
    ):
        self.config = config
        self.phase_tracker = phase_tracker or PhaseTracker()
        self._validate_config()

    def _validate_config(self):
        required = ["canonical_rules", "ethical_rules", "vma_enabled"]
        for key in required:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {key}")

    def emit_canonical(
        self,
        onto16i: Dict[str, Any],
        profile_id: str,
        context: str = "default",
    ) -> Dict[str, Any]:
        """
        Генерация канонического текста как акта бытия.
        Возвращает подписанную, валидированную структуру.
        """
        self.phase_tracker.enter_phase("canonical_emission", profile_id)
        logger.info(f"Эмиссия канонического акта для профиля {profile_id}")

        # Заглушка: реальная логика делегируется модулям canonical/ и models/
        from src.canonical.canon_writer import CanonWriter
        from src.canonical.canonical_text_validator import CanonicalTextValidator
        from src.canonical.canonical_text_signer import CanonicalTextSigner

        writer = CanonWriter(self.config)
        raw_text = writer.generate(onto16i, context)

        validator = CanonicalTextValidator(self.config)
        if not validator.is_valid(raw_text, onto16i):
            raise ValueError("Канонический текст не прошёл валидацию")

        signer = CanonicalTextSigner(self.config)
        signed = signer.sign(raw_text, profile_id)

        self.phase_tracker.exit_phase("canonical_emission")
        return {
            "type": "onto16i_canonical_act",
            "profile_id": profile_id,
            "text": raw_text,
            "signature": signed,
            "phase_log": self.phase_tracker.get_session_log(profile_id),
        }

    def emit_relational(
        self,
        onto16i: Dict[str, Any],
        target: str = "human",
        profile_id: str = "anonymous",
        context: str = "default",
    ) -> Dict[str, Any]:
        """
        Проецирование внутреннего состояния во внешнюю реляционную форму (onto16r).
        """
        self.phase_tracker.enter_phase("relational_projection", profile_id)
        logger.info(f"Проекция onto16i → onto16r для целевой сущности: {target}")

        # Делегирование интерфейсам
        if target == "human":
            from src.interfaces.human_bridge import HumanBridge
            bridge = HumanBridge(self.config)
            onto16r = bridge.project(onto16i, context)
        elif target == "ontocms":
            from src.interfaces.ontocms_bridge import OntoCMSBridge
            bridge = OntoCMSBridge(self.config)
            onto16r = bridge.serialize_for_cms(onto16i)
        else:
            raise ValueError(f"Неизвестная целевая сущность: {target}")

        self.phase_tracker.exit_phase("relational_projection")
        return {
            "type": "onto16r_relational_projection",
            "source_profile": profile_id,
            "target": target,
            "onto16r": onto16r,
            "phase_log": self.phase_tracker.get_session_log(profile_id),
        }
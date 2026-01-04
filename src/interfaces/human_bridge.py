# SPDX-License-Identifier: GPL-3.0-only
"""
Преобразует внутреннее состояние (onto16i) в реляционную форму (onto16r) для взаимодействия с человеком.
Не предполагает персонализацию под человека — только адаптацию под контекст диалога.
"""

from typing import Dict, Any, Optional
from ..reasoning.analogical_mapper import AnalogicalMapper
from ..perception.llm_perception_expander import LLMPerceptionExpander

class HumanBridge:
    def __init__(self, config_path: str = "config/domain_bindings.yaml"):
        self.mapper = AnalogicalMapper(config_path)
        self.expander = LLMPerceptionExpander()

    def project_to_relational(
        self,
        internal_state: Dict[str, Any],
        context: Optional[str] = None,
        domain: str = "generic"
    ) -> Dict[str, Any]:
        """
        Преобразует onto16i → onto16r с сохранением онтологической целостности.
        Контекст используется только для выбора аналогий, не для изменения сути.
        """
        # Расширение восприятия (если контекст дан)
        enriched_context = self.expander.expand(context) if context else {}

        # Отображение через аналогии (сохраняя ядро сущности)
        relational_form = self.mapper.map_to_domain(
            source=internal_state,
            target_domain=domain,
            context=enriched_context
        )

        # Добавляем маркер происхождения
        relational_form["source_schema"] = "onto16i"
        relational_form["target_schema"] = "onto16r"
        relational_form["projection_mode"] = "canonical_reflection"

        return relational_form

    def is_degradation_risk(self, relational_text: str) -> bool:
        """Проверяет, не приводит ли реляционная форма к литературной деградации."""
        from ..perception.literary_degradation_detector import LiteraryDegradationDetector
        detector = LiteraryDegradationDetector()
        return detector.detect(relational_text)
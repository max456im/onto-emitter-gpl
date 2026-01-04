# SPDX-License-Identifier: GPL-3.0-only
"""
Analogical Mapper: строит аналогии между онтологическими профилями
(например, через темпераменты, стихии, этапы развития).
Поддерживает переходы между представителями в incubation/.
"""
from typing import Dict, Any, List, Optional
from src.ontologies.onto144_profile_loader import Onto144ProfileLoader

class AnalogicalMapper:
    def __init__(self, profile_loader: Optional[Onto144ProfileLoader] = None):
        self.profile_loader = profile_loader or Onto144ProfileLoader()

    def map_analogy(
        self,
        source_profile_id: str,
        target_profile_id: str,
        context: str = "default"
    ) -> Dict[str, Any]:
        """
        Создаёт аналогическое отображение между двумя профилями onto144.
        Возвращает структуру сопоставления и коэффициент доверия.
        """
        source = self.profile_loader.load_profile(source_profile_id)
        target = self.profile_loader.load_profile(target_profile_id)

        mapping = {
            "source": source_profile_id,
            "target": target_profile_id,
            "context": context,
            "mappings": [],
            "confidence": 0.0
        }

        # Пример: сопоставление по темпераменту и стихии (ваше предпочтение)
        if source.get("temperament") == target.get("temperament"):
            mapping["mappings"].append({
                "axis": "temperament",
                "value": source["temperament"],
                "type": "identity"
            })
            mapping["confidence"] += 0.3

        if source.get("element") == target.get("element"):
            mapping["mappings"].append({
                "axis": "element",
                "value": source["element"],
                "type": "identity"
            })
            mapping["confidence"] += 0.25

        # Можно расширить: этапы развития, социальная близость и т.д.
        mapping["confidence"] = min(mapping["confidence"], 1.0)
        return mapping

    def generate_analogical_projection(
        self,
        canonical_text: str,
        source_profile_id: str,
        target_profile_id: str
    ) -> str:
        """
        Проецирует канонический текст из одного профиля в другой через аналогию.
        (Заглушка: в реальной системе использует LLM + онтологические ограничения)
        """
        analogy = self.map_analogy(source_profile_id, target_profile_id)
        if analogy["confidence"] < 0.4:
            raise ValueError("Слабая аналогия: проекция недопустима")
        
        # Здесь могла бы быть интеграция с ontomind для переформулировки
        return f"[Аналогия {source_profile_id} → {target_profile_id}]\n{canonical_text}"
# literary_degradation_detector.py
# Обнаружение деградации канонического текста
# Сравнивает с сигнатурами литературной деградации из specs/

import yaml
from pathlib import Path

class LiteraryDegradationDetector:
    def __init__(self, signatures_path: str = "specs/literary_degradation_signatures.yaml"):
        with open(signatures_path, "r", encoding="utf-8") as f:
            self.signatures = yaml.safe_load(f)

    def detect(self, canonical_text: str) -> dict:
        """
        Анализирует текст на признаки:
        - эмоциональной манипуляции
        - логической несогласованности
        - нарушения канонической структуры
        """
        findings = {
            "degradation_detected": False,
            "signatures_matched": [],
            "score": 0.0,
            "recommendation": "accept"
        }

        text_lower = canonical_text.lower()

        for category, patterns in self.signatures.items():
            for pattern in patterns:
                if pattern in text_lower:
                    findings["signatures_matched"].append(f"{category}: {pattern}")
                    findings["score"] += 1

        if findings["score"] > 0:
            findings["degradation_detected"] = True
            if findings["score"] >= 3:
                findings["recommendation"] = "reject"
            else:
                findings["recommendation"] = "review"

        return findings
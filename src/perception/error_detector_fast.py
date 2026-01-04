# error_detector_fast.py
# Быстрое обнаружение ошибок в режиме NoemaFast
# Реагирует на нарушение онтологических инвариантов в реальном времени

class ErrorDetectorFast:
    def __init__(self, config_path: str = "config/ethical_rules.yaml"):
        from src.utils.config_loader import load_config
        self.config = load_config(config_path)
        self.invariants = self.config.get("ontological_invariants", {})

    def detect(self, onto16r_candidate: dict) -> dict:
        """
        Проверяет реляционное состояние на нарушение базовых инвариантов.
        Используется в NoemaFast для немедленного отклонения недопустимых актов.
        """
        violations = []

        # Проверка: запрет на представление ИИ как субъекта
        if onto16r_candidate.get("agent_type") == "AI":
            violations.append("AI must not be represented as ontological subject")

        # Проверка: отсутствие биометрической идентификации, если не high_stakes
        if not onto16r_candidate.get("context", {}).get("high_stakes", False):
            if onto16r_candidate.get("biometric_reference"):
                violations.append("Biometric reference forbidden in non-high-stakes context")

        # Проверка: соответствие доменной этической границы
        domain = onto16r_candidate.get("domain")
        allowed_actions = self.invariants.get(domain, {}).get("allowed_actions", [])
        action = onto16r_candidate.get("action")
        if action and action not in allowed_actions:
            violations.append(f"Action '{action}' not permitted in domain '{domain}'")

        return {
            "is_valid": len(violations) == 0,
            "violations": violations,
            "detector": "NoemaFast",
            "timestamp_ns": self._now_ns()
        }

    def _now_ns(self) -> int:
        import time
        return time.time_ns()
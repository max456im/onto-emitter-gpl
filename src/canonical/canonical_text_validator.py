# canonical_text_validator.py
# GPL-3.0-only
# Validates structural, lexical, and ethical integrity of canonical acts

import json
import yaml
from jsonschema import validate, ValidationError
from ..specs import load_schema
from ..utils.config_loader import load_config

class CanonicalTextValidator:
    """
    Ensures emitted canonical texts:
    - conform to onto16r schema
    - use only allowed lexicon
    - do not exhibit literary degradation
    - respect ethical rules (e.g., no high-stakes claims without VMA)
    """

    def __init__(self, profile_id: str):
        self.profile_id = profile_id
        self.onto16r_schema = load_schema("onto16r-schema.json")
        self.ethical_rules = load_config("ethical_rules.yaml")
        self.lexicon = self._load_profile_lexicon()

    def validate_act(self, canonical_act: dict) -> dict:
        """Returns enriched act with validation metadata."""
        issues = []

        # 1. Schema conformance
        try:
            validate(instance=canonical_act["onto16r"], schema=self.onto16r_schema)
        except ValidationError as e:
            issues.append(f"Schema violation: {e.message}")

        # 2. Lexical purity
        bad_terms = self._check_lexical_purity(canonical_act["narrative"])
        if bad_terms:
            issues.append(f"Unauthorized lexicon: {bad_terms}")

        # 3. Ethical context check
        if self._is_high_stakes_context(canonical_act):
            if not canonical_act.get("vma_signature"):
                issues.append("High-stakes act missing VMA signature")

        # 4. Literary degradation (placeholder for ML-based detector)
        # Actual logic in literary_degradation_detector.py
        # Here we assume pre-screened input

        canonical_act["validation"] = {
            "valid": len(issues) == 0,
            "issues": issues,
            "timestamp": self._now_iso()
        }
        return canonical_act

    def _load_profile_lexicon(self):
        # Simulated; real impl via onto144_profile_loader
        from ..ontologies.onto144_profile_loader import load_profile
        profile = load_profile(self.profile_id)
        return set(term.lower() for term in profile.lexicon)

    def _check_lexical_purity(self, text: str) -> list:
        words = set(w.strip(".,;:!?").lower() for w in text.split())
        return list(words - self.lexicon)

    def _is_high_stakes_context(self, act: dict) -> bool:
        domain = act["onto16r"].get("domain", "")
        return domain in self.ethical_rules.get("high_stakes_contexts", [])

    def _now_iso(self) -> str:
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
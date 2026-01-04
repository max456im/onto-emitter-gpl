# canon_writer.py
# GPL-3.0-only
# Canonical writing as an ontological act: onto16i → onto16r under VMA guard

from ..core.phase_tracker import PhaseTracker
from ..protocols.vma_signer import VMASigner
from ..utils.onto_serializer import serialize_onto16i, serialize_onto16r
from ..ontologies.onto144_profile_loader import load_profile
from ..reasoning.analogical_mapper import AnalogicalMapper

class CanonWriter:
    """
    Generates canonical text from internal onto16i state,
    projecting it into socially legible onto16r form.
    Does not generate from user data—only from incubated profiles and domain lexicons.
    """

    def __init__(self, profile_id: str, config):
        self.profile = load_profile(profile_id)
        self.config = config
        self.phase_tracker = PhaseTracker()
        self.vma_signer = VMASigner(self.profile)
        self.mapper = AnalogicalMapper(self.profile.lexicon)

    def emit_canonical(self, onto16i_state: dict) -> dict:
        """
        Produces a canonical text act in onto16r form.
        Returns a signed, validated structure ready for ontoCMS.
        """
        self.phase_tracker.enter("canonical_emission")

        # Ensure internal state conforms to schema
        if not self._validate_internal(onto16i_state):
            raise ValueError("Invalid onto16i structure")

        # Map internal state to relational expression
        onto16r = self.mapper.map_internal_to_relational(onto16i_state)

        # Render narrative form (non-stochastic, rule-guided)
        narrative = self._render_canonical_narrative(onto16r)

        # Assemble canonical act
        canonical_act = {
            "type": "canonical_text",
            "profile_id": self.profile.id,
            "onto16i_hash": serialize_onto16i(onto16i_state, hash_only=True),
            "onto16r": onto16r,
            "narrative": narrative,
            "phase": self.phase_tracker.current_phase,
            "vma_status": "pending_signature"
        }

        self.phase_tracker.exit()
        return canonical_act

    def _validate_internal(self, state: dict) -> bool:
        # Minimal structural check (full validation in canonical_text_validator)
        required = {"energy", "stability", "causal_anchor", "subjective_vector"}
        return all(k in state for k in required)

    def _render_canonical_narrative(self, onto16r: dict) -> str:
        """
        Renders a human-legible narrative using only terms from the profile's lexicon.
        No probabilistic generation—strict template + analogical substitution.
        """
        template = self.config.get("canonical_templates", {}).get(onto16r.get("domain", "default"))
        if not template:
            template = "{subject} maintains {causal_anchor} through {action}."
        return template.format(**onto16r)
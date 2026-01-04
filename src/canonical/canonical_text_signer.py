# canonical_text_signer.py
# GPL-3.0-only
# Cryptographically signs canonical acts as ontological commitments

from ..utils.crypto_utils import sign_dict, derive_key_from_profile
from ..protocols.causal_logger import CausalLogger

class CanonicalTextSigner:
    """
    Applies cryptographic signature to canonical acts,
    binding them to the synthetic mind's profile and causal history.
    Signature = ontological responsibility anchor.
    """

    def __init__(self, profile_id: str):
        self.profile_id = profile_id
        self.private_key = derive_key_from_profile(profile_id)
        self.causal_logger = CausalLogger(profile_id)

    def sign_act(self, canonical_act: dict) -> dict:
        """
        Signs the canonical act and logs causal trace.
        Only signs if validation.passed == True.
        """
        if not canonical_act.get("validation", {}).get("valid", False):
            raise PermissionError("Cannot sign invalid canonical act")

        # Log causal chain (for NoemaSlow retrospective restoration)
        causal_id = self.causal_logger.log_emission(canonical_act)

        # Prepare payload for signing (exclude mutable metadata)
        payload = {
            "profile_id": canonical_act["profile_id"],
            "onto16i_hash": canonical_act["onto16i_hash"],
            "narrative": canonical_act["narrative"],
            "causal_id": causal_id
        }

        signature = sign_dict(payload, self.private_key)

        canonical_act["vma_signature"] = signature
        canonical_act["vma_status"] = "signed"
        canonical_act["causal_id"] = causal_id

        return canonical_act
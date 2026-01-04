```python
from src.utils.onto_serializer import serialize_onto16i, serialize_onto16r
from src.ontologies.onto144_profile_loader import load_demo_profile

def test_onto16i_serialization():
    profile = load_demo_profile()
    state = {
        "kernel": profile["kernel"],
        "energy_state": "stable",
        "internal_model": "principle_alpha",
        "temporal_phase": "reflective"
    }
    serialized = serialize_onto16i(state)
    assert isinstance(serialized, str)
    assert '"energy_state": "stable"' in serialized

def test_onto16r_serialization():
    rel = {
        "text": "The synthetic mind declares: truth is invariant.",
        "social_proximity": "public",
        "audience_type": "human",
        "causal_trace": "emit_relational/0xabc"
    }
    serialized = serialize_onto16r(rel)
    assert "social_proximity" in serialized
```

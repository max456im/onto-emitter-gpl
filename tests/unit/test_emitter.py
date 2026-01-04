```python
import pytest
from src.core.emitter import Emitter
from src.ontologies.onto144_profile_loader import load_demo_profile

def test_emitter_initialization():
    profile = load_demo_profile()
    emitter = Emitter(profile=profile)
    assert emitter.profile is not None
    assert emitter.phase_tracker is not None

def test_emit_canonical_produces_onto16i():
    profile = load_demo_profile()
    emitter = Emitter(profile=profile)
    result = emitter.emit_canonical(intent="declare_principle", domain="ethics")
    assert "onto16i" in result
    assert isinstance(result["onto16i"], dict)
    assert "energy_state" in result["onto16i"]
    assert "canonical_text" in result

def test_emit_relational_produces_onto16r():
    profile = load_demo_profile()
    emitter = Emitter(profile=profile)
    result = emitter.emit_relational(intent="explain_principle", audience="human")
    assert "onto16r" in result
    assert "social_proximity" in result["onto16r"]
    assert "text" in result["onto16r"]
```

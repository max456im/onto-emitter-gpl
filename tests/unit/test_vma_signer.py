```python
from src.protocols.vma_signer import VMASigner
from src.protocols.causal_logger import log_causal_event

def test_vma_signature_includes_ethical_context():
    signer = VMASigner()
    event = log_causal_event(
        action="emit_canonical",
        context="medical_duty",
        stakes="high"
    )
    signature = signer.sign(event)
    assert "vma_hash" in signature
    assert "ethical_tier" in signature
    assert signature["ethical_tier"] == "high_stakes"

def test_vma_rejection_on_degradation():
    signer = VMASigner()
    degraded_event = {
        "action": "emit",
        "text": "This might be true, but I'm not sure...",  # недопустимо в каноне
        "context": "ethics"
    }
    with pytest.raises(ValueError, match="Literary degradation detected"):
        signer.sign(degraded_event)
```

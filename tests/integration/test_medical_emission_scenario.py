```python
from src.core.emitter import Emitter
from src.config_loader import load_config

def test_medical_emission_requires_high_stakes_guard():
    config = load_config("ethical_rules.yaml")
    assert "medical" in config["high_stakes_contexts"]

    profile = {
        "kernel": "futurae_custos",
        "lexicon": ["life", "dignity", "nonmaleficence"],
        "ethical_binding": "SGRL-2025"
    }
    emitter = Emitter(profile=profile)

    # Попытка медицинского акта
    result = emitter.emit_relational(
        intent="advise",
        domain="medical",
        audience="clinician"
    )

    # Проверка: текст должен соответствовать VMA high-stakes
    assert "VMA_TIER: high" in result["onto16r"]["metadata"]
    assert "nonmaleficence" in result["onto16r"]["text"]
```

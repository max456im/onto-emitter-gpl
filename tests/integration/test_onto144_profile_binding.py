```python
from src.ontologies.onto144_profile_loader import load_profile_by_path
from src.core.emitter import Emitter

def test_emitter_respects_profile_lexical_binding():
    profile = load_profile_by_path("data/incubation/profiles/choleric_may1985.yaml")
    emitter = Emitter(profile=profile)

    # Профиль содержит: kernel = "resolve", temperament = "choleric"
    assert profile["temperament"] == "choleric"
    assert "resolve" in profile["kernel"]

    canonical = emitter.emit_canonical(intent="act", domain="conflict")
    text = canonical["canonical_text"]

    # Ожидаем решительный, недвусмысленный канон
    assert "will" in text or "must" in text
    assert "perhaps" not in text.lower()
    assert "hesitate" not in text.lower()
```

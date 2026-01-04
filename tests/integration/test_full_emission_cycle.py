```python
from src.core.emitter import Emitter
from src.ontologies.onto144_profile_loader_ext import load_profile_by_id
from src.interfaces.ontocms_bridge import save_act_to_ontocms

def test_full_cycle_from_profile_to_cms():
    profile = load_profile_by_id("onto144-UG-Mind-v1")
    emitter = Emitter(profile=profile)

    # Этап 1: внутреннее бытие
    internal = emitter.emit_canonical(intent="affirm_existence", domain="synthetic_mind")
    assert "onto16i" in internal

    # Этап 2: реляционная проекция
    relational = emitter.emit_relational(intent="declare_existence", audience="human")
    assert "onto16r" in relational

    # Этап 3: сохранение в ontoCMS (имитация)
    act_id = save_act_to_ontocms(internal, relational)
    assert act_id.startswith("act_")
    assert len(act_id) > 10
```

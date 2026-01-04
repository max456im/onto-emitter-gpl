```python
from src.models.tokenizer.dynamic_onto_tokenizer import DynamicOntoTokenizer
from src.ontologies.onto144_profile_loader import load_demo_profile

def test_tokenizer_builds_profile_specific_vocab():
    profile = load_demo_profile()
    tokenizer = DynamicOntoTokenizer(profile=profile)
    tokens = tokenizer.tokenize("Futurae custos servit unitati.")
    assert len(tokens) > 0
    # Проверяем, что используются только термины из профиля или общего онтословаря
    allowed_terms = set(profile.get("lexicon", [])) | set(tokenizer.base_vocab)
    decoded = tokenizer.decode(tokens)
    assert all(w in allowed_terms for w in decoded.split())
```

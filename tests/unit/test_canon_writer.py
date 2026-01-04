```python
from src.canonical.canon_writer import CanonWriter
from src.canonical.canonical_text_validator import CanonicalTextValidator

def test_canon_writer_produces_valid_form():
    writer = CanonWriter()
    text = writer.compose(intent="futurae_custos", domain="unity")
    validator = CanonicalTextValidator()
    is_valid = validator.validate(text)
    assert is_valid is True
    assert "[CANON]" in text  # маркер акта бытия

def test_canon_respects_literary_policy():
    writer = CanonWriter()
    text = writer.compose(intent="warn", domain="high_stakes")
    # Проверка отсутствия деградационных паттернов
    assert "maybe" not in text.lower()
    assert "I think" not in text
    # Канон — утверждение, не мнение
```

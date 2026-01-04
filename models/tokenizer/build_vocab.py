# models/tokenizer/build_vocab.py
# Utility to generate onto_vocab.txt (32k terms) from canonical incubation corpus
# Run once during packaging. Not used at runtime.

import re
from collections import Counter
from pathlib import Path

def build_base_vocab(corpus_dir: str, output_path: str, max_tokens: int = 32000):
    corpus_dir = Path(corpus_dir)
    counter = Counter()

    for txt_file in corpus_dir.rglob("*.txt"):
        with open(txt_file, 'r', encoding='utf-8') as f:
            text = f.read().lower()
            words = re.findall(r'\b[a-zа-яё]{2,}\b', text)
            counter.update(words)

    # Отфильтровать и сохранить
    vocab = [word for word, _ in counter.most_common(max_tokens - 4)]
    special_tokens = ['<pad>', '<unk>', '<bos>', '<eos>']
    full_vocab = special_tokens + vocab

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(full_vocab))

# Пример использования (в скриптах):
# if __name__ == "__main__":
#     build_base_vocab("data/incubation", "models/ontomind-50m/onto_vocab.txt")
# SPDX-License-Identifier: GPL-3.0-only
"""
build_vocab.py — Static utility to generate onto_vocab.txt from incubation corpus.
Used only during model incubation (not at runtime).
"""

import argparse
from pathlib import Path
from collections import Counter
import re

def build_ontology_vocab(
    incubation_dir: Path,
    output_path: Path,
    max_vocab_size: int = 32000
):
    """Builds a 32k-term vocabulary strictly from /data/incubation."""
    token_counter = Counter()

    for txt_file in incubation_dir.rglob("*.txt"):
        with open(txt_file, "r", encoding="utf-8") as f:
            text = f.read().lower()
            tokens = re.findall(r"\b\w+\b", text)
            token_counter.update(tokens)

    # Keep only top terms, exclude numbers/symbols unless canonical
    vocab = [token for token, _ in token_counter.most_common(max_vocab_size - 4)]
    special_tokens = ["<pad>", "<unk>", "<bos>", "<eos>"]
    final_vocab = special_tokens + vocab[:max_vocab_size - 4]

    with open(output_path, "w", encoding="utf-8") as f:
        for token in final_vocab:
            f.write(token + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--incubation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build_ontology_vocab(args.incubation, args.output)
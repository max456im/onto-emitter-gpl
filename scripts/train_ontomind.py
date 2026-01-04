#!/usr/bin/env python3
"""
Обучение модели ontomind-50m только на данных инкубации (без внешних корпусов).
"""

import argparse
import sys
from pathlib import Path

from src.models.ontomind import OntoMindModel
from src.models.tokenizer.build_vocab import build_incubation_vocab
from src.utils.config_loader import load_config


def main():
    parser = argparse.ArgumentParser(description="Обучение ontomind на инкубационных данных")
    parser.add_argument("--incubation-dir", required=True, help="Путь к data/incubation/")
    parser.add_argument("--output-model-dir", required=True, help="Каталог для сохранения модели")
    parser.add_argument("--vocab-size", type=int, default=32000)
    parser.add_argument("--epochs", type=int, default=10)
    args = parser.parse_args()

    incubation_path = Path(args.incubation_dir)
    if not incubation_path.exists():
        print(f"Ошибка: {incubation_path} не существует", file=sys.stderr)
        sys.exit(1)

    print("Сборка словаря из инкубационных текстов...")
    vocab_path = Path(args.output_model_dir) / "onto_vocab.txt"
    build_incubation_vocab(
        incubation_dir=incubation_path,
        output_path=vocab_path,
        vocab_size=args.vocab_size
    )

    print("Инициализация модели...")
    model = OntoMindModel(vocab_path=vocab_path)

    print("Загрузка данных обучения...")
    training_dir = Path("data/training")
    training_dir.mkdir(exist_ok=True)
    # Здесь подразумевается, что bootstrap_incubation.py уже подготовил data/training/
    if not any(training_dir.iterdir()):
        print("Предупреждение: data/training пуст. Запустите bootstrap_incubation.py", file=sys.stderr)

    print("Начало обучения...")
    model.train(
        data_dir=training_dir,
        output_dir=args.output_model_dir,
        epochs=args.epochs
    )

    print(f"Модель сохранена в {args.output_model_dir}")


if __name__ == "__main__":
    main()
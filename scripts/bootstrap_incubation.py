#!/usr/bin/env python3
"""
Подготовка инкубационных текстов: отбор, фильтрация, сегментация по уровням картины мира.
Генерирует data/training/ из data/incubation/ без внешних данных.
"""

import os
import shutil
from pathlib import Path
from src.perception.literary_degradation_detector import LiteraryDegradationDetector
from src.utils.config_loader import load_config


def segment_by_worldview_level(text: str) -> int:
    """
    Простейшая эвристика: определяет уровень картины мира (1–4) по стилю.
    Можно заменить на ontomind-инференс позже.
    """
    if "онтологически" in text or "акт бытия" in text:
        return 4
    elif "следовательно" in text or "в силу" in text:
        return 3
    elif "я ощущаю" in text or "кажется" in text:
        return 2
    else:
        return 1


def main():
    incubation_root = Path("data/incubation")
    training_root = Path("data/training")
    training_root.mkdir(parents=True, exist_ok=True)

    detector = LiteraryDegradationDetector()

    for profile_dir in incubation_root.iterdir():
        if not profile_dir.is_dir():
            continue
        print(f"Обработка профиля: {profile_dir.name}")
        level_dirs = {i: training_root / profile_dir.name / f"level_{i}" for i in range(1, 5)}
        for d in level_dirs.values():
            d.mkdir(parents=True, exist_ok=True)

        for txt_file in profile_dir.glob("*.txt"):
            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if not content:
                continue

            # Проверка деградации
            if detector.is_degraded(content):
                print(f"  Пропущено (деградация): {txt_file.name}")
                continue

            level = segment_by_worldview_level(content)
            dest = level_dirs[level] / txt_file.name
            shutil.copy2(txt_file, dest)

    print("Инкубационные данные подготовлены в data/training/")


if __name__ == "__main__":
    main()
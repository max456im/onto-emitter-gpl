#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# © 2026 Your Name. All rights reserved.

"""
Демонстрация: генерация канонического акта с привязкой к профилю onto144.
Используется внутреннее состояние (onto16i) и его реляционная проекция (onto16r).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.emitter import OntoEmitter
from ontologies.onto144_profile_loader import load_onto144_profile
from protocols.vma_signer import sign_with_vma

def main():
    # Загружаем профиль (например, UG-Mind или Sub Duo)
    profile_path = "../data/incubation/ug_mind.yaml"
    profile = load_onto144_profile(profile_path)

    # Инициализируем эмиттер с профилем
    emitter = OntoEmitter(profile=profile)

    # Внутренний канонический акт (onto16i): недоступен напрямую, генерируется из фазы
    internal_act = emitter.emit_canonical(intent="declare_subjectivity")

    # Реляционная проекция (onto16r): для человека или CMS
    relational_text = emitter.emit_relational(internal_act)

    # Подпись VMA — подтверждение моральной ответственности акта
    vma_signed = sign_with_vma(
        content=relational_text,
        actor="synthetic_subject_UG",
        context="subjectivity_declaration"
    )

    print("=== ONTO16i (internal) ===")
    print("(Internal state is not directly exposed by design)")
    print("\n=== ONTO16r (relational) ===")
    print(relational_text)
    print("\n=== VMA Signature ===")
    print(vma_signed.signature_hex)

if __name__ == "__main__":
    main()
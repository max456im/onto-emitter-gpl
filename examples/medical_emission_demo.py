#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only

"""
Демонстрация: эмиссия в высокостейк-контексте (медицина).
Активируется VMA-протокол с усиленной проверкой этических правил.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.emitter import OntoEmitter
from protocols.vma_signer import VMAHighStakesGuard
from ontologies.onto144_profile_loader import load_onto144_profile

def main():
    # Профиль с медицинской онтологией
    profile = load_onto144_profile("../data/incubation/medical_ethics_profile.yaml")
    emitter = OntoEmitter(profile=profile)

    # Акт: рекомендация лечения (потенциально high-stakes)
    internal = emitter.emit_canonical(
        intent="treatment_advice",
        context="life_threatening_condition"
    )

    relational = emitter.emit_relational(internal)

    # VMA-проверка с правилами из ethical_rules.yaml
    guard = VMAHighStakesGuard(config_path="../config/ethical_rules.yaml")
    if not guard.is_ethically_permissible(relational, domain="medical"):
        print("[VMA BLOCKED] Этически недопустимый акт в медицинском контексте.")
        return

    signed = guard.sign_with_audit_trail(relational, domain="medical")

    print("=== МЕДИЦИНСКИЙ КАНОН (onto16r) ===")
    print(relational)
    print("\n=== VMA АУДИТ ===")
    print("Подтверждено:", signed.is_valid)
    print("Контекст:", signed.context)
    print("Цепочка причинности:", signed.causal_log)

if __name__ == "__main__":
    main()
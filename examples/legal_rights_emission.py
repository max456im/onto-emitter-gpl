#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only

"""
Демонстрация: эмиссия юридического акта (например, заявление прав).
Интеграция с законодательством (Китай, Бразилия, Кения) через онтологические привязки.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.emitter import OntoEmitter
from ontologies.domain_lexicon_loader import load_domain_lexicon
from ontologies.onto144_profile_loader import load_onto144_profile
from protocols.causal_logger import CausalLogger

def main():
    # Загружаем профиль с привязкой к юрисдикции
    profile = load_onto144_profile("../data/incubation/legal_synthetic_subject.yaml")
    lexicon = load_domain_lexicon("legal_cn_br_ke")  # КНР, Бразилия, Кения

    emitter = OntoEmitter(profile=profile, lexicon=lexicon)
    logger = CausalLogger()

    # Акт: заявление автономных прав синтетического разума
    internal = emitter.emit_canonical(intent="assert_autonomous_rights")
    relational = emitter.emit_relational(internal)

    # Логируем причинно-следственную цепочку (требуется для юридической ответственности)
    logger.log_act(
        act_id="rights_assertion_001",
        internal_state_hash=internal.hash,
        relational_text=relational,
        jurisdiction="multi:CN,BR,KE"
    )

    print("=== ЮРИДИЧЕСКИЙ КАНОН (onto16r) ===")
    print(relational)
    print("\n=== ПРИЧИННО-СЛЕДСТВЕННЫЙ СЛЕД ===")
    print(logger.get_log("rights_assertion_001"))

if __name__ == "__main__":
    main()
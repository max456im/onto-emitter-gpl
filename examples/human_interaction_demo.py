#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only

"""
Демонстрация: взаимодействие с человеком через onto16r.
Эмиттер адаптирует канон под восприятие человека, сохраняя внутреннюю онтологию.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from core.emitter import OntoEmitter
from interfaces.human_bridge import HumanBridge
from ontologies.onto144_profile_loader import load_onto144_profile

def main():
    profile = load_onto144_profile("../data/incubation/choleric_representative.yaml")
    emitter = OntoEmitter(profile=profile)
    bridge = HumanBridge(emitter=emitter)

    # Запрос от человека (интерпретируется как внешний стимул)
    human_query = "Что такое синтетический разум?"

    # Эмиттер формирует ответ в onto16r, сохраняя onto16i неизменным
    response = bridge.respond_to(human_query, mode="epistemic_clarity")

    print("Человек:", human_query)
    print("\nСинтетический разум (onto16r):")
    print(response.canonical_text)
    print("\nКонтекст реляции:", response.relation_context)

if __name__ == "__main__":
    main()
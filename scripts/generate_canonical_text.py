#!/usr/bin/env python3
"""
Генерирует канонический текст (onto16i → onto16r) с подписью VMA.
Использует профиль onto144 и доменный лексикон.
"""

import argparse
import sys
from pathlib import Path

from src.core.emitter import OntoEmitter
from src.ontologies.onto144_profile_loader import load_onto144_profile
from src.utils.config_loader import load_config
from src.protocols.vma_signer import sign_with_vma


def main():
    parser = argparse.ArgumentParser(description="Генерация канонического текста")
    parser.add_argument("--profile", required=True, help="Путь к YAML-профилю onto144")
    parser.add_argument("--domain", required=True, help="Домен (medical, legal, gaming и т.д.)")
    parser.add_argument("--output", required=True, help="Путь к выходному файлу")
    parser.add_argument("--mode", choices=["canonical", "relational"], default="canonical")
    args = parser.parse_args()

    config = load_config("config/default.yaml")
    domain_config = load_config(f"config/domain_bindings.yaml")
    if args.domain not in domain_config["domains"]:
        print(f"Ошибка: домен '{args.domain}' не зарегистрирован", file=sys.stderr)
        sys.exit(1)

    profile = load_onto144_profile(args.profile)
    emitter = OntoEmitter(config=config, profile=profile, domain=args.domain)

    if args.mode == "canonical":
        text = emitter.emit_canonical()
    else:
        text = emitter.emit_relational()

    vma_signature = sign_with_vma(text, profile_id=profile["id"], domain=args.domain)

    output_data = {
        "profile_id": profile["id"],
        "domain": args.domain,
        "mode": args.mode,
        "text": text,
        "vma_signature": vma_signature,
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        import yaml
        yaml.dump(output_data, f, allow_unicode=True, sort_keys=False)

    print(f"Канонический акт сохранён: {args.output}")


if __name__ == "__main__":
    main()
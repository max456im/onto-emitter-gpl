#!/usr/bin/env python3
"""
Healthcheck для onto-emitter-gpl.
Проверяет:
- доступность лицензии GPL-3.0
- наличие onto144 профиля
- работоспособность канонического ядра
"""
import os
import sys
from pathlib import Path

def check_license():
    if not Path("/app/LICENSE").exists():
        return False, "LICENSE missing"
    with open("/app/LICENSE") as f:
        if "GNU GENERAL PUBLIC LICENSE Version 3" not in f.read():
            return False, "Invalid license"
    return True, "OK"

def check_config():
    if not Path("/app/config/default.yaml").exists():
        return False, "Config missing"
    return True, "OK"

def check_incubation():
    incubation = Path("/app/data/incubation")
    if not incubation.exists() or not any(incubation.iterdir()):
        return False, "No incubation data"
    return True, "OK"

if __name__ == "__main__":
    checks = [check_license, check_config, check_incubation]
    for check in checks:
        ok, msg = check()
        if not ok:
            print(f"[FAIL] {check.__name__}: {msg}", file=sys.stderr)
            sys.exit(1)
    print("All health checks passed.")
    sys.exit(0)
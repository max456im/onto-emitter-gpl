# hardware_probe.py — GPL-3.0-only
"""
Обнаружение аппаратного контекста для лицензионного и этического контроля.
Минималистичный сбор: только архитектура, ОС, наличие TEE (опционально).
Не собирает MAC, serial, user data.
"""

import platform
import os

def probe_hardware_context() -> dict:
    """
    Возвращает минимально достаточный аппаратный контекст.
    Используется license_guard.py для проверки условий GPL-исполнения.
    """
    context = {
        "os": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
        "has_tee": _detect_tee(),  # placeholder для SGX/TrustZone
        "is_container": _is_container(),
    }
    return context

def _detect_tee() -> bool:
    """Простая эвристика — не обязательна, но полезна для high-stakes."""
    # В реальной реализации — проверка через /dev/sgx, dmesg и т.д.
    return False

def _is_container() -> bool:
    """Определение, запущено ли в контейнере (ограниченная среда для лицензии)."""
    return os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv")
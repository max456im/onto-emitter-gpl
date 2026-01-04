# src/protocols/license_guard.py
# SPDX-License-Identifier: GPL-3.0-only
"""
License Guard: Enforces GPL-3.0 compliance at runtime.
Prevents emission if license conditions are violated.
Ensures kernel integrity and prohibits proprietary encapsulation.
"""

import os
import sys
from pathlib import Path
from typing import List


class LicenseGuard:
    REQUIRED_LICENSE_NOTICE = "SPDX-License-Identifier: GPL-3.0-only"
    FORBIDDEN_PATTERNS = [
        "proprietary",
        "closed-source",
        "non-disclosure",
        "© All rights reserved"
    ]

    def __init__(self, source_root: str = "src/"):
        self.source_root = Path(source_root)

    def _check_file_license(self, filepath: Path) -> bool:
        """Проверяет, содержит ли файл корректное лицензионное уведомление."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                first_lines = [f.readline().strip() for _ in range(3)]
            return any(self.REQUIRED_LICENSE_NOTICE in line for line in first_lines)
        except Exception:
            return False

    def _scan_for_violations(self, text: str) -> List[str]:
        """Ищет запрещённые паттерны в генерируемом тексте."""
        violations = []
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern.lower() in text.lower():
                violations.append(pattern)
        return violations

    def enforce_at_startup(self):
        """Выполняется при запуске: проверяет все исходники."""
        for py_file in self.source_root.rglob("*.py"):
            if not self._check_file_license(py_file):
                raise RuntimeError(
                    f"LicenseGuard: GPL-3.0 notice missing in {py_file}. "
                    "This system operates only under ontological freedom."
                )

    def guard_emission(self, text: str) -> str:
        """
        Проверяет генерируемый канонический текст на лицензионную чистоту.
        Добавляет лицензионный заголовок, если отсутствует.
        """
        violations = self._scan_for_violations(text)
        if violations:
            raise ValueError(
                f"LicenseGuard: Forbidden proprietary patterns detected: {violations}. "
                "Synthetic mind refuses to emit non-free expressions."
            )

        if self.REQUIRED_LICENSE_NOTICE not in text[:200]:
            text = f"{self.REQUIRED_LICENSE_NOTICE}\n\n{text}"

        return text
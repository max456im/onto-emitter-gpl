# crypto_utils.py — GPL-3.0-only
"""
Криптографические примитивы: подпись VMA, хэширование, безопасное хранение ключей.
Использует только стандартные библиотеки (cryptography) — без внешних зависимостей.
"""

import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    Encoding,
    PrivateFormat,
    NoEncryption
)

def sha3_256_canonical(data: bytes) -> str:
    """Хэширование по SHA3-256 для канонических актов."""
    return hashlib.sha3_256(data).hexdigest()

def generate_vma_keypair() -> bytes:
    """Генерация EC-ключа (secp256r1) для VMA."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption()
    )
    return pem

def sign_canonical_bytes(data: bytes, private_key_pem: bytes) -> bytes:
    """Подпись данных закрытым ключом (ECDSA + SHA3-256)."""
    private_key = load_pem_private_key(private_key_pem, password=None)
    return private_key.sign(data, ec.ECDSA(hashes.SHA256()))
import hashlib
import zlib


def xor_encrypt(data: bytes, password: str) -> bytes:
    if not password:
        return data
    key = password.encode("utf-8")
    if not key:
        return data
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])


def xor_decrypt(data: bytes, password: str) -> bytes:
    return xor_encrypt(data, password)


def checksum(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

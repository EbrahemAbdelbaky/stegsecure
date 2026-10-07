from .security import xor_encrypt, checksum
from .image_utils import open_image, ensure_capacity, bytes_to_bits

MAGIC = b"STEG"


def _embed_bits_in_image(image, bits: str) -> None:
    pixels = image.load()
    width, height = image.size
    total_bits = len(bits)
    bit_index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            if bit_index < total_bits:
                r = (r & ~1) | int(bits[bit_index])
                bit_index += 1
            if bit_index < total_bits:
                g = (g & ~1) | int(bits[bit_index])
                bit_index += 1
            if bit_index < total_bits:
                b = (b & ~1) | int(bits[bit_index])
                bit_index += 1

            pixels[x, y] = (r, g, b)

            if bit_index >= total_bits:
                return


def _build_payload(secret_text: str, password: str) -> bytes:
    data = secret_text.encode("utf-8")
    encrypted = xor_encrypt(data, password)
    return encrypted


def encode_text(image_path: str, output_path: str, secret_text: str, password: str = "") -> str:
    if not secret_text:
        raise ValueError("Secret text cannot be empty.")

    image = open_image(image_path)

    payload = _build_payload(secret_text, password)
    payload_len = len(payload)

    header = MAGIC + payload_len.to_bytes(4, byteorder="big") + checksum(payload).to_bytes(4, byteorder="big")
    bit_stream = bytes_to_bits(header) + bytes_to_bits(payload)

    ensure_capacity(image, len(bit_stream))

    _embed_bits_in_image(image, bit_stream)
    image.save(output_path)

    return output_path

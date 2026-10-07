from .security import xor_decrypt, checksum
from .image_utils import open_image, bits_to_bytes, bytes_to_bits

MAGIC = b"STEG"


def _extract_n_bits(image, total_bits: int) -> str:
    bits = []
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits.extend([str(r & 1), str(g & 1), str(b & 1)])

            if len(bits) >= total_bits:
                return "".join(bits[:total_bits])

    raise ValueError("Not enough bits found in image to decode data.")


def _extract_bits_after_offset(image, offset_bits: int, total_bits: int) -> str:
    bits = []
    pixels = image.load()
    width, height = image.size
    consumed = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            channels = [r, g, b]

            for channel in channels:
                if consumed >= offset_bits and len(bits) < total_bits:
                    bits.append(str(channel & 1))
                consumed += 1

                if len(bits) >= total_bits:
                    return "".join(bits)

    raise ValueError("Unable to extract the complete payload.")


def decode_text(image_path: str, password: str = "") -> str:
    image = open_image(image_path)

    header_bits = _extract_n_bits(image, 96)
    header = bits_to_bytes(header_bits)

    if len(header) < 12:
        raise ValueError("No hidden message detected.")

    magic = header[:4]
    if magic != MAGIC:
        raise ValueError("Invalid steganography signature. No hidden message found.")

    payload_len = int.from_bytes(header[4:8], byteorder="big")
    stored_checksum = int.from_bytes(header[8:12], byteorder="big")

    if payload_len <= 0:
        raise ValueError("Hidden message length is invalid or empty.")

    payload_bits = _extract_bits_after_offset(image, 96, payload_len * 8)
    payload = bits_to_bytes(payload_bits)

    if len(payload) != payload_len:
        raise ValueError("Payload length mismatch while decoding.")

    decrypted = xor_decrypt(payload, password)

    if checksum(decrypted) != stored_checksum:
        raise ValueError("Checksum mismatch. The message may be corrupted or password is incorrect.")

    try:
        return decrypted.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Decoded data is not valid UTF-8 text.")

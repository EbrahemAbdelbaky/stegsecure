from PIL import Image


def open_image(path: str):
    return Image.open(path).convert("RGB")


def image_capacity(image) -> int:
    return image.width * image.height * 3


def ensure_capacity(image, needed_bits: int):
    cap = image_capacity(image)
    if needed_bits > cap:
        raise ValueError(
            f"Image is too small for this payload. Required bits: {needed_bits}, "
            f"available bits: {cap}."
        )


def bits_to_bytes(bits: str) -> bytes:
    if len(bits) % 8 != 0:
        raise ValueError("Bit length is not divisible by 8.")
    return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))


def bytes_to_bits(data: bytes) -> str:
    return "".join(format(b, "08b") for b in data)

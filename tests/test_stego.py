import os
import tempfile
from PIL import Image

from stego.encoder import encode_text
from stego.decoder import decode_text


def test_round_trip_with_password():
    img = Image.new("RGB", (200, 200), color=(255, 255, 255))
    with tempfile.TemporaryDirectory() as d:
        original = os.path.join(d, "cover.png")
        encoded = os.path.join(d, "encoded.png")

        img.save(original)

        secret = "This is a secret message hidden in an image!"
        encode_text(original, encoded, secret, password="secure123")

        decoded = decode_text(encoded, password="secure123")
        assert decoded == secret


def test_invalid_password_fails():
    img = Image.new("RGB", (200, 200), color=(255, 255, 255))
    with tempfile.TemporaryDirectory() as d:
        original = os.path.join(d, "cover.png")
        encoded = os.path.join(d, "encoded.png")

        img.save(original)

        secret = "Password protected hidden text"
        encode_text(original, encoded, secret, password="correct-password")

        try:
            decode_text(encoded, password="wrong-password")
            assert False, "Expected ValueError for wrong password"
        except ValueError:
            pass

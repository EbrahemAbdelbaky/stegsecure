# StegSecure

StegSecure is a secure image steganography project built in Python. It allows users to hide secret text inside an image and decode it later using a password (optional).

## Features
- Hide text inside an image using LSB steganography
- Extract hidden text from encoded images
- Password protection
- Integrity check using checksum validation
- Simple GUI built with Tkinter
- Works with PNG, JPG, and BMP images

## Team Roles
1. Team Lead / Project Manager
2. Image Processing Engineer
3. Algorithm Developer
4. UI Developer
5. QA / Documentation

## Project Structure
- `app.py` - GUI application
- `stego/encoder.py` - Encode logic
- `stego/decoder.py` - Decode logic
- `stego/security.py` - Password encryption and checksum
- `stego/image_utils.py` - Image access and helper functions
- `tests/` - Unit tests

## Installation
```bash
pip install -r requirements.txt
```

## Run the GUI
```bash
python app.py
```

## Run tests
```bash
pytest
```

## How it works
This project uses least significant bit (LSB) steganography:
- The secret text is converted to bytes
- It is optionally encrypted with a XOR key based on the password
- A header is added with metadata:
  - magic signature
  - payload length
  - checksum
- The bits are embedded into the least significant bits of image pixels
- On decode, the data is extracted, validated, and the original message is restored

## Notes
- This project is suitable for educational and university use
- It is not a replacement for advanced cryptographic steganography systems
- For higher security, it can be extended with AES encryption and stronger encoding schemes

from pathlib import Path
import binascii

def read_file(path: Path):
    with open(path, 'rb') as f:
        while chunk := f.read(16):
            hex_data = binascii.hexlify(chunk, sep=' ').decode('ascii')
            print(f'{len(chunk):04X}: {hex_data}')

def read_file_binary(path: Path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None


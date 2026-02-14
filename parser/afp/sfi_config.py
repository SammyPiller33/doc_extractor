"""
Module for defining structured field syntax, types, and related constants.
"""

from typing import NamedTuple

CARRIAGE_CONTROL: bytes = b'\x5a' # Échappements hexadécimaux
"""Carriage control code for MODCA structured fields."""

################################################
# ===== Structured field introducer syntax =====

SFI_CMPNT_TYPE_UBIN = 1  # Unsigned binary integer
SFI_CMPNT_TYPE_CODE = 2  # Fixed binary code
SFI_CMPNT_TYPE_BITS = 3  # Bit flags
SFI_CPMNT_TYPE_HEXA = 4  # Raw bytes (hex)

class SfiComponent(NamedTuple):
    offset: int
    length: int
    name: str
    type: int
    mandatory: bool

"""
Structured Field Introducer (SFI) component.

Attributes:
    offset (int): Starting position of the component in the field.
    length (int): Length of the component in bytes.
    name (str): Name of the component.
    type (int): Type of data (UBIN, CODE, BITS, RAW).
    mandatory (bool): Indicates whether the component is mandatory.
"""

SFI_STRUCTURE: list[SfiComponent] = [
    SfiComponent(0, 2, 'sf_len', SFI_CMPNT_TYPE_UBIN, True),
    SfiComponent(2, 3, 'sf_id', SFI_CMPNT_TYPE_CODE, True),
    SfiComponent(5, 1, 'flags', SFI_CMPNT_TYPE_BITS, True),
    SfiComponent(6, 2, 'reserved', SFI_CPMNT_TYPE_HEXA, True),
    SfiComponent(8, 1, 'extension_len', SFI_CMPNT_TYPE_UBIN, False),
    SfiComponent(9, 0, 'extension_data', SFI_CPMNT_TYPE_HEXA, False)
]
"""
Structured Field Introducer syntax according to MODCA specification.

List of components defining the structure of an SFI:
    - sf_len: Total length of the structured field (mandatory)
    - sf_id: Structured field type identifier (mandatory)
    - flags: Control flags (mandatory)
    - reserved: Reserved bytes (mandatory)
    - extension_len: Extension data length (optional)
    - extension_data: Extension data (optional)
"""
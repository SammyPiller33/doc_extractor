"""
Module for streaming and parsing AFP (Advanced Function Presentation) structured fields.

This module provides the SfStreamer class which allows efficient streaming and parsing
of structured fields from AFP files using memory mapping for optimal performance.
"""

from parser.common.file_parser import FileParser

from pathlib import Path
from parser.afp.sf_config import *
import mmap
import struct

class SfStreamer(FileParser):
    """
    Class for streaming structured fields from an AFP file.

    This class uses memory mapping to efficiently read and parse AFP structured fields
    sequentially from a file. It validates the AFP format and extracts both the
    Structured Field Introducer (SFI) and the structured field data.

    Attributes:
        afp_path (Path): Path object pointing to the AFP file.
        afp_offset (int): Current read offset in the AFP file (in bytes).
        afp_len (int): Total size of the AFP file (in bytes).

    Raises:
        FileNotFoundError: If the specified AFP file does not exist.
        ValueError: If the specified path is not a file.
        OSError: If file information cannot be read.
    """

    def __init__(self, afp_path: str) -> None:
        """
        Initialize the SfStreamer with an AFP file path.

        Args:
            afp_path (str): Path to the AFP file to be parsed.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the path is not a file.
            OSError: If file information cannot be read.
        """

        # Construct the path to the AFP file
        self.afp_path = Path(afp_path)

        if not self.afp_path.exists():
            raise FileNotFoundError(f"Le fichier '{afp_path}' n'existe pas.")

        if not self.afp_path.is_file():
            raise ValueError(f"Le chemin '{afp_path}' n'est pas un fichier.")

        # Initialize the offset and length of the AFP file.
        # The offset is set to 0 and incremented as structured fields are read.
        self.afp_offset = 0
        # The length is obtained from the file size. It is used to determine when to stop reading structured fields.
        try:
            self.afp_len = self.afp_path.stat().st_size
        except OSError as e:
            raise OSError(f"Impossible de lire les informations du fichier '{afp_path}': {e}")

    def stream(self):
        """
        Stream structured fields from the AFP file one at a time (generator).

        This generator function opens the AFP file using memory mapping for efficient
        access and yields each structured field as a dictionary containing the field
        name, SFI data, and field data.

        Yields:
            dict: A dictionary with the following keys:
                - sf_name (str): Short name of the structured field (e.g., "BDT", "EPG").
                - sfi_data (dict): Parsed Structured Field Introducer data.
                - sf_data (bytes or None): Raw structured field data, or None if unknown type.

        Raises:
            EOFError: If an unexpected end of file is encountered.
            ValueError: If an AFP structure error is detected.
            OSError: If a file access error occurs.
        """

        try:
            with open(self.afp_path, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                    while self.afp_offset < self.afp_len:
                        try:
                            yield self.read_sf(mmapped_file)
                        except EOFError:
                            raise EOFError(f"Fin de fichier inattendue à l'offset {self.afp_offset}")
                        except ValueError as e:
                            raise ValueError(f"Erreur de structure AFP à l'offset {self.afp_offset}: {e}")

        except OSError as e:
            raise OSError(f"Erreur d'accès au fichier: {e}")

    def read_sf(self, f) -> dict:
        """
        Read the next structured field from the file.

        This method reads and parses a single structured field at the current offset.
        It validates the carriage control byte, parses the SFI, determines the field
        type, and extracts the field data.

        Args:
            f: Memory-mapped file object to read from.

        Returns:
            dict: A dictionary containing:
                - sf_name (str): Short name of the structured field or "NA" if unknown.
                - sfi_data (dict): Parsed SFI metadata including length, ID, flags, etc.
                - sf_data (bytes or None): Raw field data or None for unknown types.

        Raises:
            ValueError: If the carriage control byte is invalid (not 0x5A).
        """

        f.seek(self.afp_offset, 0)

        # Check if the file is an AFP file by reading the first byte of the next chunck.
        # The carriage control byte 0x5A starts each structured field.
        control = f.read(1)
        if control != CARRIAGE_CONTROL:
            raise ValueError("Le fichier n'est pas un fichier AFP conforme")

        # Parse the SFI. It contains information about the structured field type, its length, and other metadata.
        sfi_data = self._parse_sfi(f)

        # Get the structured field type name from the SF ID, in the SF_TYPES dictionary.
        sf = SF_TYPES.get(sfi_data['sf_id'], None)
        sf_name = sf.short_name if sf else "NA"

        # Parse the SF data using the pre-calculated length from sfi_data
        sf_data = self._parse_sf(f, sfi_data['sf_data_len']) if sf else None

        self.afp_offset += sfi_data['sf_len'] + 1
        return {
            'sf_name': sf_name,
            'sfi_data': sfi_data,
            'sf_data': sf_data
        }


    @staticmethod
    def _parse_sfi(f) -> dict:
        """
        Parse the Structured Field Introducer (SFI) - common to all structured fields.

        The SFI is an 8-byte header (optionally followed by extension data) that precedes
        every structured field in an AFP file. It contains metadata about the field such as
        length, type identifier, and control flags.

        Args:
            f: Memory-mapped file object positioned after the carriage control byte.

        Returns:
            dict: Parsed SFI data containing:
                - sf_len (int): Total length of the structured field (excluding carriage control).
                - sf_id (bytes): 3-byte structured field identifier.
                - flags (str): 8-bit binary string representation of control flags.
                - has_extension (bool): Whether extension data is present.
                - extension_len (int, optional): Length of extension data if present.
                - extension_data (str, optional): Hex string of extension data if present.
                - sf_data_len (int): Calculated length of the structured field data.
        """

        # Declare a dict to store parsed data
        sfi_parsed = {}

        # Iterate over each component of the SFI. Each component has an offset, a length, a given name,
        # and a boolean indicating whether it is mandatory.
        # Each component is processed according to its type (int, bytes, etc.)
        for component in SFI:

            # Test if the component is mandatory. Mandatory components are parsed without any condition.
            if component.mandatory:

                # Read the component's data. The length is given by the component's attribute.
                # The data is read as bytes.
                data = f.read(component.length)

                # Parse the component based on its name using pattern matching
                match component.name:
                    # Test if the component is the SF length (sf_len).
                    case 'sf_len':
                        # Cast int from Big-endian (2 bytes). Big-endian byte order = most significant byte first.
                        sfi_parsed[component.name] = struct.unpack('>H', data)[0]

                    # Test if the component is the SF ID (sf_id). The id is a unique identifier
                    # for each structured field type.
                    case 'sf_id':
                        # Store the SF ID as bytes
                        sfi_parsed[component.name] = data

                    # Test if the component is the Flags (flags).
                    # The flags field contains control information. The first bit indicates whether an extension is present.
                    case 'flags':
                        # Extract the single byte value and display as binary
                        sfi_parsed[component.name] = f"{data[0]:08b}"
                        # Check if the extension bit is set
                        sfi_parsed['has_extension'] = bool(data[0] & 0x80)

                    # Test if the component is the Reserved (reserved).
                    # The reserved field is reserved by the standard for future use. No need to parse it.
                    case 'reserved':
                        continue

            # Test if the component is not mandatory and if an extension is present.
            # The optional component is parsed only if the extension bit is set in the flags field.
            elif not component.mandatory and sfi_parsed.get('has_extension', False):

                match component.name:
                    # Test if the component is the Extension Length (extension_len). It is stored as a single byte.
                    case 'extension_len':
                        data = f.read(component.length)
                        ext_len = data[0]
                        sfi_parsed[component.name] = ext_len

                    # Test if the component is the Extension Data (extension_data).
                    case 'extension_data':
                        # Get the extension length from the parsed data
                        ext_len = sfi_parsed.get('extension_len', 0)
                        # Read the extension data if it exists
                        if ext_len > 0:
                            # Parse the extension data
                            data = f.read(ext_len - 1)
                            sfi_parsed[component.name] = data.hex().upper()

        # Calculate the length of the SF data
        sfi_parsed["sf_data_len"] = sfi_parsed["sf_len"] - 8 - sfi_parsed.get("extension_len", 0)

        return sfi_parsed

    @staticmethod
    def _parse_sf(f, data_len: int) -> bytes:
        """
        Parse the structured field data.

        Reads the raw data bytes for a structured field based on the provided length.

        Args:
            f: Memory-mapped file object positioned at the start of the field data.
            data_len (int): Number of bytes to read for the structured field data.

        Returns:
            bytes: Raw structured field data.
        """

        # Read the SF data directly using the pre-calculated length
        return f.read(data_len)

"""
Module for streaming and parsing AFP (Advanced Function Presentation) structured fields.

This module provides the SfStreamer class which allows efficient streaming and parsing
of structured fields from AFP files using memory mapping for optimal performance.
"""

from parser.afp.sf_config import SF_CONFIGS
from parser.afp.sf_handlers import SF_HANDLERS
from parser.file_parser import FileParser
from parser.afp.sfi_handlers import SFI_HANDLERS

from pathlib import Path
from parser.afp.sfi_config import *
from parser.afp.sf_filter import SfFilter
import mmap

class SfStreamer(FileParser):
    """
    Class for streaming structured fields from an AFP file.

    This class uses memory mapping to efficiently read and parse AFP structured fields
    sequentially from a file. It validates the AFP format and extracts both the
    Structured Field Introducer (SFI) and the structured field data.

    Attributes:
        _path (Path): Path object pointing to the AFP file.
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
        super().__init__(afp_path)

        if not self._path.exists():
            raise FileNotFoundError(f"Le fichier '{afp_path}' n'existe pas.")

        if not self._path.is_file():
            raise ValueError(f"Le chemin '{afp_path}' n'est pas un fichier.")

        # Initialize the offset and length of the AFP file.
        # The offset is set to 0 and incremented as structured fields are read.
        self.afp_offset = 0
        # The length is obtained from the file size. It is used to determine when to stop reading structured fields.
        try:
            self.afp_len = self._path.stat().st_size
        except OSError as e:
            raise OSError(f"Impossible de lire les informations du fichier '{afp_path}': {e}")
        
        # Store the filter
        self.sf_filter = SfFilter()

    def set_config(self, config: SfFilter) -> None:
        self.sf_filter = config

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
                - sf_data (dict or bytes): Parsed structured field data.

        Raises:
            EOFError: If an unexpected end of file is encountered.
            ValueError: If an AFP structure error is detected.
            OSError: If a file access error occurs.
        """

        try:
            with open(self._path, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                    while self.afp_offset < self.afp_len:
                        try:
                            sf_data = self.read_sf(mmapped_file)
                            # Only yield if the SF was not filtered out
                            if sf_data is not None:
                                yield sf_data
                        except EOFError:
                            raise EOFError(f"Fin de fichier inattendue à l'offset {self.afp_offset}")
                        except ValueError as e:
                            raise ValueError(f"Erreur de structure AFP à l'offset {self.afp_offset}: {e}")

        except OSError as e:
            raise OSError(f"Erreur d'accès au fichier: {e}")

    def read_sf(self, f) -> dict | None:
        """
        Read the next structured field from the file.

        Returns:
            dict: Parsed SF data if it should be processed, None if filtered out.
        """
        f.seek(self.afp_offset, 0)

        # Tous les champs structurés sont délimités par un contrôle de ligne
        control = f.read(1)
        if control != CARRIAGE_CONTROL:
            raise ValueError("Le fichier n'est pas un fichier AFP conforme")

        # Un champ structuré débute un SFI (Structured Field Introducer)
        sfi_data = SfParser.parse_sfi(f)

        # update the offset for next SF
        self.afp_offset += sfi_data['sf_len'] + 1

        # Use the bytes version for lookups
        sf_id_bytes = sfi_data['sf_id_bytes']

        # Get SF name by ID (using bytes)
        sf_name = SfParser.get_sf_name(sf_id_bytes)

        # Check if this SF should be parsed.
        # The SF must be referenced in sf_config.SF_STRUCTURES and not filtered out.
        should_parse = sf_name != "NA" and self.sf_filter.should_parse(sf_name)

        if not should_parse:
            # Skip the data entirely without reading it into memory
            f.seek(sfi_data['sf_data_len'], 1)  # 1 = SEEK_CUR (relative to current position)
            return None

        # Parse the data according to its structure (using bytes)
        sf_data = SfParser.parse_sf_data(f, sfi_data['sf_data_len'], sf_id_bytes)

        # Remove the internal bytes version before returning (keep only hex string)
        del sfi_data['sf_id_bytes']

        # Return data for SFs that should be parsed
        return {
            'sf_name': sf_name,
            'sfi_data': sfi_data,
            'sf_data': sf_data
        }

class SfParser:
    """Utility class for parsing AFP structured field components."""

    @staticmethod
    def parse_sfi(f) -> dict:
        """
        Parse the Structured Field Introducer (SFI).

        Args:
            f: Memory-mapped file object positioned after the carriage control byte.

        Returns:
            dict: Parsed SFI data.
        """
        sfi_parsed = {}
        context = {}

        for component in SFI_STRUCTURE:
            handler = SFI_HANDLERS.get(component.type)
            if not handler:
                continue

            result = handler.parse(f, component, context)
            if result:
                field_name, value = result
                sfi_parsed[field_name] = value
                # Update context with parsed values for dependent fields
                context[field_name] = value

        sfi_parsed['has_extension'] = context.get('has_extension', False)

        # Store the bytes version for internal lookups
        sfi_parsed['sf_id_bytes'] = context.get('sf_id_bytes')

        # Calculate SF data length for
        sfi_parsed["sf_data_len"] = sfi_parsed["sf_len"] - 8 - sfi_parsed.get("extension_len", 0)

        return sfi_parsed

    @staticmethod
    def parse_sf_data(f, data_len: int, sf_id: bytes) -> dict | bytes:
        """
        Parse the structured field data according to its configuration.

        Args:
            f: Memory-mapped file object.
            data_len: Number of bytes to read.
            sf_id: 3-byte structured field identifier (bytes, not hex string).

        Returns:
            dict: Parsed structured field data if configuration exists.
            bytes: Raw bytes if FIELD_BASE_STRUCTURE or no configuration.
        """
        sf_parsed = {}
        sf_config = SF_CONFIGS.get(sf_id, None)

        if not sf_config:
            # SF inconnu : on lit en hexa brut
            handler = SF_HANDLERS.get(1)
            sf_parsed["NA"] = handler.parse(f, data_len)
        else:
            structure = sf_config.struct
            bytes_read = 0

            for component in structure:
                handler = SF_HANDLERS.get(component.type)

                if not handler:
                    # Si pas de handler, skip les bytes
                    if component.length > 0:
                        f.read(component.length)
                        bytes_read += component.length
                    continue

                # Calculer la longueur réelle pour les composants à longueur variable
                comp_length = component.length
                if comp_length == 0:
                    # Longueur variable = reste des données
                    comp_length = data_len - bytes_read

                # Parser le composant
                value = handler.parse(f, comp_length)

                # Ajouter au dictionnaire seulement si non-None
                if value is not None:
                    sf_parsed[component.name] = value

                bytes_read += comp_length

        return sf_parsed

    @staticmethod
    def get_sf_name(sf_id: bytes) -> str:
        """
        Get the structured field name from its ID.

        Args:
            sf_id: 3-byte structured field identifier (bytes, not hex string).

        Returns:
            str: Short name of the SF or "NA" if unknown.
        """
        sf = SF_CONFIGS.get(sf_id, None)
        return sf.short_name if sf else "NA"

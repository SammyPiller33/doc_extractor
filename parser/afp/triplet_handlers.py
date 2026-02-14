
"""Handlers for parsing triplet components."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class TripletComponentHandler(ABC):
    """Base class for triplet component handlers."""

    @abstractmethod
    def parse(self, f, component_length) -> Optional[Any]:
        """
        Parse a triplet component from the file stream.

        Args:
            f: File-like object positioned at component start
            component_length: Length of the component data

        Returns:
            Parsed value or None
        """
        pass


class HexaHandler(TripletComponentHandler):
    """Handler for hexadecimal data."""

    def parse(self, f, component_length) -> Optional[str]:
        if component_length > 0:
            return f.read(component_length).hex().upper()
        return None


class BytesHandler(TripletComponentHandler):
    """Handler for raw bytes data."""

    def parse(self, f, component_length) -> Optional[str]:
        if component_length > 0:
            # Convert to hex string for JSON serialization
            f.read(component_length).hex().upper()
        return None


class GidHandler(TripletComponentHandler):
    """Handler for GID (Global Identifier) data."""

    def parse(self, f, component_length) -> Optional[str]:
        if component_length > 0:
            data = f.read(component_length)
            return data.decode('cp500', errors='replace').rstrip()
        return None


class ReservedHandler(TripletComponentHandler):
    """Handler for reserved/unused data."""

    def parse(self, f, component_length) -> Optional[None]:
        # Skip reserved bytes
        if component_length > 0:
            f.read(component_length)
        return None


class CharHandler(TripletComponentHandler):
    """Handler for character/text data."""

    def parse(self, f, component_length) -> Optional[str]:
        if component_length > 0:
            data = f.read(component_length)
            return data.decode('cp500', errors='replace').rstrip()
        return None


# Registry
TRIPLET_HANDLERS = {
    1: HexaHandler(),          # TRPLT_CMPNT_TYPE_HEXA
    2: BytesHandler(),         # TRPLT_CMPNT_TYPE_CODE
    3: BytesHandler(),         # TRPLT_CMPNT_TYPE_PARAM
    4: GidHandler(),           # TRPLT_CMPNT_TYPE_GID
    6: ReservedHandler(),      # TRPLT_CMPNT_TYPE_RESERVED
    7: CharHandler(),          # TRPLT_CMPNT_TYPE_CHAR
    8: BytesHandler(),         # TRPLT_CMPNT_TYPE_UBIN
}
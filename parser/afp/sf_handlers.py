"""Handlers for parsing SFI components."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class SfComponentHandler(ABC):
    """Base class for SF component handlers."""

    @abstractmethod
    def parse(self, f, component, context: dict) -> Optional[tuple[str, Any]]:
        """
        Parse an SF component from the file stream.

        Args:
            f: File-like object positioned at component start
            component: SfComponent configuration
            context: Parsing context (e.g., parsed values, flags)

        Returns:
            tuple: (field_name, parsed_value) or None to skip
        """
        pass


class RawHandler(SfComponentHandler):
    """Handler for TYPE_RAW (raw bytes as hex)."""

    def parse(self, f, component, component_length) -> Optional[tuple[str, Any]]:

        if component_length > 1:
            return component.name, f.read(component_length).hex().upper()
        else:
            return None


class CharHandler(SfComponentHandler):
    """Handler for TYPE_CHAR (single ASCII character)."""

    def parse(self, f, component, component_length) -> Optional[tuple[str, Any]]:
        return component.name, f.read(component_length).decode('cp500', errors='replace').rstrip()

class TripletHandler(SfComponentHandler):
    """Handler for TYPE_TRIPLET (repeating triplet structures)."""

    def parse(self, f, component, component_length) -> Optional[tuple[str, Any]]:
        triplet = f.read(component_length)
        return component.name, triplet




# Registry
SFI_HANDLERS = {
    1: RawHandler(),
    2: CharHandler(),
    3: TripletHandler(),
}


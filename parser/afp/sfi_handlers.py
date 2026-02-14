"""Handlers for parsing SFI components."""
from abc import ABC, abstractmethod
from typing import Any, Optional
import struct


class SfiComponentHandler(ABC):
    """Base class for SFI component handlers."""

    @abstractmethod
    def parse(self, f, component, context: dict) -> Optional[tuple[str, Any]]:
        """
        Parse an SFI component from the file stream.

        Args:
            f: File-like object positioned at component start
            component: SfiComponent configuration
            context: Parsing context (e.g., parsed values, flags)

        Returns:
            tuple: (field_name, parsed_value) or None to skip
        """
        pass

    def should_parse(self, component, context: dict) -> bool:
        """Check if this component should be parsed."""
        if component.mandatory:
            return True
        return context.get('has_extension', False)


class UnsignedBinaryHandler(SfiComponentHandler):
    """Handler for TYPE_UBIN (unsigned binary integers)."""

    def parse(self, f, component, context: dict) -> Optional[tuple[str, Any]]:
        if not self.should_parse(component, context):
            return None

        data = f.read(component.length)

        if component.length == 1:
            value = data[0]
        elif component.length == 2:
            value = struct.unpack('>H', data)[0]
        elif component.length == 4:
            value = struct.unpack('>I', data)[0]
        else:
            value = int.from_bytes(data, byteorder='big')

        return component.name, value


class CodeHandler(SfiComponentHandler):
    """Handler for TYPE_CODE (fixed binary codes)."""

    def parse(self, f, component, context: dict) -> Optional[tuple[str, Any]]:
        if not self.should_parse(component, context):
            return None

        data = f.read(component.length)

        # Store raw bytes in context for internal use (lookups)
        if component.name == 'sf_id':
            context['sf_id_bytes'] = data

        # Return hex string for JSON output
        return component.name, data.hex().upper()


class BitsHandler(SfiComponentHandler):
    """Handler for TYPE_BITS (bit flags)."""

    def parse(self, f, component, context: dict) -> Optional[tuple[str, Any]]:
        if not self.should_parse(component, context):
            return None

        data = f.read(component.length)
        binary_str = f"{data[0]:08b}"

        # Update context for subsequent conditional components
        context['has_extension'] = bool(data[0] & 0x80)

        return component.name, binary_str


class HexaHandler(SfiComponentHandler):
    """Handler for TYPE_RAW (raw bytes as hex)."""

    def parse(self, f, component, context: dict) -> Optional[tuple[str, Any]]:
        if component.name == 'reserved':
            if self.should_parse(component, context):
                f.read(component.length)  # Skip reserved bytes
            return None

        if not self.should_parse(component, context):
            return None

        # Handle variable-length extension_data
        if component.length == 0:
            # Variable length - read based on context
            ext_len = context.get('extension_len', 0)
            if ext_len > 1:
                data = f.read(ext_len - 1)
            else:
                return None
        else:
            data = f.read(component.length)

        return component.name, data.hex().upper()


# Registry
SFI_HANDLERS = {
    1: UnsignedBinaryHandler(),
    2: CodeHandler(),
    3: BitsHandler(),
    4: HexaHandler(),
}
